"""
OpenAI LLM provider implementation.
"""
from typing import Dict, Any, List, Optional
import os
from openai import OpenAI
from GS.agents_rag_system.llm.base import BaseLLM
from GS.agents_rag_system.config.config import LLMConfig

class OpenAILLM(BaseLLM):
    """OpenAI LLM provider implementation."""
    
    def _setup_client(self) -> OpenAI:
        """Set up the OpenAI client."""
        api_key = self.config.api_key or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found in config or environment variables")
        
        return OpenAI(api_key=api_key)
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the OpenAI model."""
        merged_kwargs = {
            "model": self.config.model_name,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "top_p": self.config.top_p,
            **self.config.additional_params,
            **kwargs
        }
        
        # Format for text completion if using older models
        if "gpt-3.5-turbo" in self.config.model_name or "gpt-4" in self.config.model_name:
            messages = [{"role": "user", "content": prompt}]
            response = self.client.chat.completions.create(
                messages=messages,
                **merged_kwargs
            )
            return response.choices[0].message.content
        else:
            response = self.client.completions.create(
                prompt=prompt,
                **merged_kwargs
            )
            return response.choices[0].text
    
    def generate_with_chat_history(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a response from the OpenAI model using a chat history format."""
        if not ("gpt-3.5-turbo" in self.config.model_name or "gpt-4" in self.config.model_name):
            # For non-chat models, convert messages to a single prompt
            prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
            return self.generate(prompt, **kwargs)
        
        merged_kwargs = {
            "model": self.config.model_name,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "top_p": self.config.top_p,
            **self.config.additional_params,
            **kwargs
        }
        
        response = self.client.chat.completions.create(
            messages=messages,
            **merged_kwargs
        )
        
        return response.choices[0].message.content 