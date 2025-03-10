#!/usr/bin/env python
"""
Test script for the DocumentQA agent.
Tests the agent's ability to answer questions based on document retrieval from ChromaDB.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

# Ensure this script can import from the agent_rag_system package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Import agent components
from GS.agents_rag_system.config.config import RAGConfig, AgentConfig, LLMConfig
from GS.agents_rag_system.db.chroma.vectorstore import ChromaVectorStore
from GS.agents_rag_system.agents.examples.document_qa.agent import DocumentQAAgent


def test_document_qa_agent():
    """
    Test the DocumentQA agent functionality.
    This tests the agent's ability to retrieve relevant documents and answer questions based on them.
    """
    print("=" * 80)
    print("TESTING DOCUMENT QA AGENT")
    print("=" * 80)

    # Verify required environment variables
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        print(f"❌ Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your .env file or environment")
        sys.exit(1)

    # 1. Setup agent configuration
    print("\n1. Setting up agent configuration...")

    # Generate a unique collection name for this test
    collection_name = f"test_docqa_{uuid.uuid4().hex[:8]}"

    # Determine which ChromaDB client to use (HTTP or local)
    use_http_client = os.environ.get("CHROMA_HOST") is not None

    rag_config = None
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

    # Create LLMConfig
    llm_config = LLMConfig(
        provider="openai",  # Must match the LLMProviderType literal
        model_name="gpt-3.5-turbo",
        api_key=os.environ.get("OPENAI_API_KEY"),
        temperature=0.3,
        max_tokens=800,
        top_p=1.0,
        additional_params={}
    )

    # Create agent configuration with the correct prompt template keys and parameter names
    # Based on DocumentQAAgent implementation:
    # - process_query uses 'user_question' in QUERY_PROMPT
    # - chat method doesn't pass any parameters to CHAT_PROMPT
    agent_config = AgentConfig(
        name="DocumentQAAgentTest",
        description="Document QA agent for testing purposes",
        llm_config=llm_config,
        rag_config=rag_config,
        prompt_templates={
            "QUERY_PROMPT": "Please answer the following question based on the provided documents: {user_question}",
            "CHAT_PROMPT": "You are a helpful assistant that answers questions based on document context. Please be concise and accurate.",
            "SYSTEM_PROMPT": "You are a document QA assistant. Please analyze the documents and provide relevant information."
        }
    )

    # 2. Initialize the DocumentQA agent
    print("\n2. Initializing DocumentQA agent...")
    try:
        agent = DocumentQAAgent(config=agent_config)
        print("✅ DocumentQA agent initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing DocumentQA agent: {e}")
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

    # 4. Add documents to the agent's vector store
    print("\n4. Adding documents to vector store...")
    try:
        vectorstore = ChromaVectorStore(config=rag_config)
        vectorstore.add_documents(test_documents)
        count = vectorstore.get_collection_count()
        agent.vectorstore = vectorstore  # Assign the vectorstore to the agent
        print(f"✅ Successfully added {count} documents to the vector store")
    except Exception as e:
        print(f"❌ Error adding documents: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 5. Test document retrieval and question answering
    print("\n5. Testing document retrieval and question answering...")

    test_queries = [
        "What is the capital of France?",
        "Tell me about landmarks in Germany",
        "What attractions can I visit in Rome?",
        "What museums are in Madrid?",
        "Tell me about Tokyo"
    ]

    for query in test_queries:
        print(f"\nQuery: '{query}'")
        try:
            answer = agent.process_query(query)
            print(f"✅ Answer: {answer}")
        except Exception as e:
            print(f"❌ Error during question answering: {e}")
            import traceback
            traceback.print_exc()

    # 6. Test chat functionality
    print("\n6. Testing chat functionality...")
    message = "Compare the attractions in Rome and Paris"
    print(f"Message: '{message}'")

    try:
        answer = agent.chat(message)
        print(f"✅ Chat response: {answer}")

        # Test a follow-up question
        follow_up = "Which city has more museums?"
        print(f"\nFollow-up: '{follow_up}'")
        answer = agent.chat(follow_up)
        print(f"✅ Follow-up response: {answer}")
    except Exception as e:
        print(f"❌ Error during chat: {e}")
        import traceback
        traceback.print_exc()

    # 7. Test getting document sources
    print("\n7. Testing get_document_sources...")
    try:
        sources = agent.get_document_sources()
        print(f"✅ Document sources: {sources}")
    except Exception as e:
        print(f"❌ Error getting document sources: {e}")
        import traceback
        traceback.print_exc()

    # 8. Clean up
    print("\n8. Cleaning up...")
    try:
        vectorstore.delete_collection()
        print(f"✅ Successfully deleted collection: {collection_name}")
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")

    print("\n" + "=" * 80)
    print("DOCUMENT QA AGENT TEST COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    test_document_qa_agent()