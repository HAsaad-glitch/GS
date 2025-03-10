# Configuration Module

This directory contains configuration-related code for the Multi-Agent RAG System.

## Contents

- `config.py`: Contains configuration classes (`AgentConfig`, `LLMConfig`, `RAGConfig`) used throughout the system
- `api_keys.py`: Utility for managing API keys for different providers

## Usage

### AgentConfig

The `AgentConfig` class is the main configuration for creating agents:

```python
from GS.agents_rag_system.config.config import AgentConfig, LLMConfig, RAGConfig

# First create LLM configuration
llm_config = LLMConfig(
    provider="openai",  # Options: "openai", "anthropic", "deepseek"
    model_name="gpt-3.5-turbo", 
    api_key="your-api-key-or-from-env",
    temperature=0.7,
    max_tokens=1000,
    top_p=1.0,
    additional_params={}
)

# Create RAG configuration
rag_config = RAGConfig(
    vectorstore_type="chroma",
    collection_name="my_collection",
    persist_directory="./chroma_db",  # For local storage
    embedding_model="sentence-transformers/all-mpnet-base-v2",
    similarity_top_k=3,
    additional_params={
        "use_http_client": True,  # For HTTP connection to ChromaDB
        "chroma_host": "localhost",
        "chroma_port": 8000
    }
)

# Create the agent configuration
agent_config = AgentConfig(
    name="MyAgent",
    description="A description of what this agent does",
    llm_config=llm_config,
    rag_config=rag_config,
    prompt_templates={
        # These must match what the agent implementation expects!
        "QUERY_PROMPT": "Please answer this question: {user_question}",
        "CHAT_PROMPT": "You are having a conversation...",
        "SYSTEM_PROMPT": "You are a helpful assistant..."
    },
    additional_params={
        # Any extra parameters needed by specific agent types
        "company_name": "Acme Inc",
        "languages": "Python, JavaScript, Java"
    }
)
```

### Important Notes for  Developers

1. **Pydantic Models**: These configurations are Pydantic models, which means they validate their input. Make sure to provide all required fields.

2. **Additional Parameters**: Use the `additional_params` field to pass custom parameters needed by specific agent types. Don't try to set attributes directly on the config objects (they're Pydantic models and will raise errors).

3. **Prompt Templates**: Make sure the keys in the `prompt_templates` dictionary match what the agent implementation expects. For example, if an agent looks for "QUERY_PROMPT", you must use exactly that key.

4. **Parameter Names**: The variables used in prompt templates (like `{user_question}`) must match the parameter names the agent passes when formatting the templates.

## API Keys

The `api_keys.py` module provides utilities for managing API keys securely:

```python
from GS.agents_rag_system.config.api_keys import get_api_key

# Get API key for a provider (checks environment variables)
openai_key = get_api_key("openai")
```

API keys are first looked for in environment variables:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `DEEPSEEK_API_KEY`

For security, prefer setting these as environment variables rather than hardcoding them. 