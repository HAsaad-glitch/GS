"""
DeepSeek LLM provider implementation.
"""
from typing import Dict, Any, List, Optional
import os
from GS.agents_rag_system.llm.base import BaseLLM
from GS.agents_rag_system.config.config import LLMConfig

class DeepSeekLLM(BaseLLM):
    """DeepSeek LLM provider implementation."""
    
    def _setup_client(self) -> Any:
        """Set up the DeepSeek client."""
        try:
            from deepseek import DeepSeekAI
        except ImportError:
            raise ImportError("DeepSeek package not installed. Install it with: pip install deepseek-ai")
        
        api_key = self.config.api_key or os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DeepSeek API key not found in config or environment variables")
        
        return DeepSeekAI(api_key=api_key)
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the DeepSeek model."""
        merged_kwargs = {
            "model": self.config.model_name,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            **self.config.additional_params,
            **kwargs
        }
        
        # Format for chat completion
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            **merged_kwargs
        )
        
        return response.choices[0].message.content
    
    def generate_with_chat_history(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a response from the DeepSeek model using a chat history format."""
        merged_kwargs = {
            "model": self.config.model_name,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            **self.config.additional_params,
            **kwargs
        }
        
        response = self.client.chat.completions.create(
            messages=messages,
            **merged_kwargs
        )
        
        return response.choices[0].message.content 