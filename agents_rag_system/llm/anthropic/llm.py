"""
Anthropic (Claude) LLM provider implementation.
"""
from typing import Dict, Any, List, Optional
import os
import anthropic
from GS.agents_rag_system.llm.base import BaseLLM
from GS.agents_rag_system.config.config import LLMConfig

class AnthropicLLM(BaseLLM):
    """Anthropic (Claude) LLM provider implementation."""
    
    def _setup_client(self) -> anthropic.Anthropic:
        """Set up the Anthropic client."""
        api_key = self.config.api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Anthropic API key not found in config or environment variables")
        
        return anthropic.Anthropic(api_key=api_key)
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the Anthropic model."""
        merged_kwargs = {
            "model": self.config.model_name,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            **self.config.additional_params,
            **kwargs
        }
        
        # Create a structured message for Claude
        message = self.client.messages.create(
            messages=[{"role": "user", "content": prompt}],
            **merged_kwargs
        )
        
        return message.content[0].text
    
    def generate_with_chat_history(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a response from the Anthropic model using a chat history format."""
        # Convert standard chat format to Anthropic format
        anthropic_messages = []
        
        for message in messages:
            role = message["role"]
            # Map 'assistant' to 'assistant' and everything else to 'user'
            anthropic_role = "assistant" if role == "assistant" else "user"
            anthropic_messages.append({
                "role": anthropic_role,
                "content": message["content"]
            })
        
        merged_kwargs = {
            "model": self.config.model_name,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            **self.config.additional_params,
            **kwargs
        }
        
        response = self.client.messages.create(
            messages=anthropic_messages,
            **merged_kwargs
        )
        
        return response.content[0].text 