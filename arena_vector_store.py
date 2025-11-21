import asyncio
import json
import os
from pathlib import Path

from beeai_framework.backend.document_loader import DocumentLoader
from beeai_framework.backend.embedding import EmbeddingModel
from beeai_framework.backend.text_splitter import TextSplitter
from beeai_framework.backend.vector_store import VectorStore
from beeai_framework.adapters.beeai.backend.vector_store import TemporalVectorStore


VECTOR_DB_PATH = "arena_vector_store"  # Path for persistent storage
ARENA_CONTENT_DIR = "arena_content"  # Directory containing markdown files
PROCESSED_FILES_TRACKER = "processed_files.json"  # Track which files have been processed

POPULATE_VECTOR_DB = True  # Set to False to skip population if DB already exists


def load_processed_files() -> dict[str, float]:
    """Load the tracking file of processed files and their modification times."""
    if os.path.exists(PROCESSED_FILES_TRACKER):
        try:
            with open(PROCESSED_FILES_TRACKER, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_processed_files(processed: dict[str, float]) -> None:
    """Save the tracking file of processed files."""
    with open(PROCESSED_FILES_TRACKER, "w") as f:
        json.dump(processed, f, indent=2)


def get_new_files(markdown_files: list[Path], processed_files: dict[str, float]) -> list[Path]:
    """Filter out files that have already been processed and haven't changed."""
    new_files = []
    for file_path in markdown_files:
        file_str = str(file_path)
        mtime = file_path.stat().st_mtime
        
        # File is new if not in processed list, or if modification time has changed
        if file_str not in processed_files or processed_files[file_str] != mtime:
            new_files.append(file_path)
    
    return new_files


async def setup_vector_store() -> VectorStore | None:
    """
    Setup vector store with arena_content markdown files.
    Only processes new or modified files.
    """
    # Create embedding model
    embedding_model = EmbeddingModel.from_name("ollama:nomic-embed-text")

    # Load existing vector store if available
    vector_store = None
    if os.path.exists(VECTOR_DB_PATH):
        print(f"Loading vector store from: {VECTOR_DB_PATH}")
        vector_store = TemporalVectorStore.load(
            path=VECTOR_DB_PATH, embedding_model=embedding_model
        )
    else:
        # Create new vector store if it doesn't exist
        if POPULATE_VECTOR_DB:
            vector_store = VectorStore.from_name(
                name="beeai:TemporalVectorStore", embedding_model=embedding_model
            )

    # Load tracking of processed files
    processed_files = load_processed_files()

    # Get all markdown files from arena_content directory
    content_dir = Path(ARENA_CONTENT_DIR)
    if not content_dir.exists():
        print(f"Error: {ARENA_CONTENT_DIR} directory does not exist")
        return vector_store

    all_markdown_files = list(content_dir.glob("*.md"))
    if not all_markdown_files:
        print(f"No markdown files found in {ARENA_CONTENT_DIR}")
        return vector_store

    # Filter to only new or modified files
    new_files = get_new_files(all_markdown_files, processed_files)
    
    if not new_files:
        print(f"All {len(all_markdown_files)} files have already been processed.")
        if vector_store:
            return vector_store
        else:
            print("No vector store exists. Set POPULATE_VECTOR_DB=True to create one.")
            return None

    print(f"Found {len(all_markdown_files)} total markdown files")
    print(f"Processing {len(new_files)} new or modified files...")

    # Process new files
    if POPULATE_VECTOR_DB and vector_store is not None:
        # Load documents from new files only
        all_documents = []
        updated_processed_files = processed_files.copy()
        
        for file_path in new_files:
            try:
                loader = DocumentLoader.from_name(
                    name="langchain:UnstructuredMarkdownLoader", file_path=str(file_path)
                )
                documents = await loader.load()
                all_documents.extend(documents)
                
                # Mark file as processed with current modification time
                file_str = str(file_path)
                updated_processed_files[file_str] = file_path.stat().st_mtime
                print(f"Loaded {len(documents)} document(s) from {file_path.name}")
            except Exception as e:
                print(f"Failed to load {file_path}: {e}")
                continue

        if not all_documents:
            print("No new documents to process")
            # Still save the processed files tracker in case files were deleted
            save_processed_files(updated_processed_files)
            return vector_store

        # Split documents into chunks
        text_splitter = TextSplitter.from_name(
            name="langchain:RecursiveCharacterTextSplitter", chunk_size=1000, chunk_overlap=200
        )
        documents = await text_splitter.split_documents(all_documents)

        print(f"Split into {len(documents)} document chunks")
        
        # Process documents in smaller batches to avoid connection issues
        batch_size = 20  # Process 20 documents at a time
        total_batches = (len(documents) + batch_size - 1) // batch_size
        
        print(f"Processing {len(documents)} documents in {total_batches} batches of {batch_size}...")
        
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            
            # Retry logic for each batch
            max_retries = 3
            retry_count = 0
            success = False
            
            while retry_count < max_retries and not success:
                try:
                    await vector_store.add_documents(documents=batch)
                    print(f"✓ Processed batch {batch_num}/{total_batches} ({len(batch)} documents)")
                    success = True
                except Exception as e:
                    retry_count += 1
                    if retry_count < max_retries:
                        print(f"⚠ Error processing batch {batch_num} (attempt {retry_count}/{max_retries}): {e}")
                        print(f"   Retrying in 2 seconds...")
                        await asyncio.sleep(2)
                    else:
                        print(f"✗ Failed to process batch {batch_num} after {max_retries} attempts: {e}")
                        print(f"   Skipping this batch and continuing...")
                        break

        print("Vector store populated with new documents")

        # Save vector store to disk
        if hasattr(vector_store, "dump"):
            vector_store.dump(path=VECTOR_DB_PATH)
            print(f"Vector store saved to: {VECTOR_DB_PATH}")

        # Save updated processed files tracker
        save_processed_files(updated_processed_files)
        print(f"Updated processed files tracker: {PROCESSED_FILES_TRACKER}")

    return vector_store


async def search_similar_chunks(vector_store: VectorStore, query: str, k: int = 5) -> None:
    """
    Search for the most semantically similar chunks to a query.
    """
    print(f"\nSearching for chunks similar to: '{query}'")
    print("-" * 60)

    # Search for similar documents
    results = await vector_store.search(query=query, k=k)

    print(f"Found {len(results)} similar chunks:\n")

    for i, result in enumerate(results, 1):
        document = result.document
        score = result.score

        # Get metadata
        source = document.metadata.get("source", "Unknown")
        content_preview = document.content[:200] + "..." if len(document.content) > 200 else document.content

        print(f"{i}. Score: {score:.4f}")
        print(f"   Source: {source}")
        print(f"   Content: {content_preview}")
        print()


async def main() -> None:
    """
    Main function to setup vector store and search for similar chunks.
    """
    # Setup vector store
    vector_store = await setup_vector_store()

    if vector_store is None:
        raise FileNotFoundError(
            "Failed to instantiate Vector Store. "
            "Either set POPULATE_VECTOR_DB=True to create a new one, or ensure the database file exists."
        )

    # Hardcoded user query for demonstration
    user_query = "What is intelligence?"

    # Search for similar chunks
    await search_similar_chunks(vector_store, user_query, k=5)


if __name__ == "__main__":
    asyncio.run(main())

