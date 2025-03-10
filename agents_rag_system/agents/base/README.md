# Base Agent Module

This directory contains the base implementation for all agents in the Multi-Agent RAG System.

## Contents

- `agent.py`: Contains the `BaseAgent` abstract class which all agent implementations extend

## Base Agent Abstract Class

The `BaseAgent` class provides common functionality that all agents need:

1. **Document Management**: Methods for adding documents to the agent's knowledge base
2. **Conversation History**: Management of conversation history for chat-based interactions
3. **Prompt Formatting**: Utilities for formatting prompts with variables
4. **RAG Integration**: Methods for using RAG (Retrieval Augmented Generation) in queries

## Key Methods

### Document Management

```python
# Add a document from a file
agent.add_document("path/to/document.pdf")

# Add raw text with metadata
agent.add_text("This is some information", {"source": "manual", "topic": "example"})

# Clear the knowledge base
agent.clear_knowledge_base()
```

### Conversation History

```python
# Add a message to the conversation history
agent.add_to_conversation("user", "Hello, how can you help me?")
agent.add_to_conversation("assistant", "I can help you with your questions.")

# Get the current conversation history
history = agent.get_conversation_history()

# Clear the conversation history
agent.clear_conversation_history()
```

### Prompt Formatting

```python
# Format a prompt template with variables
formatted_prompt = agent.get_formatted_prompt(
    prompt_key="QUERY_PROMPT", 
    user_question="What is RAG?"
)
```

### RAG Integration

```python
# Process a query using RAG
response = agent.query_with_rag(
    query="What is a transformer model?",
    prompt_key="QUERY_PROMPT",
    user_question="What is a transformer model?"
)
```

### Chat-Based Interaction

```python
# Process a query in the context of a conversation
response = agent.query_with_conversation("Tell me more about transformer models")
```

## Implementation Notes for Developers

1. **Abstract Methods**: The `process_query` method is marked as abstract and must be implemented by all derived classes.

2. **Configuration Access**: The class stores the configuration as `self.config` and initializes RAG and LLM components based on it.

3. **Prompt Template Keys**: The class expects certain prompt templates to be defined in the configuration. Make sure your agent implementation uses the same keys it's looking for.

4. **Error Handling**: The base implementation includes some error handling, but derived classes should add appropriate error handling for their specific features.

5. **Extending the Base**: When creating a new agent type:
   - Subclass `BaseAgent`
   - Call `super().__init__(config)` in your `__init__` method
   - Implement the `process_query` method
   - Add any additional methods specific to your agent type

## Example Extension

```python
from GS.agents_rag_system.agents.base.agent import BaseAgent
from GS.agents_rag_system.config.config import AgentConfig

class SimpleQAAgent(BaseAgent):
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        # Any additional initialization
    
    def process_query(self, query: str) -> str:
        # Implementation of the abstract method
        return self.query_with_rag(
            query=query, 
            prompt_key="QUERY_PROMPT", 
            user_question=query
        )
    
    # Additional methods specific to this agent type
``` 