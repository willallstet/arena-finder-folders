# Arena Finder: Project Breakdown
**Built with [BeeAI Framework](https://beeai.dev/)**

## Overview
This is a **RAG (Retrieval-Augmented Generation)** system built on the **BeeAI Framework**. It transforms your Are.na content into a searchable knowledge base.

**BeeAI Role**: The framework provides the standardized building blocks (Tools, Vector Stores, Embeddings) that allow us to easily compose this AI agent workflow.

---

## System Architecture

```
┌─────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  arena.py   │───>  │ arena_vector_    │───>  │  arena_search.py│
│ (BeeAI Tool)│      │    store.py      │      │                 │
│             │      │ (BeeAI Backend)  │      │   (Search)      │
└─────────────┘      └──────────────────┘      └─────────────────┘
     │                        │                         │
     v                        v                         v
  Markdown               Vector Store             Similar Content
  Files (.md)         (Embedded Vectors)           Results
```

---

## Stage 1: Content Ingestion (`arena.py`)

**Purpose**: Fetches content from Are.na API using a custom **BeeAI Tool**.

### BeeAI Integration: The Tool Pattern
The ingestion script isn't just a script—it's a formal Agent Tool defined using BeeAI's `Tool` class. This makes it reusable by any AI agent in the BeeAI ecosystem.

```python
from beeai_framework.tools.tool import Tool
from beeai_framework.emitter.emitter import Emitter

class ArenaTool(Tool[ArenaToolInput, ToolRunOptions, ArenaToolOutput]):
    name = "Are.na"
    description = "Fetch all block titles from a user's Are.na channels..."
    
    def _create_emitter(self) -> Emitter:
        # BeeAI's event system for tracking tool execution
        return Emitter.root().child(namespace=["tool", "search", "arena"])
```

**Why this matters**: By subclassing `Tool`, we get built-in error handling, type validation (`ArenaToolInput`), and observability through the `Emitter` system.

### Content Processing
The tool handles complex logic like paginating through Are.na channels and extracting text from PDF attachments, effectively normalizing external data into a format the AI framework can use.

---

## Stage 2: Vector Store Creation (`arena_vector_store.py`)

**Purpose**: Converts text files into searchable vectors using **BeeAI Backend** components.

### BeeAI Integration: Standardized Backends
Instead of writing raw code for specific databases (like Chroma or Pinecone) or specific models, we use BeeAI's abstractions. This allows us to swap underlying technologies without changing our code.

#### 1. The Embedding Model
We load the embedding model via BeeAI's unified interface:

```python
from beeai_framework.backend.embedding import EmbeddingModel

# BeeAI handles the connection to the local Ollama instance
embedding_model = EmbeddingModel.from_name("ollama:nomic-embed-text")
```

#### 2. The Vector Store
We use `TemporalVectorStore`, a BeeAI adapter that manages storage consistency:

```python
from beeai_framework.backend.vector_store import VectorStore
from beeai_framework.adapters.beeai.backend.vector_store import TemporalVectorStore

# Load or create the store using the BeeAI adapter
vector_store = TemporalVectorStore.load(
    path=VECTOR_DB_PATH, 
    embedding_model=embedding_model
)
```

### Document Processing
We use BeeAI's `TextSplitter` and `DocumentLoader` wrappers to prepare content:

```python
from beeai_framework.backend.text_splitter import TextSplitter

text_splitter = TextSplitter.from_name(
    name="langchain:RecursiveCharacterTextSplitter",
    chunk_size=1000,
    chunk_overlap=200
)
```

---

## Stage 3: Semantic Search (`arena_search.py`)

**Purpose**: Finds semantically similar content using BeeAI's search capabilities.

### BeeAI Integration: Unified Search Interface
The actual search logic is simplified because the `VectorStore` abstraction handles the complexity of converting queries to vectors and calculating cosine similarity.

```python
async def search_pdf_chunks(vector_store, pdf_path, k):
    # 1. Create a BeeAI Document object
    from beeai_framework.backend.types import Document
    pdf_document = Document(content=pdf_text, metadata={...})
    
    # 2. Split using BeeAI splitter
    pdf_chunks = await text_splitter.split_documents([pdf_document])
    
    # 3. Search using the unified VectorStore interface
    for chunk in pdf_chunks:
        results = await vector_store.search(
            query=chunk.content, 
            k=k * 2
        )
```

### Deduplication Strategy
The system returns up to 60 unique results (by content), which the GUI then deduplicates by block_id to show 20 unique blocks. This robust logic ensures the user sees a diverse set of Are.na blocks.

---

## Why Use BeeAI?

1.  **Modularity**: We define the `ArenaTool` once, and it can be used by *any* agent—not just this search script.
2.  **Abstraction**: We switch between embedding models (e.g., OpenAI vs. Ollama) just by changing a string name (`ollama:nomic-embed-text`), without rewriting logic.
3.  **Standardization**: All components (Tools, Vector Stores, Models) speak the same language, making the codebase clean and maintainable.

---

## Technical Stack

-   **Framework**: **[BeeAI](https://beeai.dev/)** (Core orchestration)
-   **Embedding**: Ollama (`nomic-embed-text`) via `beeai_framework.backend`
-   **Storage**: `TemporalVectorStore` via `beeai_framework.adapters`
-   **Client**: httpx (async HTTP requests)
-   **Processing**: pypdf & BeautifulSoup (wrapped in tool logic)
