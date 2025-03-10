"""
Utility functions for initialization.
"""
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Union, Type
from GS.agents_rag_system.config.config import AgentConfig
from GS.agents_rag_system.agents.base.agent import BaseAgent

def load_agent_from_config(agent_class: Type[BaseAgent], config_path: Union[str, Path]) -> BaseAgent:
    """
    Load an agent from a configuration file.
    
    Args:
        agent_class: Agent class to instantiate.
        config_path: Path to the configuration file.
        
    Returns:
        An instance of the agent.
    """
    config = AgentConfig.from_file(config_path)
    return agent_class(config)

def load_documents_from_directory(agent: BaseAgent, directory: Union[str, Path]) -> int:
    """
    Load documents from a directory into an agent's knowledge base.
    
    Args:
        agent: Agent to load documents into.
        directory: Directory to load documents from.
        
    Returns:
        Number of documents loaded.
    """
    directory = Path(directory)
    
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    count = 0
    for file_path in directory.glob("**/*.*"):
        if file_path.is_file() and file_path.suffix.lower() in [".txt", ".md", ".pdf", ".docx", ".html"]:
            try:
                agent.add_document(file_path)
                count += 1
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
    
    return count 