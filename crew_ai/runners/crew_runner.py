import os
import yaml
import json
from typing import Dict, Any, Optional
from GS.core.app.models.task_result import TaskResult
from GS.crew_ai.crews.data_analysis_crew import DataAnalysisCrew
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

def get_llm(provider: str = 'openai', model_name: str = 'gpt-4-turbo', temperature: float = 0.7, **kwargs):
    """Get an LLM instance based on provider and model name."""
    if provider.lower() == 'openai':
        return ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            **kwargs
        )
    elif provider.lower() == 'anthropic':
        return ChatAnthropic(
            model_name=model_name,
            temperature=temperature,
            **kwargs
        )
    else:
        # Default to OpenAI
        return ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            **kwargs
        )

def run_data_analysis_crew(task_id: str, data: Dict[Any, Any]) -> None:
    """Run a CrewAI data analysis task.
    
    Args:
        task_id: The ID of the task to run.
        data: The data to pass to the crew.
    """
    from GS.core.app import db
    
    try:
        # Get crew type from data or default to data_analysis
        crew_type = data.get('crew_type', 'data_analysis')
        
        # Load agent and task configurations from YAML files
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Load agent configuration
        agents_file = os.path.join(base_dir, f'agents/{crew_type}_agents.yaml')
        with open(agents_file, 'r') as f:
            agents_config = yaml.safe_load(f)
        
        # Load task configuration
        tasks_file = os.path.join(base_dir, f'tasks/{crew_type}_tasks.yaml')
        with open(tasks_file, 'r') as f:
            tasks_config = yaml.safe_load(f)
        
        # Initialize default LLM (can be overridden by agent configs)
        llm_config = agents_config.get('llm_config', {})
        default_llm = get_llm(
            provider=llm_config.get('provider', 'openai'),
            model_name=llm_config.get('model_name', 'gpt-4-turbo'),
            temperature=llm_config.get('temperature', 0.7)
        )
        
        # Create crew instance
        crew_instance = DataAnalysisCrew(
            agents_config=agents_config,
            tasks_config=tasks_config,
            llm=default_llm
        )
        
        # Run the crew
        crew = crew_instance.crew()
        result = crew.kickoff(inputs=data.get('inputs', {}))
        
        # Convert CrewOutput to a JSON-serializable format
        serializable_result = {}
        if hasattr(result, 'raw'):
            serializable_result['content'] = result.raw
        elif hasattr(result, '__str__'):
            serializable_result['content'] = str(result)
        else:
            serializable_result['content'] = "Result format not supported"
        
        # Add any additional metadata if available
        if hasattr(result, 'token_usage') and result.token_usage:
            token_usage = result.token_usage
            serializable_result['token_usage'] = {
                'total_tokens': getattr(token_usage, 'total_tokens', 0),
                'prompt_tokens': getattr(token_usage, 'prompt_tokens', 0),
                'completion_tokens': getattr(token_usage, 'completion_tokens', 0),
                'successful_requests': getattr(token_usage, 'successful_requests', 0)
            }
        
        # Convert the dictionary to a JSON string
        json_result = json.dumps(serializable_result)
        
        # Update task status in database
        session = db.session
        task = session.query(TaskResult).filter_by(task_id=task_id).first()
        if task:
            task.status = 'completed'
            task.result = json_result
            session.commit()
    
    except Exception as e:
        # Update task status in case of error
        session = db.session
        task = session.query(TaskResult).filter_by(task_id=task_id).first()
        if task:
            task.status = 'error'
            task.result = json.dumps({'error': str(e)})
            session.commit()
        raise