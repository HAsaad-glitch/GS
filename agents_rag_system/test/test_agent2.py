#!/usr/bin/env python
"""
Test script for the CodeAssistantAgent.
Tests the agent's ability to process code-related queries, chat, analyze code, and generate code.
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
from GS.agents_rag_system.agents.examples.code_assistant.agent import CodeAssistantAgent


def test_code_assistant_agent():
    """
    Test the CodeAssistantAgent functionality.
    This tests the agent's ability to process code-related queries, chat, analyze code, and generate code.
    """
    print("=" * 80)
    print("TESTING CODE ASSISTANT AGENT")
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
    collection_name = f"test_code_assistant_{uuid.uuid4().hex[:8]}"

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

    # Default languages and frameworks
    languages = "Python, JavaScript, TypeScript, Java, C++, C#"
    frameworks = "React, Django, Flask, Spring, Node.js, Express.js"

    # Create agent configuration with the correct prompt template keys and parameter names
    agent_config = AgentConfig(
        name="CodeAssistantAgentTest",
        description="Code assistant agent for testing purposes",
        llm_config=llm_config,
        rag_config=rag_config,
        prompt_templates={
            "QUERY_PROMPT": "Please help with the following code-related question: {user_question}",
            "CHAT_PROMPT": "Programming languages: {languages}\nFrameworks: {frameworks}\nPlease assist with code-related questions.",
            "SYSTEM_PROMPT": "You are a code assistant for {languages} and {frameworks}. Please provide code examples and explanations."
        },
        additional_params={
            "languages": languages,
            "frameworks": frameworks
        }
    )

    # 2. Initialize the CodeAssistantAgent
    print("\n2. Initializing CodeAssistantAgent...")
    try:
        agent = CodeAssistantAgent(config=agent_config)
        print("✅ CodeAssistantAgent initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing CodeAssistantAgent: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 3. Test process_query functionality
    print("\n3. Testing process_query functionality...")
    query = "How do I implement a binary search in Python?"
    print(f"Query: '{query}'")

    try:
        response = agent.process_query(query)
        print("✅ process_query response:")
        print(response[:500] + "..." if len(response) > 500 else response)
    except Exception as e:
        print(f"❌ Error during process_query: {e}")
        import traceback
        traceback.print_exc()

    # 4. Test chat functionality
    print("\n4. Testing chat functionality...")
    message = "What's the difference between a list and a tuple in Python?"
    print(f"Message: '{message}'")

    try:
        response = agent.chat(message)
        print("✅ chat response:")
        print(response[:500] + "..." if len(response) > 500 else response)
    except Exception as e:
        print(f"❌ Error during chat: {e}")
        import traceback
        traceback.print_exc()

    # 5. Test analyze_code functionality
    print("\n5. Testing analyze_code functionality...")
    code_to_analyze = """
def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    else:
        result = [0, 1]
        for i in range(2, n):
            result.append(result[i-1] + result[i-2])
        return result

print(fibonacci(10))
"""

    print(f"Code to analyze length: {len(code_to_analyze)} characters")

    try:
        analysis = agent.analyze_code(code_to_analyze, language="Python")
        print("✅ Code analysis:")
        print(analysis[:500] + "..." if len(analysis) > 500 else analysis)
    except Exception as e:
        print(f"❌ Error during analyze_code: {e}")
        import traceback
        traceback.print_exc()

    # 6. Test generate_code functionality
    print("\n6. Testing generate_code functionality...")
    requirement = "Write a function to check if a string is a palindrome"
    print(f"Requirement: '{requirement}'")

    try:
        generated_code = agent.generate_code(requirement, language="Python")
        print("✅ Generated code:")
        print(generated_code[:500] + "..." if len(generated_code) > 500 else generated_code)
    except Exception as e:
        print(f"❌ Error during generate_code: {e}")
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
    print("CODE ASSISTANT AGENT TEST COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    test_code_assistant_agent()