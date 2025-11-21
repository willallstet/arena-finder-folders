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
from pypdf import PdfReader
from beeai_framework.backend.embedding import EmbeddingModel
from beeai_framework.backend.text_splitter import TextSplitter
from beeai_framework.backend.vector_store import VectorStore
from beeai_framework.adapters.beeai.backend.vector_store import TemporalVectorStore
from beeai_framework.backend.types import Document


VECTOR_DB_PATH = "arena_vector_store"


async def load_vector_store() -> VectorStore | None:
    if not os.path.exists(VECTOR_DB_PATH):
        raise FileNotFoundError(f"Vector store not found at {VECTOR_DB_PATH}")
    embedding_model = EmbeddingModel.from_name("ollama:nomic-embed-text")
    vector_store = TemporalVectorStore.load(path=VECTOR_DB_PATH, embedding_model=embedding_model)
    return vector_store

async def extract_text_from_pdf(pdf_path: str) -> str:
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    pdf_file = io.BytesIO(pdf_bytes)
    pdf_reader = PdfReader(pdf_file)
    return "\n\n".join([page.extract_text() for page in pdf_reader.pages])


async def search_pdf_chunks(vector_store: VectorStore, pdf_path: str, k: int = 20) -> list:
    pdf_text = await extract_text_from_pdf(pdf_path)
    if not pdf_text or len(pdf_text.strip()) < 10:
        return []
    pdf_document = Document(content=pdf_text, metadata={"source": pdf_path, "type": "pdf"})
    text_splitter = TextSplitter.from_name(
        name="langchain:RecursiveCharacterTextSplitter", chunk_size=1000, chunk_overlap=200
    )
    pdf_chunks = await text_splitter.split_documents([pdf_document])
    all_results = []
    for pdf_chunk in pdf_chunks:
        results = await vector_store.search(query=pdf_chunk.content, k=k)
        all_results.extend(results)
    if not all_results:
        return []

    seen_docs = set() #for deduplication
    unique_results = []
    for result in sorted(all_results, key=lambda x: x.score):
        # Use document content as key to avoid duplicates
        doc_key = result.document.content[:100]  # First 100 chars as key
        if doc_key not in seen_docs:
            seen_docs.add(doc_key)
            unique_results.append(result)
            if len(unique_results) >= 60:  # Return more for block_id deduplication
                break
    
    return unique_results


async def search(vector_store: VectorStore, query: str, k: int = 5) -> None:
    try:
        results = await vector_store.search(query=query, k=k)
        
        if not results:
            print("No results found.")
            return
        
        print(f"\nFound {len(results)} similar chunks:\n")

        for i, result in enumerate(results, 1):
            document = result.document
            score = result.score
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

    except Exception as e:
        print(f"Error during search: {e}", file=sys.stderr)
        raise


async def main() -> None:
    """Main function for command-line search."""
    parser = argparse.ArgumentParser(
        description="Search the arena vector store for semantically similar content.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
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
        print(f"\nProcessing file: {args.pdf}")
        print("=" * 70)
        results = await search_pdf_chunks(vector_store, args.pdf, k=args.top_k)
        
        if not results:
            print("No similar chunks found.")
        else:
            print(f"TOP {len(results)} MOST SIMILAR CHUNKS")
            print("=" * 70)
            print()
            
            for i, result in enumerate(results, 1):
                document = result.document
                score = result.score
                source = document.metadata.get("source", "Unknown")
                filename = os.path.basename(source) if source != "Unknown" else "Unknown"
                content_preview = document.content[:300] + "..." if len(document.content) > 300 else document.content
                
                print(f"{i}. Similarity Score: {score:.4f}")
                print(f"   File: {filename}")
                if source != "Unknown":
                    print(f"   Path: {source}")
                print(f"   Content:")
                for line in content_preview.split("\n"):
                    print(f"   {line}")
                print()
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

