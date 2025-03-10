"""
Configuration module for the multi-agent RAG system.
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Union, Literal
from pathlib import Path
import os
import json
import yaml

# LLM Provider Types
LLMProviderType = Literal["openai", "anthropic", "deepseek"]

class LLMConfig(BaseModel):
    """Configuration for LLM providers."""
    provider: LLMProviderType = Field(..., description="LLM provider name")
    model_name: str = Field(..., description="Model name to use")
    api_key: Optional[str] = Field(None, description="API key (if not in environment)")
    temperature: float = Field(0.7, description="Temperature for generation")
    max_tokens: int = Field(1000, description="Maximum tokens to generate")
    top_p: float = Field(1.0, description="Top p sampling parameter")
    additional_params: Dict[str, Any] = Field(default_factory=dict, description="Additional parameters for the LLM")

class RAGConfig(BaseModel):
    """Configuration for RAG components."""
    collection_name: str = Field(..., description="ChromaDB collection name")
    embedding_model: str = Field("sentence-transformers/all-mpnet-base-v2", description="Embedding model to use")
    chunk_size: int = Field(1000, description="Chunk size for document splitting")
    chunk_overlap: int = Field(200, description="Chunk overlap for document splitting")
    similarity_top_k: int = Field(4, description="Number of chunks to retrieve")
    persist_directory: str = Field("./chroma_db", description="Directory to persist ChromaDB")
    additional_params: Dict[str, Any] = Field(default_factory=dict, description="Additional parameters for RAG")

class AgentConfig(BaseModel):
    """Configuration for an agent."""
    name: str = Field(..., description="Name of the agent")
    description: str = Field(..., description="Description of the agent")
    llm_config: LLMConfig = Field(..., description="LLM configuration")
    rag_config: RAGConfig = Field(..., description="RAG configuration")
    prompt_templates: Dict[str, str] = Field(..., description="Prompt templates for the agent")
    
    @classmethod
    def from_file(cls, config_path: Union[str, Path]) -> "AgentConfig":
        """Load configuration from a file."""
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        if config_path.suffix == ".json":
            with open(config_path, "r") as f:
                config_data = json.load(f)
        elif config_path.suffix in [".yaml", ".yml"]:
            with open(config_path, "r") as f:
                config_data = yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported config file format: {config_path.suffix}")
        
        return cls(**config_data)

def load_api_keys_from_env():
    """Load API keys from environment variables."""
    api_keys = {
        "openai": os.environ.get("OPENAI_API_KEY"),
        "anthropic": os.environ.get("ANTHROPIC_API_KEY"),
        "deepseek": os.environ.get("DEEPSEEK_API_KEY"),
    }
    return api_keys 