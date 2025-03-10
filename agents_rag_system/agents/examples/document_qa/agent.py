"""
Document QA agent implementation.
"""
from typing import Dict, Any, List, Optional, Union
from GS.agents_rag_system.agents.base.agent import BaseAgent
from GS.agents_rag_system.config.config import AgentConfig

class DocumentQAAgent(BaseAgent):
    """Document QA agent implementation."""
    
    def __init__(self, config: AgentConfig):
        """Initialize the document QA agent."""
        super().__init__(config)
    
    def process_query(self, query: str) -> str:
        """
        Process a query about documents and return a response.
        
        Args:
            query: User query.
            
        Returns:
            Response to the user.
        """
        return self.query_with_rag(
            query=query,
            prompt_key="QUERY_PROMPT",
            user_question=query
        )
    
    def chat(self, message: str) -> str:
        """
        Chat with a user about documents.
        
        Args:
            message: User message.
            
        Returns:
            Response to the user.
        """
        # Add the user message to the conversation history
        self.add_to_conversation("user", message)
        
        # Get the conversation history
        history = self.get_conversation_history()
        
        # Format the history for RAG
        query = " ".join([msg["content"] for msg in history])
        
        # Generate a response using RAG
        response = self.rag.augment_prompt(
            prompt=self.get_formatted_prompt("CHAT_PROMPT"),
            query=query
        )
        
        # Generate the response using the LLM
        llm_response = self.llm.generate_with_chat_history(self.conversation_history)
        
        # Add the response to the conversation history
        self.add_to_conversation("assistant", llm_response)
        
        return llm_response
        
    def get_document_sources(self) -> List[str]:
        """
        Get the list of document sources in the agent's knowledge base.
        
        Returns:
            List of document sources.
        """
        # Using the first few documents to get their sources
        results = self.rag.query("", 100)  # Try to get a large sample
        
        # Extract unique sources
        sources = set()
        for result in results:
            if "source" in result.get("metadata", {}):
                sources.add(result["metadata"]["source"])
        
        return list(sources) 