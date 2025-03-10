# Research Agent

This directory contains the implementation of the Research Agent, which is designed to assist with research tasks, paper summarization, and finding related research.

## Contents

- `agent.py`: Contains the `ResearchAgent` class implementation

## Features

- Process research queries using RAG
- Chat-based interactions
- Summarize research papers
- Find related research on specific topics

## Required Prompt Templates

The ResearchAgent requires these prompt templates in the configuration:

- `QUERY_PROMPT`: Template for processing research queries
- `CHAT_PROMPT`: Template for chat-based interactions
- `SYSTEM_PROMPT`: Template for finding related research
- `SUMMARIZE_PROMPT`: Template for summarizing papers (optional)

## Usage Example

```python
from GS.agents_rag_system.config.config import AgentConfig, LLMConfig, RAGConfig
from GS.agents_rag_system.agents.examples.research_agent.agent import ResearchAgent

# Create configurations
llm_config = LLMConfig(
    provider="openai",
    model_name="gpt-3.5-turbo",
    api_key="your-api-key",
    temperature=0.7,
    max_tokens=1000
)

rag_config = RAGConfig(
    vectorstore_type="chroma",
    collection_name="research_papers",
    persist_directory="./chroma_db",
    embedding_model="sentence-transformers/all-mpnet-base-v2",
    similarity_top_k=5
)

agent_config = AgentConfig(
    name="ResearchAssistant",
    description="Research Assistant Agent",
    llm_config=llm_config,
    rag_config=rag_config,
    prompt_templates={
        "QUERY_PROMPT": "Please research the following topic: {research_question}",
        "CHAT_PROMPT": "Research fields: {research_fields}\nPlease respond helpfully.",
        "SYSTEM_PROMPT": "You are a research assistant. Find information related to: {research_fields}",
        "SUMMARIZE_PROMPT": "Please summarize the following paper: {text}"
    },
    additional_params={
        "research_fields": "AI, Machine Learning, Computer Science"
    }
)

# Create the agent
agent = ResearchAgent(config=agent_config)

# Add research papers to the knowledge base
agent.add_document("./papers/transformer_paper.pdf")
agent.add_document("./papers/bert_paper.pdf")

# Process a research query
response = agent.process_query("What are the latest advancements in transformer models?")
print(response)

# Chat with the agent
response = agent.chat("Tell me about the benefits of self-attention mechanisms")
print(response)

# Summarize a paper
paper_text = """
[Paper text here]
"""
summary = agent.summarize_paper(paper_text, max_length=300)
print(summary)

# Find related research
related = agent.find_related_research("transformer models", num_results=3)
print(related)
```

## Implementation Details for Developers

### Key Methods

1. **`process_query(query: str) -> str`**
   - Processes a research query using RAG
   - Returns a detailed response based on the retrieved research

2. **`chat(message: str) -> str`**
   - Handles conversational interactions about research topics
   - Maintains conversation history for context

3. **`summarize_paper(paper_text: str, max_length: int = 500) -> str`**
   - Summarizes a research paper
   - The `max_length` parameter controls the approximate length of the summary

4. **`find_related_research(topic: str, num_results: int = 5) -> str`**
   - Finds related research on a specific topic
   - Returns a list of relevant papers or studies

### Parameter Names in Templates

Make sure your prompt templates use these parameter names:

- In `QUERY_PROMPT`: Use `{research_question}` for the research query
- In `CHAT_PROMPT` and `SYSTEM_PROMPT`: Use `{research_fields}` for the research fields
- In `SUMMARIZE_PROMPT`: Use `{text}` for the paper text

### Custom Configuration

The agent uses a `research_fields` parameter that should be provided in the configuration's `additional_params`. This parameter specifies the research fields the agent specializes in. 