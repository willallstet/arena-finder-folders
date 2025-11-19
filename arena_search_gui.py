#!/usr/bin/env python3
"""
Simple drag-and-drop GUI for searching the arena vector store.
"""

import asyncio
import os
import sys
import webbrowser

try:
    from PyQt6.QtWidgets import (
        QApplication,
        QMainWindow,
        QWidget,
    )
    from PyQt6.QtCore import Qt, QThread, pyqtSignal
    from PyQt6.QtGui import QPainter, QColor, QPen, QPixmap, QFont
except ImportError:
    print("Error: PyQt6 is required. Install with: pip install PyQt6", file=sys.stderr)
    sys.exit(1)

from arena_search import load_vector_store, search_pdf_chunks


class DotCanvas(QWidget):
    """Canvas widget that displays dots positioned by similarity score."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dots = []  # List of (x, y, score, url, filename) tuples
        self.setMinimumSize(800, 600)
        
        # Load logo
        logo_path = "arena_Logo.png"
        if os.path.exists(logo_path):
            self.logo = QPixmap(logo_path)
        else:
            self.logo = None
    
    def set_dots(self, results: list):
        """Set the dots to display from search results."""
        self.dots = []
        
        if not results:
            return
        
        # Extract block IDs and URLs from results
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
            
            self.dots.append((score, url, filename))
        
        self.update()  # Trigger repaint
    
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
                logo_width = self.logo.width()
                logo_height = self.logo.height()
                logo_x = center_x - logo_width / 2
                logo_y = center_y - logo_height / 2
                painter.drawPixmap(int(logo_x), int(logo_y), self.logo)
            return
        
        scores = [dot[0] for dot in self.dots]
        min_score = min(scores)
        max_score = max(scores)
        score_range = max_score - min_score if max_score != min_score else 1
        
        # Calculate max radius, ensuring dots are at least 200 pixels from center
        available_radius = min(center_x, center_y) * 0.8  # Leave some margin
        min_distance = 200  # Minimum distance from center in pixels
        max_radius = max(available_radius, min_distance)
        
        # Set font for score text
        font = QFont()
        font.setPointSize(9)
        painter.setFont(font)
        
        # Draw dots and lines
        for i, (score, url, filename) in enumerate(self.dots):
            # Normalize score to 0-1 range (lower score = more similar = closer to center)
            normalized = (score - min_score) / score_range
            
            # Calculate distance from center (0 = center, 1 = edge)
            # Use a square root to make distribution more even
            # Map to range [min_distance, max_radius]
            distance_normalized = normalized ** 0.5
            distance = min_distance + distance_normalized * (max_radius - min_distance)
            
            # Calculate angle (distribute evenly around circle)
            angle = (i / len(self.dots)) * 2 * math.pi
            
            # Calculate position using polar coordinates
            x = center_x + distance * math.cos(angle)
            y = center_y + distance * math.sin(angle)
            
            # Draw line from center to dot
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.drawLine(int(center_x), int(center_y), int(x), int(y))
            
            # Calculate position for score text (midpoint of line)
            text_x = (center_x + x) / 2
            text_y = (center_y + y) / 2
            
            # Draw score text
            score_text = f"{score:.3f}"
            text_rect = painter.fontMetrics().boundingRect(score_text)
            text_x -= text_rect.width() / 2
            text_y -= text_rect.height() / 2
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.drawText(int(text_x), int(text_y), score_text)
            
            # Draw dot
            painter.setPen(QPen(QColor(0, 0, 0), 2))
            painter.setBrush(QColor(0, 0, 0))
            dot_size = 8
            painter.drawEllipse(int(x - dot_size/2), int(y - dot_size/2), dot_size, dot_size)
        
        # Draw logo at center (after dots so it's on top)
        if self.logo and not self.logo.isNull():
            logo_width = self.logo.width()
            logo_height = self.logo.height()
            logo_x = center_x - logo_width / 2
            logo_y = center_y - logo_height / 2
            painter.drawPixmap(int(logo_x), int(logo_y), self.logo)
    
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
        
        # Calculate max radius, ensuring dots are at least 200 pixels from center
        available_radius = min(center_x, center_y) * 0.8
        min_distance = 200
        max_radius = max(available_radius, min_distance)
        dot_radius = 8
        
        # Check each dot
        for i, (score, url, filename) in enumerate(self.dots):
            normalized = (score - min_score) / score_range
            distance_normalized = normalized ** 0.5
            distance = min_distance + distance_normalized * (max_radius - min_distance)
            angle = (i / len(self.dots)) * 2 * math.pi
            
            x = center_x + distance * math.cos(angle)
            y = center_y + distance * math.sin(angle)
            
            # Check if click is within dot radius
            if abs(click_x - x) < dot_radius and abs(click_y - y) < dot_radius:
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
        self.setWindowTitle("Arena Search")
        self.setGeometry(100, 100, 1200, 800)
        
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
        self.canvas.set_dots(results)
    
    def on_search_error(self, error: str):
        """Handle search error."""
        # Clear canvas on error
        self.canvas.set_dots([])


def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    window = ArenaSearchGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

