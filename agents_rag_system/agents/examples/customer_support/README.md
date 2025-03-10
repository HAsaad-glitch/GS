# Customer Support Agent

This directory contains the implementation of the Customer Support Agent, which is designed to provide customer support based on a knowledge base of product information, policies, and FAQs.

## Contents

- `agent.py`: Contains the `CustomerSupportAgent` class implementation

## Features

- Process customer queries using RAG
- Chat-based interactions
- Context-aware responses based on conversation history

## Required Prompt Templates

The CustomerSupportAgent requires these prompt templates in the configuration:

- `QUERY_PROMPT`: Template for processing standalone customer queries
- `CHAT_PROMPT`: Template for chat-based interactions

## Usage Example

```python
from GS.agents_rag_system.config.config import AgentConfig, LLMConfig, RAGConfig
from GS.agents_rag_system.agents.examples.customer_support.agent import CustomerSupportAgent

# Create configurations
llm_config = LLMConfig(
    provider="openai",
    model_name="gpt-3.5-turbo",
    api_key="your-api-key",
    temperature=0.5,
    max_tokens=800
)

rag_config = RAGConfig(
    vectorstore_type="chroma",
    collection_name="customer_support_kb",
    persist_directory="./chroma_db",
    embedding_model="sentence-transformers/all-mpnet-base-v2",
    similarity_top_k=3
)

# Define company information
company_name = "Acme Corporation"
company_description = "A leading provider of technology solutions for businesses of all sizes."

agent_config = AgentConfig(
    name="CustomerSupport",
    description="Customer Support Agent",
    llm_config=llm_config,
    rag_config=rag_config,
    prompt_templates={
        "QUERY_PROMPT": "Please help with the following customer query: {customer_query}",
        "CHAT_PROMPT": "Company: {company_name}\nDescription: {company_description}\nPlease provide helpful customer support."
    },
    additional_params={
        "company_name": company_name,
        "company_description": company_description
    }
)

# Create the agent
agent = CustomerSupportAgent(config=agent_config)

# Add knowledge base documents
agent.add_document("./support_docs/faq.pdf")
agent.add_document("./support_docs/product_manual.pdf")
agent.add_document("./support_docs/return_policy.txt")

# Process a customer query
response = agent.process_query("What is your return policy?")
print(response)

# Chat with the agent
response = agent.chat("I'm having trouble with my product.")
print(response)

# Continue the conversation
response = agent.chat("It won't turn on. I've tried charging it.")
print(response)
```

## Implementation Details for  Developers

### Key Methods

1. **`process_query(query: str) -> str`**
   - Processes a standalone customer query using RAG
   - Returns a response based on the knowledge base

2. **`chat(message: str) -> str`**
   - Handles conversational interactions with customers
   - Maintains conversation history for context
   - Uses the conversation context to provide more helpful responses

### Parameter Names in Templates

Make sure your prompt templates use these parameter names:

- In `QUERY_PROMPT`: Use `{customer_query}` for the customer's query
- In `CHAT_PROMPT`: Use `{company_name}` and `{company_description}` for the company information

### Custom Configuration

The agent uses these parameters that should be provided in the configuration's `additional_params`:
- `company_name`: The name of the company
- `company_description`: A brief description of the company's business

### Knowledge Base Organization

For best results, organize your knowledge base with appropriate metadata:

```python
agent.add_text(
    "Our standard return policy allows returns within 30 days of purchase.",
    metadata={"category": "policy", "subcategory": "returns"}
)

agent.add_text(
    "Product A features include 8GB RAM and 256GB storage.",
    metadata={"category": "product", "product_id": "A123", "name": "Product A"}
)
```

This will help the RAG system retrieve the most relevant information for each query. 