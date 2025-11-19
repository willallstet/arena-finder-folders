#!/usr/bin/env python3
"""
Command-line search tool for the arena vector store.
Usage: 
  python arena_search.py "your search query" [--k 5]
  python arena_search.py --pdf path/to/file.pdf [--k 5]
"""

import argparse
import asyncio
import io
import os
import sys

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None  # type: ignore

from beeai_framework.backend.embedding import EmbeddingModel
from beeai_framework.backend.text_splitter import TextSplitter
from beeai_framework.backend.vector_store import VectorStore

VECTOR_DB_PATH = "arena_vector_store"  # Path to persistent storage


async def load_vector_store() -> VectorStore | None:
    """Load the existing vector store."""
    if not os.path.exists(VECTOR_DB_PATH):
        print(f"Error: Vector store not found at {VECTOR_DB_PATH}", file=sys.stderr)
        print("Run arena_vector_store.py first to create the vector store.", file=sys.stderr)
        return None

    print(f"Loading vector store from: {VECTOR_DB_PATH}")
    embedding_model = EmbeddingModel.from_name("ollama:nomic-embed-text")
    
    from beeai_framework.adapters.beeai.backend.vector_store import TemporalVectorStore
    
    try:
        vector_store = TemporalVectorStore.load(
            path=VECTOR_DB_PATH, embedding_model=embedding_model
        )
        print("Vector store loaded successfully.")
        return vector_store
    except Exception as e:
        print(f"Error loading vector store: {e}", file=sys.stderr)
        return None


async def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file."""

    
    try:
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        
        pdf_file = io.BytesIO(pdf_bytes)
        pdf_reader = PdfReader(pdf_file)
        
        # Extract text from all pages
        extracted_text = []
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text.append(page_text)
        
        return "\n\n".join(extracted_text)
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {e}") from e


async def search_pdf_chunks(vector_store: VectorStore, pdf_path: str, k: int = 5) -> None:
    """
    Extract text from PDF, chunk it, and find the top 20 most similar chunks across all PDF chunks.
    """
    print(f"\nProcessing PDF: {pdf_path}")
    print("=" * 70)
    
    # Extract text from PDF
    print("Extracting text from PDF...")
    pdf_text = await extract_text_from_pdf(pdf_path)
    
    if not pdf_text or len(pdf_text.strip()) < 10:
        print("Error: No text could be extracted from the PDF.", file=sys.stderr)
        return
    
    # Create a temporary document from the PDF text
    from beeai_framework.backend.types import Document
    
    pdf_document = Document(
        content=pdf_text,
        metadata={"source": pdf_path, "type": "pdf"}
    )
    
    # Chunk the PDF document
    print("Chunking PDF content...")
    text_splitter = TextSplitter.from_name(
        name="langchain:RecursiveCharacterTextSplitter", chunk_size=1000, chunk_overlap=200
    )
    pdf_chunks = await text_splitter.split_documents([pdf_document])
    
    print(f"PDF split into {len(pdf_chunks)} chunks")
    print("Searching for similar chunks...\n")
    
    # Search for similar chunks for each PDF chunk and collect all results
    all_results = []
    for i, pdf_chunk in enumerate(pdf_chunks, 1):
        try:
            # Search using the PDF chunk content as the query
            results = await vector_store.search(query=pdf_chunk.content, k=k)
            
            for result in results:
                all_results.append(result)
        except Exception as e:
            print(f"  Error searching for chunk {i}: {e}", file=sys.stderr)
            continue
    
    if not all_results:
        print("No similar chunks found.")
        return
    
    # Sort by similarity score (lower is better for distance-based scores)
    # and get top 20 unique chunks (by document content)
    seen_docs = set()
    unique_results = []
    for result in sorted(all_results, key=lambda x: x.score):
        # Use document content as key to avoid duplicates
        doc_key = result.document.content[:100]  # First 100 chars as key
        if doc_key not in seen_docs:
            seen_docs.add(doc_key)
            unique_results.append(result)
            if len(unique_results) >= 20:
                break
    
    # Display top 20 results
    print("=" * 70)
    print(f"TOP {len(unique_results)} MOST SIMILAR CHUNKS")
    print("=" * 70)
    print()
    
    for i, result in enumerate(unique_results, 1):
        document = result.document
        score = result.score
        
        # Get metadata
        source = document.metadata.get("source", "Unknown")
        filename = os.path.basename(source) if source != "Unknown" else "Unknown"
        
        # Get content preview (first 300 chars)
        content = document.content
        content_preview = content[:300] + "..." if len(content) > 300 else content
        
        print(f"{i}. Similarity Score: {score:.4f}")
        print(f"   File: {filename}")
        if source != "Unknown":
            print(f"   Path: {source}")
        print(f"   Content:")
        # Indent content for readability
        for line in content_preview.split("\n"):
            print(f"   {line}")
        print()


async def search(vector_store: VectorStore, query: str, k: int = 5) -> None:
    """
    Search for the most semantically similar chunks to a query.
    """
    print(f"\nSearching for: '{query}'")
    print("=" * 70)

    try:
        # Search for similar documents
        results = await vector_store.search(query=query, k=k)

        if not results:
            print("No results found.")
            return

        print(f"\nFound {len(results)} similar chunks:\n")

        for i, result in enumerate(results, 1):
            document = result.document
            score = result.score

            # Get metadata
            source = document.metadata.get("source", "Unknown")
            # Extract just the filename from the full path
            filename = os.path.basename(source) if source != "Unknown" else "Unknown"
            
            # Get content preview (first 300 chars)
            content = document.content
            content_preview = content[:300] + "..." if len(content) > 300 else content

            print(f"{i}. Similarity Score: {score:.4f}")
            print(f"   File: {filename}")
            if source != "Unknown":
                print(f"   Path: {source}")
            print(f"   Content:")
            # Indent content for readability
            for line in content_preview.split("\n"):
                print(f"   {line}")
            print()

    except Exception as e:
        print(f"Error during search: {e}", file=sys.stderr)
        raise


async def main() -> None:
    """Main function for command-line search."""
    parser = argparse.ArgumentParser(
        description="Search the arena vector store for semantically similar content.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python arena_search.py "What is intelligence?"
  python arena_search.py "artificial intelligence" --k 10
  python arena_search.py --pdf document.pdf
  python arena_search.py --pdf document.pdf --k 3
        """,
    )
    
    # Create mutually exclusive group for query vs PDF
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "query",
        type=str,
        nargs="?",
        help="The search query to find similar content",
    )
    input_group.add_argument(
        "--pdf",
        type=str,
        metavar="PATH",
        help="Path to a PDF file. Will chunk the PDF and find similar chunks for each PDF chunk.",
    )
    
    parser.add_argument(
        "-k",
        "--top-k",
        type=int,
        default=5,
        help="Number of results to return per query/PDF chunk (default: 5)",
    )

    args = parser.parse_args()

    # Load vector store
    vector_store = await load_vector_store()
    if vector_store is None:
        sys.exit(1)

    # Perform search based on input type
    if args.pdf:
        if not os.path.exists(args.pdf):
            print(f"Error: PDF file not found: {args.pdf}", file=sys.stderr)
            sys.exit(1)
        await search_pdf_chunks(vector_store, args.pdf, k=args.top_k)
    else:
        if not args.query:
            parser.error("Either provide a query string or use --pdf flag")
        await search(vector_store, args.query, k=args.top_k)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nSearch interrupted by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)

