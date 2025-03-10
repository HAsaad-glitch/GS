#!/usr/bin/env python
"""
Script for running agents from the agents_rag_system package.
"""
import os
import sys
import argparse
from pathlib import Path

# Add the parent directory to the path if needed
current_dir = Path(__file__).parent.resolve()
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from GS.agents_rag_system.config.config import AgentConfig
from GS.agents_rag_system.agents.examples.customer_support.agent import CustomerSupportAgent
from GS.agents_rag_system.agents.examples.document_qa.agent import DocumentQAAgent
from GS.agents_rag_system.agents.examples.code_assistant.agent import CodeAssistantAgent
from GS.agents_rag_system.agents.examples.research_agent.agent import ResearchAgent
from GS.agents_rag_system.utils.init_utils import load_documents_from_directory

def main():
    """Main function for running agents."""
    parser = argparse.ArgumentParser(description="Multi-Agent RAG System")
    parser.add_argument(
        "--agent", type=str, choices=["customer_support", "document_qa", "code_assistant", "research"],
        required=True, help="Agent type to use."
    )
    parser.add_argument(
        "--config", type=str,
        help="Path to the agent configuration file."
    )
    parser.add_argument(
        "--docs", type=str,
        help="Path to the documentation directory."
    )
    parser.add_argument(
        "--query", type=str,
        help="Query to process."
    )
    parser.add_argument(
        "--chat", action="store_true",
        help="Start a chat session."
    )
    args = parser.parse_args()
    
    # Determine the agent class and default config path
    if args.agent == "customer_support":
        agent_class = CustomerSupportAgent
        default_config = current_dir / "agents/examples/customer_support/config.json"
    elif args.agent == "document_qa":
        agent_class = DocumentQAAgent
        default_config = current_dir / "agents/examples/document_qa/config.json"
    elif args.agent == "code_assistant":
        agent_class = CodeAssistantAgent
        default_config = current_dir / "agents/examples/code_assistant/config.json"
    elif args.agent == "research":
        agent_class = ResearchAgent
        default_config = current_dir / "agents/examples/research_agent/config.json"
    else:
        raise ValueError(f"Unknown agent type: {args.agent}")
    
    # Load the agent configuration
    config_path = args.config or default_config
    
    try:
        config = AgentConfig.from_file(config_path)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        print(f"Creating a default configuration for {args.agent}...")
        
        # Create a default configuration
        if args.agent == "customer_support":
            from GS.agents_rag_system.prompts.customer_support import SYSTEM_PROMPT, QUERY_PROMPT, CHAT_PROMPT
            config = AgentConfig(
                name="Customer Support Agent",
                description="An agent that helps customers with their inquiries based on company documentation.",
                llm_config={
                    "provider": "openai",
                    "model_name": "gpt-3.5-turbo",
                    "temperature": 0.3,
                    "max_tokens": 500,
                    "top_p": 1.0,
                    "additional_params": {}
                },
                rag_config={
                    "collection_name": "customer_support_kb",
                    "embedding_model": "sentence-transformers/all-mpnet-base-v2",
                    "chunk_size": 1000,
                    "chunk_overlap": 200,
                    "similarity_top_k": 5,
                    "persist_directory": "./chroma_db/customer_support",
                    "additional_params": {}
                },
                prompt_templates={
                    "SYSTEM_PROMPT": SYSTEM_PROMPT,
                    "QUERY_PROMPT": QUERY_PROMPT,
                    "CHAT_PROMPT": CHAT_PROMPT
                }
            )
        elif args.agent == "document_qa":
            from GS.agents_rag_system.prompts.document_qa import SYSTEM_PROMPT, QUERY_PROMPT, CHAT_PROMPT
            config = AgentConfig(
                name="Document QA Agent",
                description="An agent that answers questions about documents.",
                llm_config={
                    "provider": "openai",
                    "model_name": "gpt-3.5-turbo",
                    "temperature": 0.3,
                    "max_tokens": 500,
                    "top_p": 1.0,
                    "additional_params": {}
                },
                rag_config={
                    "collection_name": "document_qa_kb",
                    "embedding_model": "sentence-transformers/all-mpnet-base-v2",
                    "chunk_size": 1000,
                    "chunk_overlap": 200,
                    "similarity_top_k": 5,
                    "persist_directory": "./chroma_db/document_qa",
                    "additional_params": {}
                },
                prompt_templates={
                    "SYSTEM_PROMPT": SYSTEM_PROMPT,
                    "QUERY_PROMPT": QUERY_PROMPT,
                    "CHAT_PROMPT": CHAT_PROMPT
                }
            )
        elif args.agent == "code_assistant":
            from GS.agents_rag_system.prompts.code_assistant import SYSTEM_PROMPT, QUERY_PROMPT, CHAT_PROMPT
            config = AgentConfig(
                name="Code Assistant Agent",
                description="An agent that helps with coding problems and questions.",
                llm_config={
                    "provider": "openai",
                    "model_name": "gpt-3.5-turbo",
                    "temperature": 0.3,
                    "max_tokens": 500,
                    "top_p": 1.0,
                    "additional_params": {}
                },
                rag_config={
                    "collection_name": "code_assistant_kb",
                    "embedding_model": "sentence-transformers/all-mpnet-base-v2",
                    "chunk_size": 1000,
                    "chunk_overlap": 200,
                    "similarity_top_k": 5,
                    "persist_directory": "./chroma_db/code_assistant",
                    "additional_params": {}
                },
                prompt_templates={
                    "SYSTEM_PROMPT": SYSTEM_PROMPT,
                    "QUERY_PROMPT": QUERY_PROMPT,
                    "CHAT_PROMPT": CHAT_PROMPT
                }
            )
        elif args.agent == "research":
            from GS.agents_rag_system.prompts.research_agent import SYSTEM_PROMPT, QUERY_PROMPT, CHAT_PROMPT
            config = AgentConfig(
                name="Research Agent",
                description="An agent that helps with research questions.",
                llm_config={
                    "provider": "openai",
                    "model_name": "gpt-3.5-turbo",
                    "temperature": 0.3,
                    "max_tokens": 500,
                    "top_p": 1.0,
                    "additional_params": {}
                },
                rag_config={
                    "collection_name": "research_kb",
                    "embedding_model": "sentence-transformers/all-mpnet-base-v2",
                    "chunk_size": 1000,
                    "chunk_overlap": 200,
                    "similarity_top_k": 5,
                    "persist_directory": "./chroma_db/research",
                    "additional_params": {}
                },
                prompt_templates={
                    "SYSTEM_PROMPT": SYSTEM_PROMPT,
                    "QUERY_PROMPT": QUERY_PROMPT,
                    "CHAT_PROMPT": CHAT_PROMPT
                }
            )
    
    try:
        # Create the agent
        agent = agent_class(config)
        
        # Add documents to the agent's knowledge base
        if args.docs:
            docs_path = Path(args.docs)
            if docs_path.exists():
                print(f"Adding documents from {docs_path}...")
                count = load_documents_from_directory(agent, docs_path)
                print(f"Added {count} documents.")
            else:
                print(f"Documentation directory {docs_path} not found.")
        
        # Process a query or start a chat session
        if args.query:
            print("\nProcessing query:", args.query)
            response = agent.process_query(args.query)
            print("\nResponse:", response)
        elif args.chat:
            print(f"\nStarting chat session with {args.agent} agent. Type 'exit' to quit.")
            while True:
                try:
                    user_input = input("\nYou: ")
                    if user_input.lower() in ["exit", "quit", "bye"]:
                        print("Exiting chat session.")
                        break
                    
                    response = agent.chat(user_input)
                    print("\nAgent:", response)
                except KeyboardInterrupt:
                    print("\nExiting chat session.")
                    break
        else:
            print("Please provide a query or start a chat session.")
    except Exception as e:
        print(f"Error running agent: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 