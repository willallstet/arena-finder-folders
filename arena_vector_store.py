import asyncio
import json
import os
import warnings
from pathlib import Path

# Suppress Pydantic warnings about validate_default
warnings.filterwarnings("ignore", message=".*validate_default.*")
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

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
        
        # File is new if not in processed list
        if file_str not in processed_files:
            new_files.append(file_path)
    
    return new_files


async def setup_vector_store() -> VectorStore | None:
    embedding_model = EmbeddingModel.from_name("ollama:nomic-embed-text")
    if os.path.exists(VECTOR_DB_PATH):
        vector_store = TemporalVectorStore.load(
            path=VECTOR_DB_PATH, embedding_model=embedding_model
        )
    else:
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
            # save the processed files tracker in case files were deleted
            save_processed_files(updated_processed_files)
            return vector_store

        # Split documents into chunks
        text_splitter = TextSplitter.from_name(
            name="langchain:RecursiveCharacterTextSplitter", chunk_size=1000, chunk_overlap=200
        )
        documents = await text_splitter.split_documents(all_documents)
        
        batch_size = 20 
        total_batches = (len(documents) + batch_size - 1) // batch_size
                
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
                    print(f"Processed {batch_num}/{total_batches} ")
                    success = True
                except Exception as e:
                    retry_count += 1
                    if retry_count < max_retries:
                        await asyncio.sleep(2)
                    else:
                        print(f"SKIPP-ING ERROR BATCH {batch_num}")
                        break

        vector_store.dump(path=VECTOR_DB_PATH)
        save_processed_files(updated_processed_files)


async def main() -> None:
    """
    Main function to setup and populate the vector store.
    Use arena_search.py for searching the vector store.
    """
    # Setup vector store
    await setup_vector_store()

if __name__ == "__main__":
    asyncio.run(main())

