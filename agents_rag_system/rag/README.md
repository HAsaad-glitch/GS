# RAG (Retrieval Augmented Generation) Module

This directory contains the implementation of the RAG system that allows agents to retrieve relevant information from a vector store.

## Contents

- `rag.py`: Contains the `RAG` class that implements the RAG functionality

## Usage

### Basic Usage

```python
from GS.agents_rag_system.config.config import RAGConfig
from GS.agents_rag_system.rag.rag import RAG

# Create a RAG configuration
rag_config = RAGConfig(
    vectorstore_type="chroma",
    collection_name="my_collection",
    persist_directory="./chroma_db",
    embedding_model="sentence-transformers/all-mpnet-base-v2",
    similarity_top_k=3
)

# Initialize the RAG system
rag = RAG(rag_config)

# Add documents to the knowledge base
rag.add_document("path/to/document.pdf")
rag.add_document("path/to/another/document.txt")

# Or add text directly
rag.add_text(
    "This is some important information that should be retrievable.",
    metadata={"source": "manual_entry", "topic": "example"}
)

# Augment a prompt with relevant information
prompt = "Please summarize what you know about RAG systems."
augmented_prompt = rag.augment_prompt(prompt, query="RAG systems")

print(augmented_prompt)
```

### Querying Documents

You can also directly query the RAG system for relevant documents:

```python
results = rag.query("What are the benefits of RAG systems?", top_k=5)

for doc in results:
    print(f"Document: {doc['text']}")
    print(f"Metadata: {doc['metadata']}")
    print(f"Distance: {doc.get('distance')}")
    print("---")
```

### File Types

The `add_document` method supports various file types:

- `.txt`: Plain text files
- `.pdf`: PDF documents
- `.docx`: Microsoft Word documents
- `.md`: Markdown files
- `.html`: HTML files

### Important Notes for  Developers

1. **Document Chunking**: The RAG system automatically chunks larger documents into smaller pieces. You can control this with `chunk_size` and `chunk_overlap` parameters in the RAGConfig.

2. **Context Window Management**: When augmenting prompts, the system ensures that the total context (prompt + retrieved documents) doesn't exceed the model's context window. It will truncate documents if necessary.

3. **Document Processing**: When adding documents, the system:
   - Extracts text from the document based on its file type
   - Chunks the text into manageable pieces
   - Creates embeddings for each chunk
   - Stores the embeddings and text in the vector store

4. **Performance Considerations**:
   - Adding many documents can be slow, as it requires embedding each chunk
   - Using larger embedding models provides better retrieval quality but is slower
   - The `similarity_top_k` parameter controls how many documents to retrieve for each query

5. **Format of Augmented Prompts**: The augmented prompt follows this structure:
   ```
   Original prompt

   Here is some relevant context that might help you:

   [Document 1]
   Text from document 1

   [Document 2]
   Text from document 2

   Please use this context to inform your response.
   ``` 