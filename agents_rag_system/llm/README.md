# LLM Module

This directory contains the implementation of different Language Model (LLM) providers for the Multi-Agent RAG System.

## Contents

- `base.py`: Contains the `BaseLLM` abstract class that all provider implementations must extend
- `factory.py`: Provides a factory function to create LLM instances based on configuration
- `/anthropic/`: Implementation for Anthropic Claude models
- `/deepseek/`: Implementation for DeepSeek models
- `/openai/`: Implementation for OpenAI models (GPT-3.5, GPT-4, etc.)

## Usage

### Creating an LLM Instance

The recommended way to create an LLM instance is using the factory:

```python
from GS.agents_rag_system.config.config import LLMConfig
from GS.agents_rag_system.llm.factory import create_llm

# Create a configuration for an OpenAI model
llm_config = LLMConfig(
    provider="openai",  # Supported: "openai", "anthropic", "deepseek"
    model_name="gpt-3.5-turbo",
    api_key="your-api-key-here",  # Better to use environment variables
    temperature=0.7,
    max_tokens=1000,
    top_p=1.0,
    additional_params={}
)

# Create the LLM instance
llm = create_llm(llm_config)

# Generate text with the LLM
response = llm.generate("What is the capital of France?")
print(response)

# For chat-based models, you can use chat history
chat_history = [
    {"role": "user", "content": "Hello, who are you?"},
    {"role": "assistant", "content": "I'm an AI assistant. How can I help you?"}
]

response = llm.generate_with_chat_history(chat_history)
print(response)
```

### Using a Specific Provider Directly

If needed, you can also create provider-specific LLM instances directly:

```python
from GS.agents_rag_system.llm.openai.llm import OpenAILLM

openai_llm = OpenAILLM(
    model_name="gpt-4",
    api_key="your-openai-api-key",
    temperature=0.5,
    max_tokens=2000
)

response = openai_llm.generate("Explain quantum computing in simple terms.")
```

### Important Notes for  Developers

1. **API Keys**: Don't hardcode API keys in your code. Use environment variables or secure key management. The implementation will automatically look for:
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY`
   - `DEEPSEEK_API_KEY`

2. **Model Selection**: 
   - For OpenAI: Models like "gpt-3.5-turbo" and "gpt-4" work well
   - For Anthropic: Use "claude-2" or "claude-instant"
   - For DeepSeek: Use "deepseek-chat"

3. **Error Handling**: The implementations include error handling for common issues like rate limits, but you should still handle exceptions when using these classes.

4. **Token Usage**: Be aware of token usage and limits. The `max_tokens` parameter sets the maximum number of tokens in the response, not in the total exchange.

5. **Creating Custom Providers**: If you need to add a new LLM provider:
   1. Create a new directory for the provider
   2. Implement a class that extends `BaseLLM`
   3. Update the `create_llm` factory function in `factory.py` 