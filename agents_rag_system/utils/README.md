# Utilities Module

This directory contains utility functions used throughout the Multi-Agent RAG System.

## Contents

- `init_utils.py`: Utility functions for initializing agents and configurations

## Initialization Utilities

The `init_utils.py` file provides functions to help with initializing agents and configurations from files or command-line arguments:

```python
from GS.agents_rag_system.utils.init_utils import (
    load_config_from_file,
    create_agent_from_args,
    parse_args
)

# Load configuration from a JSON or YAML file
config = load_config_from_file("path/to/config.json")

# Parse command-line arguments
args = parse_args()

# Create an agent based on command-line arguments
agent = create_agent_from_args(args)
```

## Command-Line Arguments

The `parse_args` function in `init_utils.py` sets up the following command-line arguments:

- `--agent`: Type of agent to create (choices: "document_qa", "customer_support", "code_assistant", "research")
- `--config`: Path to a configuration file (JSON or YAML)
- `--query`: A query to process (for one-off queries)
- `--chat`: Flag to start in chat mode
- `--docs`: Path to documents to add to the agent's knowledge base

## Loading Configurations

The `load_config_from_file` function supports loading configurations from JSON and YAML files:

```python
# JSON example
config = load_config_from_file("config.json")

# YAML example
config = load_config_from_file("config.yaml")
```

The configuration file should have the following structure:

```json
{
  "agent": {
    "name": "My Agent",
    "description": "Description of my agent",
    "prompt_templates": {
      "QUERY_PROMPT": "Please answer the following question: {user_question}",
      "CHAT_PROMPT": "You are having a conversation..."
    }
  },
  "llm": {
    "provider": "openai",
    "model_name": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 1000
  },
  "rag": {
    "vectorstore_type": "chroma",
    "collection_name": "my_collection",
    "persist_directory": "./chroma_db",
    "embedding_model": "sentence-transformers/all-mpnet-base-v2",
    "similarity_top_k": 3
  }
}
```

## Creating Agents

The `create_agent_from_args` function creates an agent based on command-line arguments:

```python
# Parse arguments
args = parse_args()

# Create agent
agent = create_agent_from_args(args)

# Use the agent
if args.query:
    response = agent.process_query(args.query)
    print(response)
elif args.chat:
    # Start chat mode
    while True:
        message = input("You: ")
        if message.lower() in ["exit", "quit", "bye"]:
            break
        response = agent.chat(message)
        print(f"Agent: {response}")
```

## Notes for  Developers

1. **Configuration Files**: Use configuration files for complex setups to avoid hardcoding parameters.

2. **Command-Line Arguments**: The parsing of command-line arguments in `init_utils.py` provides a convenient way to create and run agents from the command line.

3. **Adding New Utilities**: If you add new utility functions, make sure they are well-documented and have clear input/output contracts.

4. **Error Handling**: The utility functions include basic error handling, but you might want to add more specific error handling for your use case. 