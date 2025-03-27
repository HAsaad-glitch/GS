#!/usr/bin/env python
import json
import os
import yaml
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from crewai import LLM
from crewai.flow.flow import Flow, listen, start


# Define our state model
class AnalysisState(BaseModel):
    task_id: Optional[str] = None
    input_data: Dict = {}
    analysis_result: str = ""
    summary_result: Dict = {}
    status: str = "pending"


class ComprehensiveAnalysisFlow(Flow[AnalysisState]):
    """Flow for running a comprehensive data analysis with summarization"""

    def __init__(self, task_id: str = None, data: Dict = None):
        """Initialize the flow with task ID and input data"""
        super().__init__()
        
        if task_id and data:
            self.state.task_id = task_id
            self.state.input_data = data
            self.state.status = "pending"

            # Update task status in database (moved imports into function)
            if task_id:
                from GS.core.app import db
                from GS.core.app.models.task_result import TaskResult
                
                session = db.session
                task = session.query(TaskResult).filter_by(task_id=task_id).first()
                if task:
                    task.status = 'pending'
                    session.commit()

    @start()
    def load_configurations(self):
        """Load configurations for both crews"""
        # Get crew types from data
        analysis_crew_type = self.state.input_data.get('analysis_crew_type', 'data_analysis')
        summary_crew_type = self.state.input_data.get('summary_crew_type', 'data_summary')

        # Load configurations
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Analysis crew configs
        analysis_agents_file = os.path.join(base_dir, f'agents/{analysis_crew_type}_agents.yaml')
        with open(analysis_agents_file, 'r') as f:
            self.analysis_agents_config = yaml.safe_load(f)

        analysis_tasks_file = os.path.join(base_dir, f'tasks/{analysis_crew_type}_tasks.yaml')
        with open(analysis_tasks_file, 'r') as f:
            self.analysis_tasks_config = yaml.safe_load(f)

        # Summary crew configs
        summary_agents_file = os.path.join(base_dir, f'agents/{summary_crew_type}_agents.yaml')
        with open(summary_agents_file, 'r') as f:
            self.summary_agents_config = yaml.safe_load(f)

        summary_tasks_file = os.path.join(base_dir, f'tasks/{summary_crew_type}_tasks.yaml')
        with open(summary_tasks_file, 'r') as f:
            self.summary_tasks_config = yaml.safe_load(f)

        # Update status
        self.state.status = "configured"
        self._update_task_status("in_progress")

        return self.state

    @listen(load_configurations)
    def run_data_analysis(self, state):
        """Run the data analysis crew"""
        # Import inside function to avoid circular imports
        from GS.crew_ai.crews.data_analysis_crew import DataAnalysisCrew
        
        # Create LLM
        llm_config = self.analysis_agents_config.get('llm_config', {})
        llm = LLM(
            model=llm_config.get('model_name', 'gpt-4-turbo'),
            temperature=llm_config.get('temperature', 0.7)
        )

        # Create and run the analysis crew
        analysis_crew = DataAnalysisCrew(
            agents_config=self.analysis_agents_config,
            tasks_config=self.analysis_tasks_config,
            llm=llm
        )

        analysis_result = analysis_crew.crew().kickoff(inputs=self.state.input_data.get('inputs', {}))

        # Store the result
        if hasattr(analysis_result, 'raw'):
            self.state.analysis_result = analysis_result.raw
        else:
            self.state.analysis_result = str(analysis_result)

        self.state.status = "analysis_completed"
        return self.state

    @listen(run_data_analysis)
    def run_data_summary(self, state):
        """Run the data summary crew with the analysis results"""
        # Import inside function to avoid circular imports
        from GS.crew_ai.crews.data_summary_crew import DataSummaryCrew
        
        # Create summary inputs
        summary_inputs = {
            'analysis_report': self.state.analysis_result,
            'additional_context': self.state.input_data.get('additional_context', ''),
            'audience': self.state.input_data.get('audience', 'executive'),
        }

        # Create LLM
        llm_config = self.summary_agents_config.get('llm_config', {})
        llm = LLM(
            model=llm_config.get('model_name', 'gpt-4-turbo'),
            temperature=llm_config.get('temperature', 0.7)
        )

        # Create and run the summary crew
        summary_crew = DataSummaryCrew(
            agents_config=self.summary_agents_config,
            tasks_config=self.summary_tasks_config,
            llm=llm
        )

        summary_result = summary_crew.crew().kickoff(inputs=summary_inputs)

        # Store the summary result
        if hasattr(summary_result, 'raw'):
            summary_content = summary_result.raw
        else:
            summary_content = str(summary_result)

        self.state.summary_result = {
            'content': summary_content
        }

        # Add token usage if available
        if hasattr(summary_result, 'token_usage') and summary_result.token_usage:
            token_usage = summary_result.token_usage
            self.state.summary_result['token_usage'] = {
                'total_tokens': getattr(token_usage, 'total_tokens', 0),
                'prompt_tokens': getattr(token_usage, 'prompt_tokens', 0),
                'completion_tokens': getattr(token_usage, 'completion_tokens', 0),
                'successful_requests': getattr(token_usage, 'successful_requests', 0)
            }

        self.state.status = "completed"
        return self.state

    @listen(run_data_summary)
    def save_results(self, state):
        """Save the final results to the database"""
        # Create combined result
        combined_result = {
            'analysis': {
                'content': self.state.analysis_result
            },
            'summary': self.state.summary_result
        }

        # Update task status in database
        self._update_task_status("completed", json.dumps(combined_result))

        return "Analysis and summary completed successfully"

    def _update_task_status(self, status, result=None):
        """Helper method to update task status in the database"""
        if not hasattr(self.state, 'task_id') or not self.state.task_id:
            return
        
        # Import inside function to avoid circular imports
        from GS.core.app import db
        from GS.core.app.models.task_result import TaskResult
            
        session = db.session
        task = session.query(TaskResult).filter_by(task_id=self.state.task_id).first()
        if task:
            task.status = status
            if result:
                task.result = result
            session.commit()


def run_flow_analysis(task_id: str, data: Dict[Any, Any]) -> None:
    """Run the comprehensive analysis flow"""
    try:
        # Create and run the flow
        flow = ComprehensiveAnalysisFlow(task_id, data)
        flow.kickoff()
    except Exception as e:
        # Import inside function to avoid circular imports
        from GS.core.app import db
        from GS.core.app.models.task_result import TaskResult
        
        # Update task status in case of error
        session = db.session
        task = session.query(TaskResult).filter_by(task_id=task_id).first()
        if task:
            task.status = 'error'
            task.result = json.dumps({'error': str(e)})
            session.commit()
        raise


def plot_flow(output_file='comprehensive_analysis_flow'):
    """Generate a visualization of the comprehensive analysis flow
    
    Args:
        output_file: Name of the output file (without extension)
        
    Returns:
        Path to the generated HTML file or the default filename if path is not returned
    """
    flow = ComprehensiveAnalysisFlow()
    visualization_path = flow.plot(output_file)
    
    # Handle case where flow.plot() returns None but still creates the file
    if visualization_path is None:
        # Use the default filename that CrewAI generates
        default_path = f"{output_file}.html"
        print(f"Flow visualization likely saved as {default_path}")
        return default_path
    
    print(f"Flow visualization saved to {visualization_path}")
    return visualization_path