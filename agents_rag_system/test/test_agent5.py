#!/usr/bin/env python
"""
Test script for the WebScrapingAnalysisAgent.
Tests the agent's capabilities for analyzing websites for scraping, detecting anti-scraping measures,
and recommending appropriate scraping strategies.
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

# Import agent components
from GS.agents_rag_system.config.config import RAGConfig, AgentConfig, LLMConfig
from GS.agents_rag_system.db.chroma.vectorstore import ChromaVectorStore
from GS.agents_rag_system.agents.examples.web_scraping_analysis.agent import WebScrapingAnalysisAgent

# Target website for testing
TARGET_WEBSITE = "https://naicslist.com"


def test_web_scraping_analysis_agent():
    """
    Test the WebScrapingAnalysisAgent functionality.
    This tests the agent's analysis, detection, and recommendation capabilities for web scraping.
    """
    print("=" * 80)
    print(f"TESTING WEB SCRAPING ANALYSIS AGENT ON {TARGET_WEBSITE}")
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
    collection_name = f"test_web_scraping_{uuid.uuid4().hex[:8]}"
    print(f"Collection name: {collection_name}")

    # Determine which ChromaDB client to use (HTTP or local)
    use_http_client = os.environ.get("CHROMA_HOST") is not None

    # Setup RAG configuration
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

    # Setup LLM configuration
    llm_config = LLMConfig(
        provider="openai",
        model_name="gpt-4"
    )

    # Create agent configuration
    agent_config = AgentConfig(
        name="WebScrapingAgentTest",
        description="Web scraping analysis agent for testing purposes",
        llm_config=llm_config,
        rag_config=rag_config,
        prompt_templates={
            "QUERY_PROMPT": "Please help with the following web scraping question: {user_question}",
            "CHAT_PROMPT": "You are a web scraping expert assistant having a conversation with a user. Use proxies: {use_proxies} Detect CAPTCHA: {detect_captcha}",
            "ANALYSIS_PROMPT": "I need to analyze the website at {url} for web scraping. What aspects should I focus on?",
            "RECOMMENDATION_PROMPT": "Based on this website analysis: {analysis} What are the most effective web scraping techniques?",
            "STRATEGY_PROMPT": "Create a detailed web scraping strategy for {url}. Analysis: {analysis} Recommendations: {recommendations}",
            "SYSTEM_PROMPT": "You are a web scraping analysis assistant specialized in determining the best scraping approaches for different websites."
        },
        use_proxies=True,
        detect_captcha=True
    )

    # 2. Initialize the WebScrapingAnalysisAgent
    print("\n2. Initializing WebScrapingAnalysisAgent...")
    try:
        agent = WebScrapingAnalysisAgent(config=agent_config)
        print("✅ WebScrapingAnalysisAgent initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing WebScrapingAnalysisAgent: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 3. Test analyze_website functionality
    print("\n3. Testing analyze_website functionality...")
    print(f"Analyzing website: {TARGET_WEBSITE}")

    try:
        analysis_result = agent.analyze_website(TARGET_WEBSITE)
        print("✅ Website analysis complete")

        # Print key analysis findings
        print("\nKey analysis findings:")
        for key, value in analysis_result.items():
            if key not in ["headers", "llm_analysis"]:
                print(f"- {key}: {value}")

        # Print a snippet of the LLM analysis
        if "llm_analysis" in analysis_result:
            llm_analysis = analysis_result["llm_analysis"]
            print(f"\nLLM Analysis (excerpt):")
            print(llm_analysis[:300] + "..." if len(llm_analysis) > 300 else llm_analysis)
    except Exception as e:
        print(f"❌ Error during website analysis: {e}")
        import traceback
        traceback.print_exc()
        analysis_result = {"error": str(e)}

    # 4. Test detect_proxy_and_captcha functionality
    print("\n4. Testing detect_proxy_and_captcha functionality...")

    try:
        detection_result = agent.detect_proxy_and_captcha(TARGET_WEBSITE)
        print("✅ Proxy and CAPTCHA detection complete")

        # Print detection results
        print("\nDetection results:")
        print(f"- Proxy needed: {detection_result.get('proxy_needed', False)}")
        print(f"- CAPTCHA present: {detection_result.get('captcha_present', False)}")
        print(f"- CAPTCHA type: {detection_result.get('captcha_type', 'None')}")
        if "reason" in detection_result:
            print(f"- Reason: {detection_result['reason']}")
    except Exception as e:
        print(f"❌ Error during proxy and CAPTCHA detection: {e}")
        import traceback
        traceback.print_exc()
        detection_result = {"error": str(e)}

    # 5. Test extract_website_tree functionality
    print("\n5. Testing extract_website_tree functionality...")

    try:
        tree_result = agent.extract_website_tree(TARGET_WEBSITE)
        print("✅ Website tree extraction complete")

        # Print tree excerpt
        tree_excerpt = tree_result.split("\n\nTree Summary:")[0]
        print("\nWebsite tree (excerpt):")
        print(tree_excerpt[:200] + "..." if len(tree_excerpt) > 200 else tree_excerpt)

        # Print tree summary
        if "Tree Summary:" in tree_result:
            tree_summary = tree_result.split("\n\nTree Summary:")[1]
            print("\nTree Summary:")
            print(tree_summary[:300] + "..." if len(tree_summary) > 300 else tree_summary)
    except Exception as e:
        print(f"❌ Error during website tree extraction: {e}")
        import traceback
        traceback.print_exc()
        tree_result = f"<e>{str(e)}</e>"

    # 6. Test recommend_scraping_techniques functionality
    print("\n6. Testing recommend_scraping_techniques functionality...")

    try:
        # Combine analysis results
        combined_analysis = {**analysis_result, **detection_result}

        recommendations = agent.recommend_scraping_techniques(combined_analysis)
        print("✅ Scraping technique recommendations complete")

        # Print recommendations
        print("\nRecommended techniques:")
        for i, technique in enumerate(recommendations, 1):
            print(f"{i}. {technique}")
    except Exception as e:
        print(f"❌ Error during scraping technique recommendations: {e}")
        import traceback
        traceback.print_exc()
        recommendations = [f"Error: {str(e)}"]

    # 7. Test process_website functionality (end-to-end test)
    print("\n7. Testing process_website functionality (end-to-end)...")

    try:
        process_result = agent.process_website(TARGET_WEBSITE)
        print("✅ End-to-end website processing complete")

        # Print process results
        print("\nProcess results summary:")
        print(f"- Analysis completed: {'analysis' in process_result and 'error' not in process_result['analysis']}")
        print(f"- Proxy/CAPTCHA detection: {'proxy_captcha_info' in process_result}")
        print(f"- Website tree extracted: {'website_tree_summary' in process_result}")
        print(f"- Recommendations provided: {'recommendations' in process_result}")
        print(f"- Scraping strategy generated: {'scraping_strategy' in process_result}")

        # Print scraping strategy excerpt
        if "scraping_strategy" in process_result:
            strategy = process_result["scraping_strategy"]
            print("\nScraping strategy (excerpt):")
            print(strategy[:500] + "..." if len(strategy) > 500 else strategy)
    except Exception as e:
        print(f"❌ Error during end-to-end website processing: {e}")
        import traceback
        traceback.print_exc()
        process_result = {"error": str(e)}

    # 8. Test chat functionality
    print("\n8. Testing chat functionality...")

    try:
        chat_message = "How can I scrape company data from naicslist.com effectively?"
        print(f"Chat message: '{chat_message}'")

        chat_response = agent.chat(chat_message)
        print("✅ Chat response received")

        # Print chat response
        print("\nChat response:")
        print(chat_response[:500] + "..." if len(chat_response) > 500 else chat_response)
    except Exception as e:
        print(f"❌ Error during chat: {e}")
        import traceback
        traceback.print_exc()
        chat_response = f"Error: {str(e)}"

    # 9. Test process_query functionality
    print("\n9. Testing process_query functionality...")

    try:
        query = "What are the best techniques for dealing with CAPTCHAs on naicslist.com?"
        print(f"Query: '{query}'")

        query_response = agent.process_query(query)
        print("✅ Query response received")

        # Print query response
        print("\nQuery response:")
        print(query_response[:500] + "..." if len(query_response) > 500 else query_response)
    except Exception as e:
        print(f"❌ Error during query processing: {e}")
        import traceback
        traceback.print_exc()
        query_response = f"Error: {str(e)}"

    # 10. Clean up
    print("\n10. Cleaning up...")
    try:
        # Get the vectorstore from the agent's RAG component
        if hasattr(agent, 'rag') and hasattr(agent.rag, 'vectorstore'):
            agent.rag.vectorstore.delete_collection()
            print(f"✅ Successfully deleted collection: {collection_name}")
    except Exception as e:
        print(f"❌ Error deleting collection: {e}")
        import traceback
        traceback.print_exc()

    # Final summary
    print("\n" + "=" * 80)
    print("WEB SCRAPING ANALYSIS AGENT TEST SUMMARY")
    print("=" * 80)

    test_results = {
        "Website Analysis": "analysis" in analysis_result and "error" not in analysis_result,
        "Proxy/CAPTCHA Detection": "proxy_needed" in detection_result,
        "Website Tree Extraction": "Tree Summary:" in tree_result,
        "Scraping Recommendations": len(recommendations) > 0 and not any("Error" in r for r in recommendations),
        "End-to-End Processing": "error" not in process_result,
        "Chat Functionality": "Error" not in chat_response,
        "Query Processing": "Error" not in query_response
    }

    passed = sum(1 for result in test_results.values() if result)
    total = len(test_results)

    for test, passed_test in test_results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"{status} - {test}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("\n✅ All tests passed successfully!")
        return 0
    else:
        print(f"\n❌ Some tests failed: {total - passed} failures")
        return 1


if __name__ == "__main__":
    exit_code = test_web_scraping_analysis_agent()
    sys.exit(exit_code)