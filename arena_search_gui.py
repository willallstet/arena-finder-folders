#!/usr/bin/env python3
"""
Simple drag-and-drop GUI for searching the arena vector store.
"""
import asyncio
import math
import os
import sys
import webbrowser
from PyQt6.QtCore import QRect, QRectF, Qt, QThread, pyqtSignal, QTimer
from tools.search.arena.arena import ArenaTool
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget)
from PyQt6.QtGui import QPainter, QColor, QPen, QPixmap, QFont, QTextOption
from arena_search import load_vector_store, search_pdf_chunks
import httpx

class ImageLoaderWorker(QThread):
    """Worker thread for loading block images sequentially using sync httpx."""
    image_loaded = pyqtSignal(str, object, str)  # block_id, qimage, title
    
    def __init__(self):
        super().__init__()
        self.queue = []
        self.running = True
        self.access_token = os.getenv("ARENA_ACCESS_TOKEN")
        
    def add_block(self, block_id):
        """Add a block ID to the processing queue."""
        if block_id not in self.queue:
            self.queue.append(block_id)
    
    def stop(self):
        self.running = False
        self.wait()
        
    def run(self):
        """Process the queue."""
        if not self.access_token:
            # print("Warning: ARENA_ACCESS_TOKEN not set.", file=sys.stderr)
            pass

        while self.running:
            if not self.queue:
                self.msleep(100)
                continue
                
            # Process next block
            block_id = self.queue.pop(0)
            try:
                if not self.access_token:
                    continue
                    
                # Use synchronous httpx
                api_url = f"https://api.are.na/v2/blocks/{block_id}"
                headers = {"Authorization": f"Bearer {self.access_token}"}
                
                with httpx.Client(timeout=10.0) as client:
                    response = client.get(api_url, headers=headers)
                    response.raise_for_status()
                    block_data = response.json()
                
                title = block_data.get("title", "")
                
                # Get image URL
                image_url = None
                if block_data.get("image") and block_data["image"].get("thumb"):
                    image_url = block_data["image"]["thumb"].get("url")
                
                img_obj = None
                if image_url:
                    with httpx.Client(timeout=10.0, follow_redirects=True) as client:
                        img_response = client.get(image_url)
                        img_response.raise_for_status()
                        image_data = img_response.content
                        
                        if image_data:
                            from PyQt6.QtGui import QImage
                            img_obj = QImage.fromData(image_data)
                
                self.image_loaded.emit(block_id, img_obj, title)
                
            except Exception:
                # Ignore errors to keep worker alive
                pass


class DotCanvas(QWidget):
    """Canvas widget that displays dots positioned by similarity score."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dots = []  # List of (score, url, filename, angle, block_id)
        self.block_images = {}  # Dict mapping block_id to QPixmap
        self.block_titles = {}  # Dict mapping block_id to title
        self.hovered_dot_index = None  # Index of dot being hovered, or None
        self.setMinimumSize(800, 800)
        # Enable mouse tracking for hover detection
        self.setMouseTracking(True)
        
        # Initialize image loader
        self.image_loader = ImageLoaderWorker()
        self.image_loader.image_loaded.connect(self.on_image_loaded)
        self.image_loader.start()
        
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

    def on_image_loaded(self, block_id, qimage, title):
        """Handle loaded image from worker."""
        self.block_titles[block_id] = title
        
        if qimage and not qimage.isNull():
            pixmap = QPixmap.fromImage(qimage)
            # Scale to 50x50
            scaled_pixmap = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.block_images[block_id] = scaled_pixmap
        
        self.update()

    def _load_block_image(self, block_id: str):
        """Queue block image for loading."""
        if block_id in self.block_images:
            return
            
        # Mark as loading (using None placeholder)
        self.block_images[block_id] = None
        
        if self.image_loader:
            self.image_loader.add_block(block_id)
    
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
    
    def set_dots(self, dots_data):
        """Set the dots to display directly from pre-processed data.
        
        Args:
            dots_data: List of tuples (score, url, filename, angle, block_id)
        """
        self.dots = dots_data
        
        # Clear image and title cache when setting new dots
        self.block_images = {}
        self.block_titles = {}
        
        # Fetch images for blocks with URLs
        for _, url, _, _, block_id in self.dots:
            if block_id and url != "Unknown":
                self._load_block_image(block_id)
                
        self.update()
    
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
                
                # Use synchronous httpx instead of asyncio/arena_tool to avoid event loop conflicts
                api_url = f"https://api.are.na/v2/blocks/{block_id}"
                headers = {"Authorization": f"Bearer {access_token}"}
                
                with httpx.Client(timeout=10.0) as client:
                    response = client.get(api_url, headers=headers)
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
                # print(f"Error loading image for block {block_id}: {e}", file=sys.stderr)
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
        
        # Calculate center of full canvas (graph is centered regardless of overlays)
        # Adjust center_y slightly upward for better visual balance
        width = self.width()
        height = self.height()
        center_x = width / 2
        center_y = height / 2 - 30  # Move center up by 30px for visual balance
        
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
        
        # Set distance range: most similar at 110px
        min_distance = 100  # Most similar (best score) distance from center
        # Calculate maximum distance to stay within window bounds
        # Use full window dimensions for centering (overlays can overlap)
        available_radius = min(center_x, center_y) - 20  # Small margin from edges only
        max_distance = min(590, available_radius)  # Cap at 590px but ensure within bounds
        
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
                
                # Draw text in a box with word wrapping
                font = QFont("Arial", 9)
                painter.setFont(font)
                
                # Set box dimensions (similar to image size)
                box_width = 80  # Fixed width for text box
                box_height = 50  # Fixed height for text box
                padding = 5
                
                # Calculate box position (centered at dot position)
                bg_x = x - box_width / 2
                bg_y = y - box_height / 2
                
                # Draw white background box
                painter.setBrush(QColor(255, 255, 255))
                painter.setPen(QPen(QColor(0, 0, 0), 1))
                painter.drawRect(int(bg_x), int(bg_y), box_width, box_height)
                
                # Set up text rect with word wrapping (use QRectF for QTextOption)
                text_rect = QRectF(
                    bg_x + padding,
                    bg_y + padding,
                    box_width - padding * 2,
                    box_height - padding * 2
                )
                
                # Enable word wrapping
                text_option = QTextOption()
                text_option.setWrapMode(QTextOption.WrapMode.WordWrap)
                text_option.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
                
                # Draw wrapped text
                painter.setPen(QPen(QColor(0, 0, 0), 1))
                painter.drawText(text_rect, title, text_option)
            else:
                # Fallback: draw dot
                painter.setPen(QPen(QColor(0, 0, 0), 2))
                painter.setBrush(QColor(0, 0, 0))
                dot_size = 8
                painter.drawEllipse(int(x - dot_size/2), int(y - dot_size/2), dot_size, dot_size)
        
        # Draw logo at center (after dots so it's on top)
        if self.logo and not self.logo.isNull():
            self._draw_rotated_logo(painter, center_x, center_y)
        
        # Draw hovered dot's title in top left corner
        if self.hovered_dot_index is not None and self.hovered_dot_index < len(self.dots):
            score, url, filename, angle, block_id = self.dots[self.hovered_dot_index]
            
            title = ""
            if block_id and block_id in self.block_titles:
                title = self.block_titles[block_id]
            
            if title:
                # Set font to 20pt Arial
                font = QFont("Arial", 20)
                painter.setFont(font)
                text_rect = painter.fontMetrics().boundingRect(title)
                
                # Position in top left corner with margin
                margin = 20
                padding = 8
                bg_rect_width = text_rect.width() + padding * 2
                bg_rect_height = text_rect.height() + padding * 2
                bg_rect_x = margin
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
                
                # Draw text centered in box
                painter.setPen(QPen(QColor(0, 0, 0), 1))
                text_bg_rect = QRect(int(bg_rect_x), int(bg_rect_y), int(bg_rect_width), int(bg_rect_height))
                painter.drawText(text_bg_rect, Qt.AlignmentFlag.AlignCenter, title)

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
        center_y = height / 2 - 30  # Match adjusted center from paintEvent
        
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
        
        # Set distance range: most similar at 110px
        min_distance = 110  # Most similar (highest score) distance from center
        # Calculate maximum distance to stay within window bounds
        # Leave margin for image size (50px) and padding (~10px)
        available_radius = min(center_x, center_y) - 20  # Leave margin from edges
        max_distance = min(590, available_radius)  # Cap at 590px but ensure within bounds
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
        center_y = height / 2 - 30  # Match adjusted center from paintEvent
        
        # Find min and max scores
        if not self.dots:
            return
        
        scores = [dot[0] for dot in self.dots]
        min_score = min(scores)
        max_score = max(scores)
        score_range = max_score - min_score if max_score != min_score else 1
        
        # Set distance range: most similar at 110px
        min_distance = 110  # Most similar (highest score) distance from center
        # Calculate maximum distance to stay within window bounds
        # Leave margin for image size (50px) and padding (~10px)
        available_radius = min(center_x, center_y) - 20  # Leave margin from edges
        max_distance = min(590, available_radius)  # Cap at 590px but ensure within bounds
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
        
        # Start search (match CLI default of top-k=5 unless we add UI to change it)
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
        # Stop spinning immediately
        self.canvas.stop_spinning()
        
        print(f"\nReceived {len(results)} ranked documents:")
        print("-" * 70)
        
        # Pass results directly to canvas (logic offloaded to search_pdf_chunks)
        dots = []
        
        for i, item in enumerate(results):
            if isinstance(item, dict):
                filename = item.get('filename', 'Unknown')
                weighted_score = item.get('weighted_score', 0)
                
                # Extract block ID from filename if present
                block_id = None
                url = "Unknown"
                if filename != "Unknown" and "_" in filename:
                    parts = filename.split("_")
                    if parts[0].isdigit():
                        block_id = parts[0]
                        url = f"https://are.na/block/{block_id}"
                
                # Calculate angle for visualization (purely visual)
                import math
                angle = (i * 137.5) * (math.pi / 180)  # Golden angle
                
                dots.append((weighted_score, url, filename, angle, block_id))
                
                if i < 5:
                    print(f"{i+1}. File: {filename} (Score: {weighted_score:.4f})")
            
            else:
                # Fallback for legacy results (shouldn't be hit for PDF search)
                pass

        self.canvas.set_dots(dots)
    
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

