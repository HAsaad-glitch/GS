#!/usr/bin/env python
"""
Test script for the CustomerSupportAgent.
Tests the agent's ability to process customer queries and chat with customers.
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
from GS.agents_rag_system.agents.examples.customer_support.agent import CustomerSupportAgent


def test_customer_support_agent():
    """
    Test the CustomerSupportAgent functionality.
    This tests the agent's ability to process customer queries and chat with customers.
    """
    print("=" * 80)
    print("TESTING CUSTOMER SUPPORT AGENT")
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
    collection_name = f"test_customer_support_{uuid.uuid4().hex[:8]}"

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
        temperature=0.5,
        max_tokens=800,
        top_p=1.0,
        additional_params={}
    )

    # Default company information
    company_name = "Acme Corporation"
    company_description = "A leading provider of technology solutions for businesses of all sizes."

    # Create agent configuration with the correct prompt template keys and parameter names
    agent_config = AgentConfig(
        name="CustomerSupportAgentTest",
        description="Customer support agent for testing purposes",
        llm_config=llm_config,
        rag_config=rag_config,
        prompt_templates={
            "QUERY_PROMPT": "Please help with the following customer query: {customer_query}",
            "CHAT_PROMPT": "Company: {company_name}\nDescription: {company_description}\nPlease provide helpful customer support."
        },
        additional_params={
            "company_name": company_name,
            "company_description": company_description
        }
    )

    # 2. Initialize the CustomerSupportAgent
    print("\n2. Initializing CustomerSupportAgent...")
    try:
        agent = CustomerSupportAgent(config=agent_config)
        print("✅ CustomerSupportAgent initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing CustomerSupportAgent: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Add sample customer support documents to the agent's knowledge base
    print("\n3. Adding sample knowledge base...")

    support_documents = [
        {
            "id": "doc_1",
            "text": "Product A is our flagship software solution designed for enterprise clients. It offers advanced analytics, reporting, and integration capabilities. Common issues include login problems and data synchronization. To resolve login issues, users should clear their browser cache and cookies.",
            "metadata": {"category": "product_info", "product": "Product A"}
        },
        {
            "id": "doc_2",
            "text": "Product B is our mobile application for iOS and Android. It allows users to access their accounts on the go. Common issues include notification problems and battery drain. To fix notification issues, users should check their device notification settings.",
            "metadata": {"category": "product_info", "product": "Product B"}
        },
        {
            "id": "doc_3",
            "text": "Our standard return policy allows customers to return products within 30 days of purchase with a receipt. Refunds are processed within 7-10 business days. For software subscriptions, we offer a 14-day money-back guarantee.",
            "metadata": {"category": "policies", "type": "returns"}
        },
        {
            "id": "doc_4",
            "text": "Customer support is available Monday through Friday from 9 AM to 5 PM Eastern Time. For urgent issues outside business hours, please use our emergency contact form on the website.",
            "metadata": {"category": "support", "type": "hours"}
        }
    ]

    # Create vectorstore and add documents
    try:
        vectorstore = ChromaVectorStore(config=rag_config)
        vectorstore.add_documents(support_documents)
        count = vectorstore.get_collection_count()
        agent.vectorstore = vectorstore  # Assign the vectorstore to the agent
        print(f"✅ Successfully added {count} documents to the knowledge base")
    except Exception as e:
        print(f"❌ Error adding documents: {e}")
        import traceback
        traceback.print_exc()

    # 4. Test process_query functionality
    print("\n4. Testing process_query functionality...")
    query = "What is your return policy?"
    print(f"Query: '{query}'")

    try:
        response = agent.process_query(query)
        print("✅ process_query response:")
        print(response[:500] + "..." if len(response) > 500 else response)
    except Exception as e:
        print(f"❌ Error during process_query: {e}")
        import traceback
        traceback.print_exc()

    # 5. Test chat functionality
    print("\n5. Testing chat functionality...")
    message = "I'm having trouble with Product A. I can't log in to my account."
    print(f"Message: '{message}'")

    try:
        response = agent.chat(message)
        print("✅ chat response:")
        print(response[:500] + "..." if len(response) > 500 else response)
    except Exception as e:
        print(f"❌ Error during chat: {e}")
        import traceback
        traceback.print_exc()

    # 6. Test multi-turn conversation
    print("\n6. Testing multi-turn conversation...")
    follow_up = "Is there anything else I should try?"
    print(f"Follow-up message: '{follow_up}'")

    try:
        response = agent.chat(follow_up)
        print("✅ follow-up response:")
        print(response[:500] + "..." if len(response) > 500 else response)
    except Exception as e:
        print(f"❌ Error during follow-up chat: {e}")
        import traceback
        traceback.print_exc()

    # 7. Clean up
    print("\n7. Cleaning up...")
    try:
        # If we have access to the vectorstore, clean it up
        if hasattr(agent, 'vectorstore'):
            agent.vectorstore.delete_collection()
            print(f"✅ Successfully deleted collection: {collection_name}")
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")

    print("\n" + "=" * 80)
    print("CUSTOMER SUPPORT AGENT TEST COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    test_customer_support_agent() 