# Agents Module

This directory contains the implementation of various agent types for the Multi-Agent RAG System.

## Contents

- `/base/`: Contains the base agent implementation that all specific agents extend
  - `agent.py`: Contains the `BaseAgent` abstract class
- `/examples/`: Contains example implementations of different agent types
  - `/customer_support/`: Customer support agent implementation
  - `/document_qa/`: Document Q&A agent implementation
  - `/code_assistant/`: Code assistance agent implementation
  - `/research_agent/`: Research agent implementation

## Usage

### Using Existing Agents

```python
from GS.agents_rag_system.config.config import AgentConfig, LLMConfig, RAGConfig
from GS.agents_rag_system.agents.examples.document_qa.agent import DocumentQAAgent

# Create necessary configurations (see config module README)
llm_config = LLMConfig(...)
rag_config = RAGConfig(...)

# Create agent configuration
agent_config = AgentConfig(
    name="My Document QA Agent",
    description="An agent that answers questions based on documents",
    llm_config=llm_config,
    rag_config=rag_config,
    prompt_templates={
        "QUERY_PROMPT": "Please answer the following question: {user_question}",
        "CHAT_PROMPT": "You are having a conversation...",
        "SYSTEM_PROMPT": "You are a helpful assistant..."
    }
)

# Create the agent
agent = DocumentQAAgent(config=agent_config)

# Use the agent to process a query
response = agent.process_query("What does document X say about topic Y?")
print(response)

# Or use the agent in chat mode
response = agent.chat("I have a question about document X")
print(response)
```

### Available Agent Types

1. **DocumentQAAgent**: Answers questions about documents in the knowledge base
   ```python
   from GS.agents_rag_system.agents.examples.document_qa.agent import DocumentQAAgent
   ```

2. **CustomerSupportAgent**: Provides customer support based on product information
   ```python
   from GS.agents_rag_system.agents.examples.customer_support.agent import CustomerSupportAgent
   ```

3. **CodeAssistantAgent**: Helps with coding tasks, explains code, and generates code
   ```python
   from GS.agents_rag_system.agents.examples.code_assistant.agent import CodeAssistantAgent
   ```

4. **ResearchAgent**: Conducts research on topics, summarizes papers, and finds related research
   ```python
   from GS.agents_rag_system.agents.examples.research_agent.agent import ResearchAgent
   ```

### Creating Custom Agents

To create a custom agent, extend the `BaseAgent` class and implement the required methods:

```python
from GS.agents_rag_system.agents.base.agent import BaseAgent
from GS.agents_rag_system.config.config import AgentConfig

class MyCustomAgent(BaseAgent):
    """Custom agent implementation."""
    
    def __init__(self, config: AgentConfig):
        """Initialize the custom agent."""
        super().__init__(config)
        
        # Add any custom initialization here
        self.custom_parameter = getattr(self.config, "custom_parameter", "default_value")
    
    def process_query(self, query: str) -> str:
        """
        Process a query and return a response.
        
        Args:
            query: User query.
            
        Returns:
            Response to the user.
        """
        return self.query_with_rag(
            query=query,
            prompt_key="QUERY_PROMPT",
            user_question=query  # This name must match what's in your prompt template
        )
    
    # Implement any additional methods your agent needs
```

### Important Notes for Developers

1. **Prompt Templates**: The `prompt_templates` dictionary in the agent configuration must include the keys that the agent implementation expects. Check the source code of the agent you're using to see which prompt templates it requires.

2. **Template Variables**: Make sure the variables in your prompt templates (e.g., `{user_question}`) match the parameter names that the agent passes when formatting the template.

3. **Adding to Conversation History**: The `chat` method typically adds user messages and responses to the conversation history. This allows the agent to maintain context across multiple interactions.

4. **Using RAG**: Most agents use the `query_with_rag` method from the `BaseAgent` class to retrieve relevant information and generate responses.

5. **Custom Parameters**: If your agent needs custom parameters, you should access them via `getattr(self.config, "parameter_name", default_value)` or through `self.config.additional_params["parameter_name"]`.

6. **Method Overriding**: When creating custom agents, you must implement the `process_query` method, but you can also override other methods from `BaseAgent` if needed. 