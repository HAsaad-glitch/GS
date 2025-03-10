#!/usr/bin/env python
"""
Comprehensive test script for the RAG system with OpenAI integration.
Tests the full pipeline including ChromaDB vectorstore and document QA functionality.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import uuid
import json

# Load environment variables
load_dotenv()

# Ensure this script can import from the agent_rag_system package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Import ChromaDB and agent components
from GS.agents_rag_system.config.config import RAGConfig
from GS.agents_rag_system.db.chroma.vectorstore import ChromaVectorStore

# Verify required environment variables
required_vars = ["OPENAI_API_KEY"]
missing_vars = [var for var in required_vars if not os.environ.get(var)]
if missing_vars:
    print(f"❌ Error: Missing required environment variables: {', '.join(missing_vars)}")
    print("Please set these variables in your .env file or environment")
    sys.exit(1)


def test_openai_agent():
    """
    Test OpenAI agent with RAG capabilities.
    This tests the full pipeline including document retrieval and generation.
    """
    print("=" * 80)
    print("TESTING OPENAI AGENT WITH RAG CAPABILITIES")
    print("=" * 80)

    # Generate a unique collection name for this test
    collection_name = f"test_rag_{uuid.uuid4().hex[:8]}"

    # 1. Setup configurations
    print("\n1. Setting up configurations...")

    # Determine which ChromaDB client to use (HTTP or local)
    use_http_client = os.environ.get("CHROMA_HOST") is not None

    if use_http_client:
        chroma_host = os.environ.get("CHROMA_HOST", "localhost")
        chroma_port = int(os.environ.get("CHROMA_PORT", 8000))
        chroma_ssl = os.environ.get("CHROMA_SSL", "").lower() == "true"
        print(f"Using HTTP client with ChromaDB at {chroma_host}:{chroma_port} (SSL: {chroma_ssl})")

        # Create configuration for HTTP client
        rag_config = RAGConfig(
            vectorstore_type="chroma",
            collection_name=collection_name,
            persist_directory="./chroma_db",
            embedding_model="sentence-transformers/all-mpnet-base-v2",
            similarity_top_k=3,
            additional_params={
                "use_http_client": True,
                "chroma_host": chroma_host,
                "chroma_port": chroma_port,
                "chroma_ssl": chroma_ssl
            }
        )
    else:
        print("Using local in-memory ChromaDB client")
        # Create configuration for in-memory client
        rag_config = RAGConfig(
            vectorstore_type="chroma",
            collection_name=collection_name,
            persist_directory=None,
            embedding_model="sentence-transformers/all-mpnet-base-v2",
            similarity_top_k=3,
            additional_params={
                "use_in_memory": True
            }
        )

    # 2. Initialize vector store
    print("\n2. Initializing ChromaVectorStore...")
    try:
        vector_store = ChromaVectorStore(config=rag_config)
        print("✅ ChromaVectorStore initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing ChromaVectorStore: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 3. Prepare test documents
    print("\n3. Preparing test documents...")
    test_documents = [
        {
            "id": "doc_1",
            "text": "Paris is the capital of France. It is known for the Eiffel Tower and the Louvre Museum.",
            "metadata": {"source": "test", "country": "France", "city": "Paris"}
        },
        {
            "id": "doc_2",
            "text": "Berlin is the capital of Germany. The Brandenburg Gate and the Berlin Wall are famous landmarks.",
            "metadata": {"source": "test", "country": "Germany", "city": "Berlin"}
        },
        {
            "id": "doc_3",
            "text": "Rome is the capital of Italy. The Colosseum and Vatican City are major attractions.",
            "metadata": {"source": "test", "country": "Italy", "city": "Rome"}
        },
        {
            "id": "doc_4",
            "text": "Madrid is the capital of Spain. It is home to the Prado Museum and Royal Palace.",
            "metadata": {"source": "test", "country": "Spain", "city": "Madrid"}
        },
        {
            "id": "doc_5",
            "text": "Tokyo is the capital of Japan. It is famous for Tokyo Tower and the Imperial Palace.",
            "metadata": {"source": "test", "country": "Japan", "city": "Tokyo"}
        }
    ]

    # 4. Add documents to vector store
    print("\n4. Adding documents to vector store...")
    try:
        vector_store.add_documents(test_documents)
        count = vector_store.get_collection_count()
        print(f"✅ Successfully added {count} documents to the vector store")
    except Exception as e:
        print(f"❌ Error adding documents: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 5. Test document retrieval
    print("\n5. Testing document retrieval...")
    queries = [
        "What is the capital of France?",
        "Tell me about landmarks in Germany",
        "What can I visit in Rome?"
    ]

    for query in queries:
        print(f"\nQuery: '{query}'")
        try:
            results = vector_store.query(query_text=query, n_results=2)
            if results:
                print(f"✅ Retrieved {len(results)} relevant documents:")
                for i, doc in enumerate(results):
                    print(f"  Document {i + 1}: {doc['text'][:100]}...")
                    if 'metadata' in doc:
                        print(f"  Metadata: {doc['metadata']}")
                    if 'distance' in doc and doc['distance'] is not None:
                        print(f"  Distance: {doc['distance']}")
            else:
                print("❌ No documents retrieved")
        except Exception as e:
            print(f"❌ Error during retrieval: {e}")
            import traceback
            traceback.print_exc()

    # 6. Test OpenAI integration
    print("\n6. Testing OpenAI integration...")
    try:
        import openai
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        # Use a document we retrieved along with a query to test the OpenAI integration
        query = "What are the major attractions in Rome?"
        print(f"\nQuery: '{query}'")

        # Get relevant documents
        context_docs = vector_store.query(query_text=query, n_results=1)
        if not context_docs:
            print("❌ No context documents retrieved")
            context = "No information available"
        else:
            context = context_docs[0]['text']
            print(f"Context: {context}")

        # Create prompt with context and query
        prompt = f"""
        Context information:
        {context}

        Question: {query}

        Please answer the question based on the context information provided.
        """

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a helpful assistant that answers questions based on provided context."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )

        # Print the response
        answer = response.choices[0].message.content.strip()
        print(f"\nOpenAI Response:")
        print(f"{answer}")
        print("\n✅ OpenAI integration successful!")
    except Exception as e:
        print(f"❌ Error during OpenAI integration test: {e}")
        import traceback
        traceback.print_exc()

    # 7. Clean up
    print("\n7. Cleaning up...")
    try:
        vector_store.delete_collection()
        print(f"✅ Successfully deleted collection: {collection_name}")
    except Exception as e:
        print(f"❌ Error deleting collection: {e}")

    print("\n" + "=" * 80)
    print("TEST COMPLETED")
    print("=" * 80)


def test_http_client():
    """Test the HTTP client for ChromaDB."""

    # Set required environment variables if not already set
    if "CHROMA_HOST" not in os.environ:
        os.environ["CHROMA_HOST"] = "localhost"
    if "CHROMA_PORT" not in os.environ:
        os.environ["CHROMA_PORT"] = "8000"

    # Connection parameters
    chroma_host = os.environ.get("CHROMA_HOST", "localhost")
    chroma_port = int(os.environ.get("CHROMA_PORT", 8000))
    chroma_ssl = os.environ.get("CHROMA_SSL", "").lower() == "true"
    collection_name = f"test_collection_{uuid.uuid4().hex[:8]}"

    print(f"Testing ChromaDB with HTTP client")
    print(f"Host: {chroma_host}:{chroma_port} (SSL: {chroma_ssl})")
    print(f"Collection: {collection_name}")

    try:
        # Create config with additional parameters for HTTP client
        print("\n1. Creating RAGConfig...")
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
        print(f"RAGConfig created")

        # Create ChromaVectorStore
        print("\n2. Creating ChromaVectorStore...")
        vectorstore = ChromaVectorStore(config=config)
        print(f"ChromaVectorStore created")

        # Clean up any existing collection
        try:
            vectorstore.delete_collection()
            print(f"Deleted existing collection: {collection_name}")
        except Exception as e:
            print(f"No collection to delete or error: {e}")

        # Create test documents
        print("\n3. Creating test documents...")
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

        # Add documents
        print("\n4. Adding documents to the vector store...")
        vectorstore.add_documents(documents)

        count = vectorstore.get_collection_count()
        print(f"Added {count} documents")

        # Query the vector store
        print("\n5. Testing query...")
        query_text = "capital of France"
        print(f"Query: '{query_text}'")

        results = vectorstore.query(
            query_text=query_text,
            n_results=2
        )

        if results and len(results) > 0:
            print(f"Query successful! Got {len(results)} results:")
            for i, doc in enumerate(results):
                print(f"  Result {i + 1}: {doc['text']}")
                print(f"     ID: {doc['id']}")
                print(f"     Metadata: {doc['metadata']}")
                if 'distance' in doc and doc['distance'] is not None:
                    print(f"     Distance: {doc['distance']}")
        else:
            print("Query returned no results")

        # Clean up
        print("\n6. Cleaning up...")
        vectorstore.delete_collection()
        print(f"Deleted collection: {collection_name}")

        print("\n✅ HTTP Client test completed successfully!")

    except Exception as e:
        print(f"\n❌ HTTP Client test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Choose which test to run based on environment variables
    if len(sys.argv) > 1 and sys.argv[1] == "http":
        test_http_client()
    else:
        test_openai_agent()