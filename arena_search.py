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
from tools.search.arena.arena import ArenaToolResult, ArenaToolOutput

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


async def search_pdf_chunks(vector_store: VectorStore, pdf_path: str, k: int = 10) -> list:
    """
    Extract text from PDF, chunk it, and find similar chunks across all PDF chunks.
    Searches for more results to allow deduplication by block_id in the GUI.
    Returns a list of DocumentWithScore objects (up to 60 unique chunks).
    """
    # Extract text from PDF
    pdf_text = await extract_text_from_pdf(pdf_path)
    
    if not pdf_text or len(pdf_text.strip()) < 10:
        return []
    
    # Create a temporary document from the PDF text
    from beeai_framework.backend.types import Document
    
    pdf_document = Document(
        content=pdf_text,
        metadata={"source": pdf_path, "type": "pdf"}
    )
    
    # Chunk the PDF document
    text_splitter = TextSplitter.from_name(
        name="langchain:RecursiveCharacterTextSplitter", chunk_size=1000, chunk_overlap=200
    )
    pdf_chunks = await text_splitter.split_documents([pdf_document])
    
    # Search for similar chunks for each PDF chunk and collect all results
    # Use higher k to get more results for deduplication
    all_results = []
    for pdf_chunk in pdf_chunks:
        try:
            # Search using the PDF chunk content as the query
            # Use k*2 to get more candidates for deduplication
            results = await vector_store.search(query=pdf_chunk.content, k=k * 2)
            all_results.extend(results)
        except Exception as e:
            print(f"  Error searching chunk: {e}", file=sys.stderr)
            continue
    
    if not all_results:
        return []
    
    # Sort by similarity score (lower is better for distance-based scores)
    # Return more results (up to 60) to allow deduplication by block_id in GUI
    seen_docs = set()
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
    """
    Search for the most semantically similar chunks to a query.
    """
    print(f"\nSearching for: '{query}'")
    print("=" * 70)

    try:
        # Search for similar documents
        # Request more results to allow for re-ranking
        results = await vector_store.search(query=query, k=k * 3)

        tool_results = []
        for result in results:
            document = result.document
            source = document.metadata.get("source", "Unknown")
            filename = os.path.basename(source) if source != "Unknown" else "Unknown"
            
            block_id = None
            url = "Unknown"
            if filename != "Unknown" and "_" in filename:
                parts = filename.split("_")
                if parts[0].isdigit():
                    block_id = parts[0]
                    url = f"https://are.na/block/{block_id}"
            
            tool_results.append(
                ArenaToolResult(
                    title=filename,
                    description=document.content,
                    url=url
                )
            )
        
        output = ArenaToolOutput(tool_results)

        if output.is_empty():
            print("No results found.")
            return

        # Re-rank results: prioritize exact filename matches
        exact_matches = []
        other_matches = []
        
        query_lower = query.lower()
        
        # We need to pair original results with tool results to keep score info
        paired_results = list(zip(results, tool_results))
        
        for result, tool_result in paired_results:
            source = result.document.metadata.get("source", "Unknown")
            filename = os.path.basename(source) if source != "Unknown" else "Unknown"
            
            # Check for exact match in filename (ignoring extension)
            filename_no_ext = os.path.splitext(filename)[0].lower()
            
            if query_lower in filename.lower() or query_lower == filename_no_ext:
                exact_matches.append((result, tool_result))
            else:
                other_matches.append((result, tool_result))
                
        # Combine results, placing exact matches first
        final_pairs = exact_matches + other_matches
        
        # Trim to requested k
        final_pairs = final_pairs[:k]
        
        print(f"\nFound {len(final_pairs)} similar chunks:\n")
        
        # Use output.sources() to show we can use helper methods
        # (Just as an example of using the tool output capabilities)
        # sources = output.sources()
        # print(f"Sources found: {len(sources)}")

        for i, (result, tool_result) in enumerate(final_pairs, 1):
            document = result.document
            score = result.score
            
            # Use data from tool_result where appropriate
            filename = tool_result.title
            url = tool_result.url
            source = document.metadata.get("source", "Unknown")
            
            # Get content preview (first 300 chars)
            content = tool_result.description
            content_preview = content[:300] + "..." if len(content) > 300 else content

            print(f"{i}. Similarity Score: {score:.4f}")
            print(f"   File: {filename}")
            if url != "Unknown":
                print(f"   URL: {url}")
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

