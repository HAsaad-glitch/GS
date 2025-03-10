# Code Assistant Agent

This directory contains the implementation of the Code Assistant Agent, which is designed to help with coding tasks, explain code, and generate code.

## Contents

- `agent.py`: Contains the `CodeAssistantAgent` class implementation

## Features

- Process code-related queries using RAG
- Chat-based interactions
- Analyze code and provide feedback
- Generate code based on requirements

## Required Prompt Templates

The CodeAssistantAgent requires these prompt templates in the configuration:

- `QUERY_PROMPT`: Template for processing code-related queries
- `CHAT_PROMPT`: Template for chat-based interactions
- `SYSTEM_PROMPT`: Template for generating code

## Usage Example

```python
from GS.agents_rag_system.config.config import AgentConfig, LLMConfig, RAGConfig
from GS.agents_rag_system.agents.examples.code_assistant.agent import CodeAssistantAgent

# Create configurations
llm_config = LLMConfig(
    provider="openai",
    model_name="gpt-3.5-turbo",
    api_key="your-api-key",
    temperature=0.3,
    max_tokens=1000
)

rag_config = RAGConfig(
    vectorstore_type="chroma",
    collection_name="code_examples",
    persist_directory="./chroma_db",
    embedding_model="sentence-transformers/all-mpnet-base-v2",
    similarity_top_k=3
)

# Define programming languages and frameworks the agent understands
languages = "Python, JavaScript, TypeScript, Java, C++, C#"
frameworks = "React, Django, Flask, Spring, Node.js, Express.js"

agent_config = AgentConfig(
    name="CodeAssistant",
    description="Code Assistant Agent",
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

# Create the agent
agent = CodeAssistantAgent(config=agent_config)

# Add code examples to the knowledge base
agent.add_document("./code_examples/python_examples.py")
agent.add_document("./code_examples/javascript_examples.js")

# Process a code-related query
response = agent.process_query("How do I implement a binary search in Python?")
print(response)

# Chat with the agent
response = agent.chat("What's the difference between a list and a tuple in Python?")
print(response)

# Analyze code
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
"""
analysis = agent.analyze_code(code_to_analyze, language="Python")
print(analysis)

# Generate code
code = agent.generate_code("Write a function to check if a string is a palindrome", language="Python")
print(code)
```

## Implementation Details for Developers

### Key Methods

1. **`process_query(query: str) -> str`**
   - Processes a code-related query using RAG
   - Returns a response that may include code examples and explanations

2. **`chat(message: str) -> str`**
   - Handles conversational interactions about code
   - Maintains conversation history for context

3. **`analyze_code(code: str, language: str = None) -> str`**
   - Analyzes a piece of code and provides feedback
   - The `language` parameter specifies the programming language of the code
   - If language is not specified, it attempts to detect the language

4. **`generate_code(requirement: str, language: str = None) -> str`**
   - Generates code based on requirements
   - The `language` parameter specifies the programming language to use
   - If language is not specified, it defaults to Python

### Parameter Names in Templates

Make sure your prompt templates use these parameter names:

- In `QUERY_PROMPT`: Use `{user_question}` for the user's question
- In `CHAT_PROMPT` and `SYSTEM_PROMPT`: Use `{languages}` and `{frameworks}` for the supported programming languages and frameworks

### Custom Configuration

The agent uses these parameters that should be provided in the configuration's `additional_params`:
- `languages`: A string listing the programming languages the agent specializes in
- `frameworks`: A string listing the frameworks the agent specializes in 