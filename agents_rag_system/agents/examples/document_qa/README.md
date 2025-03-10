# Document QA Agent

This directory contains the implementation of the Document QA agent, which is designed to answer questions based on documents in its knowledge base.

## Contents

- `agent.py`: Contains the `DocumentQAAgent` class implementation

## Features

- Question answering based on document content
- Chat-based interactions
- Retrieval of document sources

## Required Prompt Templates

The DocumentQAAgent requires these prompt templates in the configuration:

- `QUERY_PROMPT`: Template for processing standalone questions
- `CHAT_PROMPT`: Template for chat-based interactions

## Usage Example

```python
from GS.agents_rag_system.config.config import AgentConfig, LLMConfig, RAGConfig
from GS.agents_rag_system.agents.examples.document_qa.agent import DocumentQAAgent

# Create configurations
llm_config = LLMConfig(
    provider="openai",
    model_name="gpt-3.5-turbo",
    api_key="your-api-key",
    temperature=0.3,
    max_tokens=800
)

rag_config = RAGConfig(
    vectorstore_type="chroma",
    collection_name="my_docs",
    persist_directory="./chroma_db",
    embedding_model="sentence-transformers/all-mpnet-base-v2",
    similarity_top_k=3
)

agent_config = AgentConfig(
    name="DocQA",
    description="Document QA Agent",
    llm_config=llm_config,
    rag_config=rag_config,
    prompt_templates={
        "QUERY_PROMPT": "Please answer the following question based on the provided documents: {user_question}",
        "CHAT_PROMPT": "You are a helpful assistant that answers questions based on document context."
    }
)

# Create the agent
agent = DocumentQAAgent(config=agent_config)

# Add documents to the knowledge base
agent.add_document("./documents/report.pdf")
agent.add_document("./documents/manual.docx")

# Ask a question
answer = agent.process_query("What does the report say about quarterly earnings?")
print(answer)

# Chat with the agent
response = agent.chat("Can you summarize the key points in the manual?")
print(response)

# Get document sources
sources = agent.get_document_sources()
print(f"Available document sources: {sources}")
```

## Implementation Details for  Developers

### Key Methods

1. **`process_query(query: str) -> str`**
   - Processes a standalone query using RAG
   - The query is used to retrieve relevant documents
   - Returns a response based on the documents

2. **`chat(message: str) -> str`**
   - Processes a message in the context of a conversation
   - Adds the message to the conversation history
   - Uses the conversation context to retrieve relevant documents
   - Returns a response

3. **`get_document_sources() -> List[str]`**
   - Returns a list of unique document sources in the knowledge base
   - This can be useful for showing users what documents are available

### Parameter Names in Templates

Make sure your prompt templates use these parameter names:

- In `QUERY_PROMPT`: Use `{user_question}` for the user's question

### Error Handling

The methods include basic error handling, but you should add additional error handling when using this agent in production applications. 