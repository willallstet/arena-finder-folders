#!/usr/bin/env python3
"""
Simple GUI for searching the arena vector store.
"""

import asyncio
import io
import os
import sys
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None  # type: ignore

try:
    from PyQt6.QtWidgets import (
        QApplication,
        QMainWindow,
        QWidget,
        QVBoxLayout,
        QHBoxLayout,
        QPushButton,
        QLineEdit,
        QTextEdit,
        QLabel,
        QFileDialog,
        QMessageBox,
    )
    from PyQt6.QtCore import Qt, QThread, pyqtSignal
except ImportError:
    print("Error: PyQt6 is required. Install with: pip install PyQt6", file=sys.stderr)
    sys.exit(1)

from beeai_framework.backend.embedding import EmbeddingModel
from beeai_framework.backend.text_splitter import TextSplitter
from beeai_framework.backend.vector_store import VectorStore

VECTOR_DB_PATH = "arena_vector_store"


class SearchWorker(QThread):
    """Worker thread for async search operations."""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    progress = pyqtSignal(str)

    def __init__(self, vector_store: VectorStore, query: str = None, pdf_path: str = None, k: int = 5):
        super().__init__()
        self.vector_store = vector_store
        self.query = query
        self.pdf_path = pdf_path
        self.k = k

    def run(self):
        """Run the search operation."""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            if self.pdf_path:
                result = loop.run_until_complete(self._search_pdf())
            else:
                result = loop.run_until_complete(self._search_query())
            
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))
        finally:
            loop.close()

    async def _search_query(self) -> str:
        """Search with text query."""
        results = await self.vector_store.search(query=self.query, k=self.k)
        
        if not results:
            return "No results found."
        
        output = []
        for i, result in enumerate(results, 1):
            document = result.document
            score = result.score
            source = document.metadata.get("source", "Unknown")
            filename = os.path.basename(source) if source != "Unknown" else "Unknown"
            content_preview = document.content[:300] + "..." if len(document.content) > 300 else document.content
            
            output.append(f"{i}. Score: {score:.4f} | File: {filename}")
            output.append(f"   {content_preview}")
            output.append("")
        
        return "\n".join(output)

    async def _search_pdf(self) -> str:
        """Search with PDF file."""
        self.progress.emit("Extracting text from PDF...")
        
        # Extract text from PDF
        if PdfReader is None:
            raise ImportError("pypdf is required. Install with: pip install pypdf")
        
        with open(self.pdf_path, "rb") as f:
            pdf_bytes = f.read()
        
        pdf_file = io.BytesIO(pdf_bytes)
        pdf_reader = PdfReader(pdf_file)
        
        extracted_text = []
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text.append(page_text)
        
        pdf_text = "\n\n".join(extracted_text)
        
        if not pdf_text or len(pdf_text.strip()) < 10:
            return "Error: No text could be extracted from the PDF."
        
        # Create document and chunk it
        self.progress.emit("Chunking PDF...")
        from beeai_framework.backend.types import Document
        
        pdf_document = Document(
            content=pdf_text,
            metadata={"source": self.pdf_path, "type": "pdf"}
        )
        
        text_splitter = TextSplitter.from_name(
            name="langchain:RecursiveCharacterTextSplitter", chunk_size=1000, chunk_overlap=200
        )
        pdf_chunks = await text_splitter.split_documents([pdf_document])
        
        # Search for similar chunks
        self.progress.emit(f"Searching {len(pdf_chunks)} PDF chunks...")
        all_results = []
        for pdf_chunk in pdf_chunks:
            results = await self.vector_store.search(query=pdf_chunk.content, k=self.k)
            all_results.extend(results)
        
        if not all_results:
            return "No similar chunks found."
        
        # Get top 20 unique results
        seen_docs = set()
        unique_results = []
        for result in sorted(all_results, key=lambda x: x.score):
            doc_key = result.document.content[:100]
            if doc_key not in seen_docs:
                seen_docs.add(doc_key)
                unique_results.append(result)
                if len(unique_results) >= 20:
                    break
        
        # Format output
        output = [f"TOP {len(unique_results)} MOST SIMILAR CHUNKS\n"]
        for i, result in enumerate(unique_results, 1):
            document = result.document
            score = result.score
            source = document.metadata.get("source", "Unknown")
            filename = os.path.basename(source) if source != "Unknown" else "Unknown"
            content_preview = document.content[:300] + "..." if len(document.content) > 300 else document.content
            
            output.append(f"{i}. Score: {score:.4f} | File: {filename}")
            output.append(f"   {content_preview}")
            output.append("")
        
        return "\n".join(output)


class ArenaSearchGUI(QMainWindow):
    """Simple GUI for arena vector store search."""
    
    def __init__(self):
        super().__init__()
        self.vector_store = None
        self.worker = None
        self.init_ui()
        self.load_vector_store()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Arena Vector Store Search")
        self.setGeometry(100, 100, 800, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Title
        title = QLabel("Arena Vector Store Search")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Query input section
        query_layout = QHBoxLayout()
        query_label = QLabel("Search Query:")
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Enter your search query...")
        self.query_input.returnPressed.connect(self.search_query)
        query_layout.addWidget(query_label)
        query_layout.addWidget(self.query_input)
        layout.addLayout(query_layout)
        
        # PDF section
        pdf_layout = QHBoxLayout()
        pdf_label = QLabel("PDF File:")
        self.pdf_path_label = QLabel("No file selected")
        self.pdf_path_label.setStyleSheet("color: gray;")
        pdf_button = QPushButton("Browse...")
        pdf_button.clicked.connect(self.select_pdf)
        pdf_layout.addWidget(pdf_label)
        pdf_layout.addWidget(self.pdf_path_label)
        pdf_layout.addWidget(pdf_button)
        layout.addLayout(pdf_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.start_search)
        self.search_button.setEnabled(False)
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_results)
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.clear_button)
        layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: gray; padding: 5px;")
        layout.addWidget(self.status_label)
        
        # Results area
        results_label = QLabel("Results:")
        layout.addWidget(results_label)
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        layout.addWidget(self.results_text)
    
    def load_vector_store(self):
        """Load the vector store."""
        if not os.path.exists(VECTOR_DB_PATH):
            self.status_label.setText("Error: Vector store not found. Run arena_vector_store.py first.")
            self.status_label.setStyleSheet("color: red; padding: 5px;")
            return
        
        try:
            embedding_model = EmbeddingModel.from_name("ollama:nomic-embed-text")
            from beeai_framework.adapters.beeai.backend.vector_store import TemporalVectorStore
            
            self.vector_store = TemporalVectorStore.load(
                path=VECTOR_DB_PATH, embedding_model=embedding_model
            )
            self.status_label.setText("Vector store loaded successfully.")
            self.status_label.setStyleSheet("color: green; padding: 5px;")
            self.search_button.setEnabled(True)
        except Exception as e:
            self.status_label.setText(f"Error loading vector store: {e}")
            self.status_label.setStyleSheet("color: red; padding: 5px;")
    
    def select_pdf(self):
        """Open file dialog to select PDF."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select PDF File", "", "PDF Files (*.pdf)"
        )
        if file_path:
            self.pdf_path_label.setText(os.path.basename(file_path))
            self.pdf_path_label.setStyleSheet("color: black;")
            self.pdf_path = file_path
    
    def search_query(self):
        """Trigger search when Enter is pressed in query input."""
        if self.query_input.text().strip():
            self.start_search()
    
    def start_search(self):
        """Start the search operation."""
        if self.worker and self.worker.isRunning():
            return
        
        query = self.query_input.text().strip()
        pdf_path = getattr(self, 'pdf_path', None)
        
        if not query and not pdf_path:
            QMessageBox.warning(self, "No Input", "Please enter a search query or select a PDF file.")
            return
        
        if pdf_path and not os.path.exists(pdf_path):
            QMessageBox.warning(self, "File Not Found", f"PDF file not found: {pdf_path}")
            return
        
        self.search_button.setEnabled(False)
        self.status_label.setText("Searching...")
        self.status_label.setStyleSheet("color: blue; padding: 5px;")
        self.results_text.clear()
        
        self.worker = SearchWorker(
            vector_store=self.vector_store,
            query=query if query else None,
            pdf_path=pdf_path if pdf_path else None,
            k=5
        )
        self.worker.finished.connect(self.on_search_finished)
        self.worker.error.connect(self.on_search_error)
        self.worker.progress.connect(self.on_search_progress)
        self.worker.start()
    
    def on_search_progress(self, message: str):
        """Update status with progress message."""
        self.status_label.setText(message)
    
    def on_search_finished(self, result: str):
        """Handle search completion."""
        self.results_text.setText(result)
        self.status_label.setText("Search completed.")
        self.status_label.setStyleSheet("color: green; padding: 5px;")
        self.search_button.setEnabled(True)
    
    def on_search_error(self, error: str):
        """Handle search error."""
        self.status_label.setText(f"Error: {error}")
        self.status_label.setStyleSheet("color: red; padding: 5px;")
        self.results_text.setText(f"Error: {error}")
        self.search_button.setEnabled(True)
    
    def clear_results(self):
        """Clear the results area."""
        self.results_text.clear()
        self.query_input.clear()
        self.pdf_path_label.setText("No file selected")
        self.pdf_path_label.setStyleSheet("color: gray;")
        if hasattr(self, 'pdf_path'):
            delattr(self, 'pdf_path')
        self.status_label.setText("Ready")
        self.status_label.setStyleSheet("color: gray; padding: 5px;")


def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    window = ArenaSearchGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

