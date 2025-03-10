"""
Factory module for creating LLM providers.
"""
from typing import Dict, Any, Union
from GS.agents_rag_system.llm.base import BaseLLM
from GS.agents_rag_system.llm.openai.llm import OpenAILLM
from GS.agents_rag_system.llm.anthropic.llm import AnthropicLLM
from GS.agents_rag_system.llm.deepseek.llm import DeepSeekLLM
from GS.agents_rag_system.config.config import LLMConfig, LLMProviderType

def create_llm(config: LLMConfig) -> BaseLLM:
    """
    Create an LLM provider based on the configuration.
    
    Args:
        config: LLM configuration.
        
    Returns:
        An instance of BaseLLM.
        
    Raises:
        ValueError: If the provider is not supported.
    """
    provider_map: Dict[LLMProviderType, type[BaseLLM]] = {
        "openai": OpenAILLM,
        "anthropic": AnthropicLLM,
        "deepseek": DeepSeekLLM,
    }
    
    if config.provider not in provider_map:
        raise ValueError(f"Unsupported LLM provider: {config.provider}")
    
    return provider_map[config.provider](config) 