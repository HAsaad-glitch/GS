# Multi-Agent RAG System

A flexible and modular system for creating multiple agents with Retrieval Augmented Generation (RAG) capabilities.

## Features

- Support for multiple LLM providers (OpenAI, Anthropic/Claude, DeepSeek)
- RAG implementation using ChromaDB for each agent
- Modular design to avoid code duplication
- Configurable agent behaviors

## Directory Structure

```
/agents_rag_system/
  /agents/                # Directory for agent implementations
    /base/                # Base classes for agents
    /examples/            # Example agents
      /customer_support/  # Customer support agent
      /document_qa/       # Document Q&A agent
      /code_assistant/    # Code assistance agent
      /research_agent/    # Research agent
  /config/                # Configuration files
  /llm/                   # LLM provider interfaces
    /openai/              # OpenAI specific implementation
    /anthropic/           # Anthropic/Claude specific implementation
    /deepseek/            # DeepSeek specific implementation
  /db/                    # Database related code
    /chroma/              # ChromaDB specific implementation
  /prompts/               # Directory for prompts
  /utils/                 # Utility functions
  /rag/                   # RAG implementation
```

## Installation

```bash
# Install the package
pip install -e .
```

## Usage

### Running an Example Agent

```bash
# Run a customer support agent in chat mode
python -m agents_rag_system.run_agent --agent customer_support --chat

# Run a document QA agent with a specific query
python -m agents_rag_system.run_agent --agent document_qa --query "What does this document say about X?"

# Run a code assistant agent with documents from a specific directory
python -m agents_rag_system.run_agent --agent code_assistant --docs ./code_docs --chat

# Run a research agent with a specific configuration file
python -m agents_rag_system.run_agent --agent research --config ./my_config.json --query "What are the latest developments in AI?"
```

### Using the Agents in Your Code

```python
from GS.agents_rag_system.config.config import AgentConfig
from GS.agents_rag_system.agents.examples.customer_support.agent import CustomerSupportAgent

# Create a configuration
config = AgentConfig(
    name="My Customer Support Agent",
    description="A custom customer support agent",
    llm_config={
        "provider": "openai",
        "model_name": "gpt-3.5-turbo",
        "temperature": 0.3,
        "max_tokens": 500,
        "top_p": 1.0,
        "additional_params": {}
    },
    rag_config={
        "collection_name": "my_kb",
        "embedding_model": "sentence-transformers/all-mpnet-base-v2",
        "chunk_size": 1000,
        "chunk_overlap": 200,
        "similarity_top_k": 5,
        "persist_directory": "./chroma_db/my_agent",
        "additional_params": {}
    },
    prompt_templates={
        "SYSTEM_PROMPT": "You are a helpful assistant...",
        "QUERY_PROMPT": "Please answer the following question: {customer_query}",
        "CHAT_PROMPT": "You are helping a customer..."
    }
)

# Create the agent
agent = CustomerSupportAgent(config)

# Add documents to the agent's knowledge base
agent.add_document("./docs/faq.pdf")
agent.add_document("./docs/product_manual.pdf")

# Process a query
response = agent.process_query("How do I reset my password?")
print(response)

# Or chat with the agent
response = agent.chat("I'm having trouble logging in.")
print(response)
```

## Creating a New Agent

To create a new agent, extend the `BaseAgent` class and implement the required methods:

```python
from GS.agents_rag_system.agents.base.agent import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config)
        # Add any custom initialization here
    
    def process_query(self, query: str) -> str:
        # Implement your query processing logic here
        return self.query_with_rag(
            query=query,
            prompt_key="QUERY_PROMPT",
            custom_parameter=query
        )
```

## License

MIT 