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
    print(f"Debug: Extracted {len(pdf_text)} chars from PDF: {pdf_path}")
    if not pdf_text or len(pdf_text.strip()) < 10:
        return []
    pdf_document = Document(content=pdf_text, metadata={"source": pdf_path, "type": "pdf"})
    text_splitter = TextSplitter.from_name(
        name="langchain:RecursiveCharacterTextSplitter", chunk_size=1000, chunk_overlap=200
    )
    pdf_chunks = await text_splitter.split_documents([pdf_document])
    
    all_results = []
    # Track which PDF chunk produced each result
    for pdf_chunk in pdf_chunks:
        # Ensure we get the actual content - handle both BeeAI and LangChain Document formats
        chunk_content = pdf_chunk.content if hasattr(pdf_chunk, 'content') else getattr(pdf_chunk, 'page_content', str(pdf_chunk))
        results = await vector_store.search(query=chunk_content, k=k)
        # Store result with its matching PDF chunk (store the content, not the object)
        for result in results:
            all_results.append((result, chunk_content))
    
    if not all_results:
        return []

    # Group by filename and calculate scores
    import math
    doc_groups = {}
    
    for result, pdf_chunk_content in all_results:
        source = result.document.metadata.get("source", "Unknown")
        filename = os.path.basename(source) if source != "Unknown" else "Unknown"
        
        if filename not in doc_groups:
            doc_groups[filename] = {
                "matches": [],
                "total_score": 0,
                "source": source
            }
        
        # Add match if not duplicate (based on content snippet)
        content_snippet = result.document.content[:100]
        is_duplicate = any(m[0].document.content[:100] == content_snippet for m in doc_groups[filename]["matches"])
        
        if not is_duplicate:
            doc_groups[filename]["matches"].append((result, pdf_chunk_content))
            doc_groups[filename]["total_score"] += result.score

    # Calculate final weighted scores
    ranked_docs = []
    for filename, data in doc_groups.items():
        match_count = len(data["matches"])
        if match_count == 0:
            continue
            
        avg_score = data["total_score"] / match_count
        
        weighted_score = avg_score * (1 + math.log10(match_count))
        
        ranked_docs.append({
            "filename": filename,
            "source": data["source"],
            "weighted_score": weighted_score,
            "avg_score": avg_score,
            "match_count": match_count,
            "matches": sorted(data["matches"], key=lambda x: x[0].score, reverse=True) # Top matches first
        })

    ranked_docs.sort(key=lambda x: x["weighted_score"], reverse=True)
    
    # Return top 20 results only
    return ranked_docs[:20]


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
            
            content = document.content
            content_preview = content[:300] + "..." if len(content) > 300 else content

            print(f"{i}. Similarity Score: {score:.4f}")
            print(f"   File: {filename}")
            if source != "Unknown":
                print(f"   Path: {source}")
            print(f"   Content:")
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
        results = await search_pdf_chunks(vector_store, args.pdf, k=args.top_k)
        
        # Grouped display
        if not results:
            print("No similar chunks found.")
        else:
            print(f"TOP MATCHING DOCUMENTS (Weighted Score)")
            print("=" * 70)
            
            for i, doc_data in enumerate(results[:10], 1): # Top 10 documents
                print(f"\n{i}. FILE: {doc_data['filename']}")
                print(f"   Weighted Score: {doc_data['weighted_score']:.4f}")
                print(f"   Matches Found: {doc_data['match_count']}")
                print(f"   Path: {doc_data['source']}")
                print("-" * 40)
                
                # Show top 3 matching chunks for this document
                for j, (match, query_chunk) in enumerate(doc_data['matches'][:3], 1):
                    content = match.document.content
                    preview = content[:200].replace('\n', ' ') + "..."
                    query_preview = query_chunk[:100].replace('\n', ' ') + "..."
                    
                    print(f"   Match {j} (Score: {match.score:.4f}):")
                    print(f"     Query: \"{query_preview}\"")
                    print(f"     Found: \"{preview}\"")
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

