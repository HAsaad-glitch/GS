"""
Customer support agent implementation.
"""
from typing import Dict, Any, List, Optional, Union
from GS.agents_rag_system.agents.base.agent import BaseAgent
from GS.agents_rag_system.config.config import AgentConfig

class CustomerSupportAgent(BaseAgent):
    """Customer support agent implementation."""
    
    def __init__(self, config: AgentConfig):
        """Initialize the customer support agent."""
        super().__init__(config)
    
    def process_query(self, query: str) -> str:
        """
        Process a customer query and return a response.
        
        Args:
            query: Customer query.
            
        Returns:
            Response to the customer.
        """
        return self.query_with_rag(
            query=query,
            prompt_key="QUERY_PROMPT",
            customer_query=query
        )
    
    def chat(self, message: str) -> str:
        """
        Chat with a customer.
        
        Args:
            message: Customer message.
            
        Returns:
            Response to the customer.
        """
        # Add the user message to the conversation history
        self.add_to_conversation("user", message)
        
        # Get the conversation history
        history = self.get_conversation_history()
        
        # Format the history for RAG
        query = " ".join([msg["content"] for msg in history])
        
        # Generate a response using RAG
        response = self.rag.augment_prompt(
            prompt=self.get_formatted_prompt(
                "CHAT_PROMPT",
                company_name=getattr(self.config, "company_name", "Company"),
                company_description=getattr(self.config, "company_description", "")
            ),
            query=query
        )
        
        # Generate the response using the LLM
        llm_response = self.llm.generate_with_chat_history(self.conversation_history)
        
        # Add the response to the conversation history
        self.add_to_conversation("assistant", llm_response)
        
        return llm_response 