# Database Module

This directory contains database implementations for the Multi-Agent RAG System. The database module provides vector storage capabilities for embedding and retrieving documents.

## Directory Structure

- `chroma/`: Implementation of ChromaDB vector store
  - `vectorstore.py`: ChromaDB integration with support for HTTP, persistent, and in-memory clients
  - `README.md`: Detailed documentation for the ChromaDB implementation

## Overview

The database module is responsible for:

1. Storing document embeddings in vector databases
2. Providing efficient similarity search capabilities
3. Managing document collections and metadata
4. Supporting different storage backends

## Current Implementations

### ChromaDB

The system currently uses ChromaDB as its primary vector database. ChromaDB is a powerful, open-source embedding database that allows for:

- Efficient similarity search
- Document metadata storage
- Flexible deployment options (HTTP client, persistent storage, in-memory)

For detailed information on using the ChromaDB implementation, see the [ChromaDB README](./chroma/README.md).

## Usage Example

```python
from GS.agents_rag_system.config.config import RAGConfig
from GS.agents_rag_system.db.chroma.vectorstore import ChromaVectorStore

# Create a configuration
config = RAGConfig(
    vectorstore_type="chroma",
    collection_name="my_documents",
    persist_directory="./data/chroma_db",
    embedding_model="sentence-transformers/all-mpnet-base-v2",
    similarity_top_k=5
)

# Initialize the vector store
vectorstore = ChromaVectorStore(config=config)

# Add documents
documents = [
    {
        "id": "doc1",
        "text": "This is a sample document",
        "metadata": {"source": "example", "category": "sample"}
    }
]

vectorstore.add_documents(documents)

# Query for similar documents
results = vectorstore.query(
    query_text="Find documents about samples",
    n_results=3
)
```

## Extending with New Database Backends

To add support for a new vector database:

1. Create a new subdirectory with the database name
2. Implement a class that provides the same interface as `ChromaVectorStore`
3. Update the factory pattern in the system to support the new database type

## Future Improvements

Potential enhancements for the database module:

- Support for additional vector databases (Pinecone, Weaviate, etc.)
- Hybrid search capabilities (combining vector and keyword search)
- Improved caching mechanisms
- Distributed database support for large-scale deployments 