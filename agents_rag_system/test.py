#!/usr/bin/env python
"""
Test script for ChromaDB 0.6.3 with HTTP client.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Import ChromaDB
import chromadb
from GS.agents_rag_system.db.chroma.vectorstore import ChromaVectorStore
from GS.agents_rag_system.config.config import RAGConfig


def test_http_client():
    """Test the ChromaVectorStore with an HTTP client to a remote ChromaDB server."""

    # 1. Define the host/port from environment or defaults
    chroma_host = os.environ.get("CHROMA_HOST", "localhost")
    chroma_port = int(os.environ.get("CHROMA_PORT", 8000))
    chroma_ssl = os.environ.get("CHROMA_SSL", "").lower() == "true"

    # Generate a random name so we don't collide with old data
    collection_name = f"test_collection_{uuid.uuid4().hex[:8]}"
    print(f"Testing ChromaDB with HTTP client")
    print(f"Host: {chroma_host}:{chroma_port} (SSL: {chroma_ssl})")
    print(f"Collection: {collection_name}")

    # 2. (Optional) Delete old leftover collection with an ephemeral client
    #    so that we're starting fresh.
    print("\n1. Cleanup any old collection with ephemeral client (just in case).")
    try:
        ephemeral_client = chromadb.HttpClient(
            host=chroma_host,
            port=chroma_port,
            ssl=chroma_ssl
        )
        ephemeral_client.delete_collection(collection_name)
        print(f"Deleted old collection if it existed: {collection_name}")
    except Exception as e:
        print(f"No old collection or error ignoring: {e}")

    # 3. Create RAGConfig for the new test collection
    print("\n2. Creating RAGConfig...")
    config = RAGConfig(
        vectorstore_type="chroma",
        collection_name=collection_name,
        persist_directory="./chroma_db",
        embedding_model="sentence-transformers/all-mpnet-base-v2",
        similarity_top_k=2,
        additional_params={
            "use_http_client": True,
            "chroma_host": chroma_host,
            "chroma_port": chroma_port,
            "chroma_ssl": chroma_ssl
        }
    )
    print("RAGConfig created")

    # 4. Create the ChromaVectorStore
    print("\n3. Creating ChromaVectorStore...")
    vectorstore = ChromaVectorStore(config=config)
    print("ChromaVectorStore created")

    # 5. Add documents
    print("\n4. Creating test documents and adding to the vector store...")
    documents = [
        {
            "id": "doc_1",
            "text": "Paris is the capital of France",
            "metadata": {"source": "test", "country": "France"}
        },
        {
            "id": "doc_2",
            "text": "Berlin is the capital of Germany",
            "metadata": {"source": "test", "country": "Germany"}
        },
        {
            "id": "doc_3",
            "text": "Rome is the capital of Italy",
            "metadata": {"source": "test", "country": "Italy"}
        },
        {
            "id": "doc_4",
            "text": "Madrid is the capital of Spain",
            "metadata": {"source": "test", "country": "Spain"}
        }
    ]

    vectorstore.add_documents(documents)

    # Verify they were added
    count = vectorstore.get_collection_count()
    print(f"Collection has {count} documents.")

    if count < len(documents):
        print("⚠️ Not all documents were added successfully? Check logs.")

    # 6. Query
    print("\n5. Testing query...")
    query_text = "capital of France"
    print(f"Query: '{query_text}'")

    results = vectorstore.query(
        query_text=query_text,
        n_results=2
    )
    if results:
        print(f"Got {len(results)} results:")
        for i, doc in enumerate(results):
            print(f"  Result {i + 1}: {doc['text']}")
            print(f"     ID: {doc['id']}")
            print(f"     Metadata: {doc['metadata']}")
            if 'distance' in doc and doc['distance'] is not None:
                print(f"     Distance: {doc['distance']}")
    else:
        print("No results found for query.")

    # 7. Optional: Clean up new collection
    print("\n6. Cleaning up by deleting the current test collection.")
    vectorstore.delete_collection()
    print(f"Deleted collection: {collection_name}")

    print("\n✅ HTTP Client test completed successfully!")

# ---------------------------
# 5) If run as a script...
# ---------------------------
if __name__ == "__main__":
    test_http_client()