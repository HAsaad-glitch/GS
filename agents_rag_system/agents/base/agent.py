"""
Base agent implementation.
"""
from typing import Dict, Any, List, Optional, Union
from abc import ABC, abstractmethod
from pathlib import Path
import os
import json

from GS.agents_rag_system.config.config import AgentConfig
from GS.agents_rag_system.llm.factory import create_llm
from GS.agents_rag_system.llm.base import BaseLLM
from GS.agents_rag_system.rag.rag import RAG

class BaseAgent(ABC):
    """Base agent class that can be extended for specific agent types."""
    
    def __init__(self, config: AgentConfig):
        """Initialize the agent with the given configuration."""
        self.config = config
        self.llm = create_llm(config.llm_config)
        self.rag = RAG(config.rag_config)
        self.prompt_templates = config.prompt_templates
        self.conversation_history = []
    
    def add_document(self, file_path: Union[str, Path]) -> None:
        """Add a document to the agent's knowledge base."""
        self.rag.add_document(file_path)
    
    def add_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add text to the agent's knowledge base."""
        self.rag.add_text(text, metadata)
    
    def clear_knowledge_base(self) -> None:
        """Clear the agent's knowledge base."""
        self.rag.clear()
    
    @abstractmethod
    def process_query(self, query: str) -> str:
        """
        Process a query and return a response.
        This method should be implemented by derived classes.
        """
        pass
    
    def add_to_conversation(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        self.conversation_history.append({"role": role, "content": content})
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the conversation history."""
        return self.conversation_history
    
    def clear_conversation_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []
    
    def get_formatted_prompt(self, prompt_key: str, **kwargs) -> str:
        """
        Get a formatted prompt from the prompt templates.
        
        Args:
            prompt_key: Key of the prompt template.
            **kwargs: Arguments to format the prompt template with.
            
        Returns:
            Formatted prompt.
        """
        if prompt_key not in self.prompt_templates:
            raise ValueError(f"Prompt template not found: {prompt_key}")
        
        prompt_template = self.prompt_templates[prompt_key]
        return prompt_template.format(**kwargs)
    
    def query_with_rag(self, query: str, prompt_key: str, **kwargs) -> str:
        """
        Process a query with RAG and return a response.
        
        Args:
            query: Query to process.
            prompt_key: Key of the prompt template to use.
            **kwargs: Additional arguments to format the prompt template with.
            
        Returns:
            Response from the LLM.
        """
        # Get the base prompt
        prompt = self.get_formatted_prompt(prompt_key, **kwargs)
        
        # Augment the prompt with retrieved documents
        augmented_prompt = self.rag.augment_prompt(prompt, query)
        
        # Generate a response using the LLM
        response = self.llm.generate(augmented_prompt)
        
        return response
    
    def query_with_conversation(self, query: str) -> str:
        """
        Process a query with the conversation history and return a response.
        
        Args:
            query: Query to process.
            
        Returns:
            Response from the LLM.
        """
        # Add the user query to the conversation history
        self.add_to_conversation("user", query)
        
        # Generate a response using the LLM with the conversation history
        response = self.llm.generate_with_chat_history(self.conversation_history)
        
        # Add the response to the conversation history
        self.add_to_conversation("assistant", response)
        
        return response
    
    def save_config(self, config_path: Union[str, Path]) -> None:
        """
        Save the agent configuration to a file.
        
        Args:
            config_path: Path to save the configuration to.
        """
        config_path = Path(config_path)
        
        # Ensure the directory exists
        os.makedirs(config_path.parent, exist_ok=True)
        
        # Convert the configuration to a dictionary
        config_dict = self.config.model_dump()
        
        # Save the configuration to a file
        with open(config_path, "w") as f:
            json.dump(config_dict, f, indent=2)
    
    @classmethod
    def load_from_config(cls, config_path: Union[str, Path]) -> "BaseAgent":
        """
        Load an agent from a configuration file.
        
        Args:
            config_path: Path to the configuration file.
            
        Returns:
            An instance of the agent.
        """
        config = AgentConfig.from_file(config_path)
        return cls(config) 