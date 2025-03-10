"""
Base LLM provider implementation.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from GS.agents_rag_system.config.config import LLMConfig

class BaseLLM(ABC):
    """Base class for LLM providers."""
    
    def __init__(self, config: LLMConfig):
        """Initialize the LLM provider with configuration."""
        self.config = config
        self.client = self._setup_client()
    
    @abstractmethod
    def _setup_client(self) -> Any:
        """Set up the client for the LLM provider."""
        pass
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the LLM."""
        pass
    
    @abstractmethod
    def generate_with_chat_history(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a response from the LLM using a chat history format."""
        pass 