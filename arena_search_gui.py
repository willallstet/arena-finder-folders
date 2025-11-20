#!/usr/bin/env python3
"""
Simple drag-and-drop GUI for searching the arena vector store.
"""

import asyncio
import math
import os
import random
import sys
import webbrowser
from typing import Optional
from PyQt6.QtCore import QRect

try:
    from PyQt6.QtWidgets import (
        QApplication,
        QMainWindow,
        QWidget,
    )
    from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
    from PyQt6.QtGui import QPainter, QColor, QPen, QPixmap, QFont
except ImportError:
    print("Error: PyQt6 is required. Install with: pip install PyQt6", file=sys.stderr)
    sys.exit(1)

from arena_search import load_vector_store, search_pdf_chunks

try:
    import httpx
except ImportError:
    print("Warning: httpx not available. Install with: pip install httpx", file=sys.stderr)
    httpx = None


class DotCanvas(QWidget):
    """Canvas widget that displays dots positioned by similarity score."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dots = []  # List of (score, url, filename, angle) tuples
        self.block_images = {}  # Dict mapping block_id to QPixmap
        self.block_titles = {}  # Dict mapping block_id to title
        self.hovered_dot_index = None  # Index of dot being hovered, or None
        self.setMinimumSize(800, 800)
        # Enable mouse tracking for hover detection
        self.setMouseTracking(True)
        
        # Load logo
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "arena_Logo.png")
        if os.path.exists(logo_path):
            self.logo = QPixmap(logo_path)
        else:
            self.logo = None
        
        # Rotation animation
        self.rotation_angle = 0
        self.is_spinning = False
        self.start_angle = 0  # Track starting angle to detect full rotation
        self.pending_results = None  # Results waiting to be displayed
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_rotation)
    
    def update_rotation(self):
        """Update rotation angle and trigger repaint."""
        if self.is_spinning:
            prev_angle = self.rotation_angle
            # Rotate by smaller increments for smoother animation
            # At ~60fps (16ms), this gives about 180 degrees per second
            self.rotation_angle += 3  # Rotate by 3 degrees each frame
            
            # Check if we've completed a full rotation (wrapped around)
            if prev_angle < 360 and self.rotation_angle >= 360:
                self.rotation_angle -= 360
                # If we've completed at least one full rotation and have pending results, display them
                if self.pending_results is not None:
                    self._display_pending_results()
                    return  # Don't update after displaying
            elif self.rotation_angle >= 360:
                self.rotation_angle -= 360
            
            self.update()
    
    def start_spinning(self):
        """Start the logo rotation animation."""
        self.is_spinning = True
        self.rotation_angle = 0
        self.start_angle = 0
        self.pending_results = None  # Clear any pending results
        self.timer.start(16)  # Update every ~16ms for ~60fps smooth animation
    
    def stop_spinning(self):
        """Stop the logo rotation animation."""
        self.is_spinning = False
        self.timer.stop()
        self.rotation_angle = 0
        self.update()
    
    def set_pending_results(self, results):
        """Set results that will be displayed after completing a full rotation."""
        self.pending_results = results
    
    def _display_pending_results(self):
        """Display pending results after completing a full rotation."""
        if self.pending_results is not None:
            results = self.pending_results
            self.pending_results = None
            self.stop_spinning()
            self.set_dots(results)
    
    def set_dots(self, results: list):
        """Set the dots to display from search results."""
        self.dots = []
        # Clear image and title cache when setting new dots
        self.block_images = {}
        self.block_titles = {}
        
        if not results:
            return
        
        # Extract block IDs and URLs from results and store with scores
        dot_data = []
        for result in results:
            document = result.document
            score = result.score
            source = document.metadata.get("source", "Unknown")
            filename = os.path.basename(source) if source != "Unknown" else "Unknown"
            
            # Extract block ID from filename (part before underscore)
            block_id = None
            url = None
            if filename != "Unknown" and "_" in filename:
                block_id = filename.split("_")[0]
                url = f"https://are.na/block/{block_id}"
            
            dot_data.append((score, url, filename, block_id))
        
        # Sort by score (highest score = most similar first)
        dot_data.sort(key=lambda x: x[0], reverse=True)
        
        # Alternate placing from beginning and end of sorted list
        num_dots = len(dot_data)
        ordered_dots = []
        start_idx = 0
        end_idx = num_dots - 1
        
        for i in range(num_dots):
            if i % 2 == 0:
                # Even positions: take from beginning (most similar)
                ordered_dots.append(dot_data[start_idx])
                start_idx += 1
            else:
                # Odd positions: take from end (least similar)
                ordered_dots.append(dot_data[end_idx])
                end_idx -= 1
        
        # Assign evenly spaced angles around the circle
        for i, (score, url, filename, block_id) in enumerate(ordered_dots):
            angle = (i / num_dots) * 2 * math.pi
            self.dots.append((score, url, filename, angle, block_id))
            # Start loading image for this block
            if block_id:
                self._load_block_image(block_id)
        
        self.update()  # Trigger repaint
    
    def _load_block_image(self, block_id: str):
        """Load block image from Arena API asynchronously."""
        if block_id in self.block_images:
            return  # Already loaded or loading
        
        if not httpx:
            return  # httpx not available
        
        # Mark as loading to avoid duplicate requests
        self.block_images[block_id] = None
        
        # Use a thread pool or async to load images
        def load_image():
            try:
                # Get Arena access token from environment
                access_token = os.getenv("ARENA_ACCESS_TOKEN")
                if not access_token:
                    print(f"Warning: ARENA_ACCESS_TOKEN not set. Cannot load image for block {block_id}", file=sys.stderr)
                    return
                
                # Fetch block data from Arena API with authentication
                url = f"https://api.are.na/v2/blocks/{block_id}"
                headers = {"Authorization": f"Bearer {access_token}"}
                response = httpx.get(url, headers=headers, timeout=10.0)
                response.raise_for_status()
                block_data = response.json()
                
                # Store title
                title = block_data.get("title", "")
                self.block_titles[block_id] = title
                
                # Get thumb URL only
                image_url = None
                if block_data.get("image") and block_data["image"].get("thumb"):
                    image_url = block_data["image"]["thumb"].get("url")
                
                if image_url:
                    with httpx.Client(timeout=10.0, follow_redirects=True) as client:
                        img_response = client.get(image_url)
                        img_response.raise_for_status()
                        image_data = img_response.content
                    
                    if image_data:
                        pixmap = QPixmap()
                        if pixmap.loadFromData(image_data) and not pixmap.isNull():
                            scaled_pixmap = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                            if not scaled_pixmap.isNull():
                                self.block_images[block_id] = scaled_pixmap
                                QTimer.singleShot(0, self.update)
                else:
                    # No image, trigger repaint to show title
                    QTimer.singleShot(0, self.update)
            except Exception as e:
                # On error, store None to indicate failed load
                print(f"Error loading image for block {block_id}: {e}", file=sys.stderr)
                self.block_images[block_id] = None
        
        # Run in background thread
        from threading import Thread
        thread = Thread(target=load_image, daemon=True)
        thread.start()
    
    def paintEvent(self, event):
        """Draw the dots on the canvas."""
        import math
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        center_x = width / 2
        center_y = height / 2
        
        # Find min and max scores to normalize
        if not self.dots:
            # Still draw logo even if no dots
            if self.logo and not self.logo.isNull():
                self._draw_rotated_logo(painter, center_x, center_y)
            return
        
        scores = [dot[0] for dot in self.dots]
        min_score = min(scores)
        max_score = max(scores)
        score_range = max_score - min_score if max_score != min_score else 1
        
        # Set distance range: most similar at 120px
        min_distance = 120  # Most similar (highest score) distance from center
        # Calculate maximum distance to stay within window bounds
        # Leave margin for dot size (8px) and padding (~10px)
        available_radius = min(center_x, center_y) - 20  # Leave margin from edges
        max_distance = min(600, available_radius)  # Cap at 600px but ensure within bounds
        
        # Draw block images and lines
        for i, (score, url, filename, angle, block_id) in enumerate(self.dots):
            # Normalize score to 0-1 range (higher score = more similar = closer to center)
            normalized = (score - min_score) / score_range
            
            # Calculate distance from center
            # Use a square root to make distribution more even
            # Invert so higher scores (more similar) are closer to center
            # Map to range [min_distance, max_distance]
            distance_normalized = (1 - normalized) ** 0.5
            distance = min_distance + distance_normalized * (max_distance - min_distance)
            
            # Use random angle stored with dot (already assigned in set_dots)
            
            # Calculate position using polar coordinates
            x = center_x + distance * math.cos(angle)
            y = center_y + distance * math.sin(angle)
            
            # Draw line from center to block image
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.drawLine(int(center_x), int(center_y), int(x), int(y))
            
            # Draw block image (50x50px) or title text
            if block_id and block_id in self.block_images:
                pixmap = self.block_images[block_id]
                if pixmap and not pixmap.isNull():
                    # Draw image centered at position
                    img_size = 50
                    img_x = x - img_size / 2
                    img_y = y - img_size / 2
                    painter.drawPixmap(int(img_x), int(img_y), pixmap)
                    continue
            
            # Fallback: draw title text if available, otherwise dot
            if block_id and block_id in self.block_titles:
                title = self.block_titles[block_id]
                # Get first 30 characters, add ellipsis if longer
                if len(title) > 30:
                    display_title = title[:27] + "..."
                else:
                    display_title = title
                
                # Draw text centered at position
                font = QFont("Arial", 9)
                painter.setFont(font)
                text_rect = painter.fontMetrics().boundingRect(display_title)
                text_x = x - text_rect.width() / 2
                text_y = y + text_rect.height() / 2
                
                # Draw white background for text
                padding = 3
                bg_x = text_x - padding
                bg_y = text_y - text_rect.height() - padding
                bg_width = text_rect.width() + padding * 2
                bg_height = text_rect.height() + padding * 2
                painter.setBrush(QColor(255, 255, 255))
                painter.setPen(QPen(QColor(0, 0, 0), 1))
                painter.drawRect(int(bg_x), int(bg_y), int(bg_width), int(bg_height))
                
                # Draw text
                painter.setPen(QPen(QColor(0, 0, 0), 1))
                painter.drawText(int(text_x), int(text_y), display_title)
            else:
                # Fallback: draw dot
                painter.setPen(QPen(QColor(0, 0, 0), 2))
                painter.setBrush(QColor(0, 0, 0))
                dot_size = 8
                painter.drawEllipse(int(x - dot_size/2), int(y - dot_size/2), dot_size, dot_size)
        
        # Draw logo at center (after dots so it's on top)
        if self.logo and not self.logo.isNull():
            self._draw_rotated_logo(painter, center_x, center_y)
        
        # Draw hovered dot's similarity score in top right corner
        if self.hovered_dot_index is not None and self.hovered_dot_index < len(self.dots):
            score, url, filename, angle, block_id = self.dots[self.hovered_dot_index]
            score_text = f"{score:.3f}"
            
            # Set font to 30pt Arial
            font = QFont("Arial", 30)
            painter.setFont(font)
            text_rect = painter.fontMetrics().boundingRect(score_text)
            
            # Position in top right corner with margin
            margin = 20
            padding = 8
            bg_rect_width = text_rect.width() + padding * 2
            bg_rect_height = text_rect.height() + padding * 2
            bg_rect_x = width - bg_rect_width - margin
            bg_rect_y = margin
            
            # Draw white background
            painter.setBrush(QColor(255, 255, 255))
            painter.setPen(QPen(Qt.PenStyle.NoPen))
            painter.drawRect(int(bg_rect_x), int(bg_rect_y), int(bg_rect_width), int(bg_rect_height))
            
            # Draw black dashed border
            dashed_pen = QPen(QColor(0, 0, 0), 1)
            dashed_pen.setStyle(Qt.PenStyle.DashLine)
            painter.setPen(dashed_pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(int(bg_rect_x), int(bg_rect_y), int(bg_rect_width), int(bg_rect_height))
            
            # Draw text centered in box using QRect with alignment
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            text_bg_rect = QRect(int(bg_rect_x), int(bg_rect_y), int(bg_rect_width), int(bg_rect_height))
            painter.drawText(text_bg_rect, Qt.AlignmentFlag.AlignCenter, score_text)
    
    def _draw_rotated_logo(self, painter, center_x, center_y):
        """Draw the logo rotated around its center, scaled to 100x100 pixels."""
        # Scale logo to 100x100
        logo_size = 100
        scaled_logo = self.logo.scaled(logo_size, logo_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        logo_width = scaled_logo.width()
        logo_height = scaled_logo.height()
        logo_x = center_x - logo_width / 2
        logo_y = center_y - logo_height / 2
        
        # Save painter state
        painter.save()
        
        # Translate to center of logo, rotate, then translate back
        painter.translate(center_x, center_y)
        painter.rotate(self.rotation_angle)
        painter.translate(-center_x, -center_y)
        
        # Draw the scaled logo
        painter.drawPixmap(int(logo_x), int(logo_y), scaled_logo)
        
        # Restore painter state
        painter.restore()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move to detect hover over dots."""
        import math
        
        mouse_x = event.position().x()
        mouse_y = event.position().y()
        
        width = self.width()
        height = self.height()
        center_x = width / 2
        center_y = height / 2
        
        # Find min and max scores
        if not self.dots:
            if self.hovered_dot_index is not None:
                self.hovered_dot_index = None
                self.update()
            return
        
        scores = [dot[0] for dot in self.dots]
        min_score = min(scores)
        max_score = max(scores)
        score_range = max_score - min_score if max_score != min_score else 1
        
        # Set distance range: most similar at 120px
        min_distance = 120  # Most similar (highest score) distance from center
        # Calculate maximum distance to stay within window bounds
        # Leave margin for image size (50px) and padding (~10px)
        available_radius = min(center_x, center_y) - 20  # Leave margin from edges
        max_distance = min(600, available_radius)  # Cap at 600px but ensure within bounds
        hover_radius = 30  # Hover radius for 50x50px images
        
        # Check each dot for hover
        hovered_index = None
        for i, (score, url, filename, angle, block_id) in enumerate(self.dots):
            normalized = (score - min_score) / score_range
            # Invert so higher scores (more similar) are closer to center
            distance_normalized = (1 - normalized) ** 0.5
            distance = min_distance + distance_normalized * (max_distance - min_distance)
            # Use random angle stored with dot (already assigned in set_dots)
            
            x = center_x + distance * math.cos(angle)
            y = center_y + distance * math.sin(angle)
            
            # Check if mouse is within image hover radius
            if abs(mouse_x - x) < hover_radius and abs(mouse_y - y) < hover_radius:
                hovered_index = i
                break
        
        # Update hover state and repaint if changed
        if hovered_index != self.hovered_dot_index:
            self.hovered_dot_index = hovered_index
            # Change cursor to hand when hovering, arrow otherwise
            if hovered_index is not None:
                self.setCursor(Qt.CursorShape.PointingHandCursor)
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)
            self.update()
    
    def leaveEvent(self, event):
        """Handle mouse leaving the widget to clear hover state."""
        if self.hovered_dot_index is not None:
            self.hovered_dot_index = None
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.update()
    
    def mousePressEvent(self, event):
        """Handle mouse click to check if a dot was clicked."""
        import math
        
        if event.button() != Qt.MouseButton.LeftButton:
            return
        
        click_x = event.position().x()
        click_y = event.position().y()
        
        width = self.width()
        height = self.height()
        center_x = width / 2
        center_y = height / 2
        
        # Find min and max scores
        if not self.dots:
            return
        
        scores = [dot[0] for dot in self.dots]
        min_score = min(scores)
        max_score = max(scores)
        score_range = max_score - min_score if max_score != min_score else 1
        
        # Set distance range: most similar at 120px
        min_distance = 120  # Most similar (highest score) distance from center
        # Calculate maximum distance to stay within window bounds
        # Leave margin for image size (50px) and padding (~10px)
        available_radius = min(center_x, center_y) - 20  # Leave margin from edges
        max_distance = min(600, available_radius)  # Cap at 600px but ensure within bounds
        click_radius = 30  # Click radius for 50x50px images
        
        # Check each dot
        for i, (score, url, filename, angle, block_id) in enumerate(self.dots):
            normalized = (score - min_score) / score_range
            # Invert so higher scores (more similar) are closer to center
            distance_normalized = (1 - normalized) ** 0.5
            distance = min_distance + distance_normalized * (max_distance - min_distance)
            # Use angle stored with dot
            
            x = center_x + distance * math.cos(angle)
            y = center_y + distance * math.sin(angle)
            
            # Check if click is within image radius
            if abs(click_x - x) < click_radius and abs(click_y - y) < click_radius:
                if url:
                    webbrowser.open(url)
                break


class SearchWorker(QThread):
    """Worker thread for async search operations."""
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, vector_store, file_path: str, k: int = 5):
        super().__init__()
        self.vector_store = vector_store
        self.file_path = file_path
        self.k = k

    def run(self):
        """Run the search operation."""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(
                search_pdf_chunks(self.vector_store, self.file_path, self.k)
            )
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))
        finally:
            loop.close()


class ArenaSearchGUI(QMainWindow):
    """Simple drag-and-drop GUI for arena vector store search."""
    
    def __init__(self):
        super().__init__()
        self.vector_store = None
        self.worker = None
        self.init_ui()
        self.load_vector_store()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Are.na Vector Search")
        self.setGeometry(100, 100, 800, 800)
        
        # Set white background
        self.setStyleSheet("background-color: white;")
        
        # Create canvas widget
        self.canvas = DotCanvas()
        self.canvas.setStyleSheet("background-color: white;")
        self.setCentralWidget(self.canvas)
        
        # Enable drag and drop
        self.setAcceptDrops(True)
    
    def dragEnterEvent(self, event):
        """Handle drag enter event."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        """Handle drop event."""
        if self.vector_store is None:
            return
        
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        if files and os.path.exists(files[0]):
            self.process_file(files[0])
    
    def load_vector_store(self):
        """Load the vector store."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            self.vector_store = loop.run_until_complete(load_vector_store())
        except Exception:
            pass
        finally:
            loop.close()
    
    def process_file(self, file_path: str):
        """Process dropped file and search for similar chunks."""
        if self.worker and self.worker.isRunning():
            return
        
        # Clear previous results
        self.canvas.set_dots([])
        
        # Start logo spinning animation
        self.canvas.start_spinning()
        
        # Start search
        self.worker = SearchWorker(
            vector_store=self.vector_store,
            file_path=file_path,
            k=5
        )
        self.worker.finished.connect(self.on_search_finished)
        self.worker.error.connect(self.on_search_error)
        self.worker.start()
    
    def on_search_finished(self, results: list):
        """Handle search completion."""
        # Queue results to be displayed after completing a full rotation
        self.canvas.set_pending_results(results)
    
    def on_search_error(self, error: str):
        """Handle search error."""
        # Stop spinning and clear canvas on error immediately
        self.canvas.stop_spinning()
        self.canvas.set_dots([])


def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    window = ArenaSearchGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

