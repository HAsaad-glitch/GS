# ChromaDB Vector Store Implementation

This directory contains the implementation of the ChromaDB vector store for the Multi-Agent RAG System. ChromaDB is used to store and query vector embeddings of documents.

## Contents

- `vectorstore.py`: Contains the `ChromaVectorStore` class that integrates with ChromaDB

## Usage

### Basic Usage

```python
from GS.agents_rag_system.config.config import RAGConfig
from GS.agents_rag_system.db.chroma.vectorstore import ChromaVectorStore

# Create a RAG configuration
config = RAGConfig(
    vectorstore_type="chroma",
    collection_name="my_collection",
    persist_directory="./chroma_db",
    embedding_model="sentence-transformers/all-mpnet-base-v2",
    similarity_top_k=3,
    additional_params={}
)

# Initialize the vector store
vectorstore = ChromaVectorStore(config=config)

# Add documents 
documents = [
    {
        "id": "doc1",
        "text": "This is the content of document 1",
        "metadata": {"source": "example", "author": "John Doe"}
    },
    {
        "id": "doc2",
        "text": "This is the content of document 2",
        "metadata": {"source": "example", "author": "Jane Smith"}
    }
]

vectorstore.add_documents(documents)

# Query the vector store
results = vectorstore.query(
    query_text="What is document 1 about?",
    n_results=2
)

# Process results
for doc in results:
    print(f"ID: {doc['id']}")
    print(f"Text: {doc['text']}")
    print(f"Metadata: {doc['metadata']}")
    if 'distance' in doc:
        print(f"Distance: {doc['distance']}")
```

### HTTP Client vs. In-Memory Client

The `ChromaVectorStore` supports three different modes of operation:

1. **HTTP Client**: For connecting to a remote ChromaDB server
   ```python
   config = RAGConfig(
       # ... other parameters ...
       additional_params={
           "use_http_client": True,
           "chroma_host": "localhost", 
           "chroma_port": 8000,
           "chroma_ssl": False
       }
   )
   ```

2. **Local Persistent Client**: For storing data locally on disk
   ```python
   config = RAGConfig(
       # ... other parameters ...
       persist_directory="./chroma_db"  # Local directory to store data
   )
   ```

3. **In-Memory Client**: For temporary storage (data will be lost when the program exits)
   ```python
   config = RAGConfig(
       # ... other parameters ...
       persist_directory=None,
       additional_params={
           "use_in_memory": True
       }
   )
   ```

### Environment Variables (for HTTP Client)

When using the HTTP client, you can set these environment variables instead of specifying in the config:

```bash
export CHROMA_HOST=localhost
export CHROMA_PORT=8000
export CHROMA_SSL=false
```

### Important Notes for  Developers

1. **ChromaDB Version Compatibility**: This implementation is compatible with ChromaDB version 0.6.3. If you update ChromaDB, you might need to adjust this implementation.

2. **Embedding Function**: The code automatically detects and uses the appropriate embedding function. If the built-in `SentenceTransformerEmbeddingFunction` is not available, it falls back to a custom implementation.

3. **Error Handling**: The implementation includes robust error handling and fallbacks. If an HTTP connection fails, it will automatically fall back to an in-memory client.

4. **Document Format**: When adding documents, make sure each document has `id`, `text`, and optionally `metadata` fields.

5. **Collection Management**: Use `delete_collection()` to remove a collection and `get_collection_count()` to check how many documents are in a collection. 