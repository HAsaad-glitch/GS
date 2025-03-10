# Prompts Module

This directory contains prompt templates for different agent types in the Multi-Agent RAG System.

## Contents

- `code_assistant.py`: Default prompt templates for the Code Assistant agent
- `customer_support.py`: Default prompt templates for the Customer Support agent
- `document_qa.py`: Default prompt templates for the Document QA agent
- `research_agent.py`: Default prompt templates for the Research agent

## Usage

These prompt templates provide defaults that can be used when creating agents. You can import them and use them in your agent configuration:

```python
from GS.agents_rag_system.config.config import AgentConfig, LLMConfig, RAGConfig
from GS.agents_rag_system.prompts.document_qa import DOCUMENT_QA_PROMPTS

# Create configurations
llm_config = LLMConfig(...)
rag_config = RAGConfig(...)

# Use default prompts but customize as needed
prompts = DOCUMENT_QA_PROMPTS.copy()
prompts["QUERY_PROMPT"] = "Custom prompt for document QA: {user_question}"

# Create agent configuration
agent_config = AgentConfig(
    name="My Document QA Agent",
    description="Custom Document QA Agent",
    llm_config=llm_config,
    rag_config=rag_config,
    prompt_templates=prompts
)
```

## Customizing Prompts

When customizing prompts, make sure to maintain the expected parameters that the agent implementation requires. Each agent looks for specific parameters in the prompts:

### Document QA

- `QUERY_PROMPT`: Uses `{user_question}` parameter
- `CHAT_PROMPT`: No specific parameters

### Research Agent

- `QUERY_PROMPT`: Uses `{research_question}` parameter
- `CHAT_PROMPT`: Uses `{research_fields}` parameter
- `SYSTEM_PROMPT`: Uses `{research_fields}` parameter
- `SUMMARIZE_PROMPT`: Uses `{text}` parameter

### Code Assistant

- `QUERY_PROMPT`: Uses `{user_question}` parameter
- `CHAT_PROMPT`: Uses `{languages}` and `{frameworks}` parameters
- `SYSTEM_PROMPT`: Uses `{languages}` and `{frameworks}` parameters

### Customer Support

- `QUERY_PROMPT`: Uses `{customer_query}` parameter
- `CHAT_PROMPT`: Uses `{company_name}` and `{company_description}` parameters

## Prompt Design Best Practices

When designing custom prompts, follow these best practices:

1. **Be clear and specific**: Clearly state what you want the model to do
2. **Include role information**: Specify what role the model should take (e.g., "You are a customer support agent...")
3. **Provide context**: Include any necessary context about the task
4. **Specify format**: If you need a particular output format, specify it clearly
5. **Use placeholders consistently**: Use the expected placeholder names (`{parameter_name}`)

## Example Custom Prompt

Here's an example of a custom prompt for the Document QA agent:

```python
CUSTOM_DOCUMENT_QA_PROMPTS = {
    "QUERY_PROMPT": """
    You are a helpful assistant tasked with answering questions based on the provided documents.
    
    Question: {user_question}
    
    Please follow these guidelines:
    1. Answer only based on the context provided
    2. If the answer is not in the context, say so
    3. Provide specific references to document sources when possible
    4. Be concise and accurate
    
    Your answer:
    """
} 