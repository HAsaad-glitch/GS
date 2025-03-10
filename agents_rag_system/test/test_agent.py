#!/usr/bin/env python
"""
Test script for the ResearchAgent.
Tests the agent's capabilities including querying, chatting, paper summarization, and research finding.
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
from GS.agents_rag_system.agents.examples.research_agent.agent import ResearchAgent


def test_research_agent():
    """
    Test the ResearchAgent functionality.
    This tests the research agent's ability to process queries, chat, summarize papers,
    and find related research.
    """
    print("=" * 80)
    print("TESTING RESEARCH AGENT")
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
    collection_name = f"test_research_{uuid.uuid4().hex[:8]}"

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
        temperature=0.7,
        max_tokens=1000,
        top_p=1.0,
        additional_params={}
    )

    # Finally create AgentConfig with the correct prompt template keys and parameter names
    agent_config = AgentConfig(
        name="ResearchAgentTest",
        description="Research agent for testing purposes",
        llm_config=llm_config,
        rag_config=rag_config,
        prompt_templates={
            "QUERY_PROMPT": "Please research the following topic: {research_question}",
            "CHAT_PROMPT": "Research fields: {research_fields}\nPlease respond helpfully based on your knowledge in these fields.",
            "SYSTEM_PROMPT": "You are a research assistant. Please find information related to: {research_fields}",
            "SUMMARIZE_PROMPT": "Please summarize the following paper: {text}"
        }
    )

    # 2. Initialize the research agent
    print("\n2. Initializing ResearchAgent...")
    try:
        agent = ResearchAgent(config=agent_config)
        print("✅ ResearchAgent initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing ResearchAgent: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 3. Test process_query functionality
    print("\n3. Testing process_query functionality...")
    query = "What are the latest advancements in natural language processing?"
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
    message = "Tell me about transformer models in NLP."
    print(f"Message: '{message}'")

    try:
        response = agent.chat(message)
        print("✅ chat response:")
        print(response[:500] + "..." if len(response) > 500 else response)
    except Exception as e:
        print(f"❌ Error during chat: {e}")
        import traceback
        traceback.print_exc()

    # 5. Test summarize_paper functionality
    print("\n5. Testing summarize_paper functionality...")

    # Sample paper text for summarization
    paper_text = """
    Attention Is All You Need

    Abstract:
    The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles, by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature.

    Introduction:
    Recurrent neural networks, long short-term memory and gated recurrent neural networks in particular, have been firmly established as state of the art approaches in sequence modeling and transduction problems such as language modeling and machine translation. Numerous efforts have been made to improve recurrent language models and encoder-decoder architectures.

    Recurrent models typically factor computation along the symbol positions of the input and output sequences. Aligning the positions to steps in computation time, they generate a sequence of hidden states ht, as a function of the previous hidden state ht-1 and the input for position t. This inherently sequential nature precludes parallelization within training examples, which becomes critical at longer sequence lengths, as memory constraints limit batching across examples. Recent work has achieved significant improvements in computational efficiency through factorization tricks and conditional computation, while also improving model performance in case of the latter. The fundamental constraint of sequential computation, however, remains.

    Attention mechanisms have become an integral part of compelling sequence modeling and transduction models in various tasks, allowing modeling of dependencies without regard to their distance in the input or output sequences. In all but a few cases, however, such attention mechanisms are used in conjunction with a recurrent network.

    In this work we propose the Transformer, a model architecture eschewing recurrence and instead relying entirely on an attention mechanism to draw global dependencies between input and output. The Transformer allows for significantly more parallelization and can reach a new state of the art in translation quality after being trained for as little as twelve hours on eight P100 GPUs.
    """

    print(f"Paper text length: {len(paper_text)} characters")

    try:
        summary = agent.summarize_paper(paper_text, max_length=300)
        print("✅ Paper summary:")
        print(summary)
    except Exception as e:
        print(f"❌ Error during summarize_paper: {e}")
        import traceback
        traceback.print_exc()

    # 6. Test find_related_research functionality
    print("\n6. Testing find_related_research functionality...")
    topic = "transformer models"
    print(f"Topic: '{topic}'")

    try:
        research = agent.find_related_research(topic, num_results=3)
        print("✅ Related research:")
        print(research)
    except Exception as e:
        print(f"❌ Error during find_related_research: {e}")
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
    print("RESEARCH AGENT TEST COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    test_research_agent()