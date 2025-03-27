from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from GS.crew_ai.tools import CalculatorTool
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from typing import Dict, Any, Optional

@CrewBase
class DataSummaryCrew:
    """Crew for summarizing data analysis reports and creating executive summaries."""
    
    def __init__(self, agents_config: Dict[str, Any] = None, tasks_config: Dict[str, Any] = None, llm = None):
        """Initialize the DataSummaryCrew with configurations.
        
        Args:
            agents_config: Configuration for crew agents
            tasks_config: Configuration for crew tasks
            llm: Default LLM to use if not specified in agent configs
        """
        super().__init__()
        self.agents_config = agents_config or {}
        self.tasks_config = tasks_config or {}
        self.default_llm = llm

    def get_agent_llm(self, agent_name):
        """Get the LLM for a specific agent based on configuration."""
        agent_config = self.agents_config.get(agent_name, {})
        llm_config = agent_config.get('llm', None)
        
        # If no agent-specific LLM config, use the global LLM config or default
        if not llm_config:
            # Try to use global LLM from YAML if available
            global_llm_config = self.agents_config.get('llm_config', {})
            if global_llm_config:
                return self._create_llm_from_config(global_llm_config)
            # Otherwise, use the default LLM passed to the constructor
            return self.default_llm
        
        # Create LLM from agent-specific config
        return self._create_llm_from_config(llm_config)
    
    def _create_llm_from_config(self, config):
        """Create an LLM instance from a configuration dictionary."""
        provider = config.get('provider', 'openai')
        model_name = config.get('model_name', 'gpt-4-turbo')
        temperature = config.get('temperature', 0.7)
        
        if provider == 'openai':
            return ChatOpenAI(
                model_name=model_name,
                temperature=temperature
            )
        elif provider == 'anthropic':
            return ChatAnthropic(
                model_name=model_name,
                temperature=temperature
            )
        # Default to OpenAI
        return ChatOpenAI(
            model_name=model_name,
            temperature=temperature
        )

    @agent
    def executive_summarizer(self) -> Agent:
        """Creates an executive summary agent."""
        config = self.agents_config.get('executive_summarizer', {})
        agent_llm = self.get_agent_llm('executive_summarizer')
        
        return Agent(
            role=config.get('role', "Executive Summarizer"),
            goal=config.get('goal', "Create concise executive summaries from detailed reports"),
            backstory=config.get('backstory', "You are a skilled executive assistant known for distilling complex information into actionable insights for busy executives."),
            verbose=config.get('verbose', True),
            allow_delegation=config.get('allow_delegation', False),
            tools=[CalculatorTool],
            llm=agent_llm
        )

    @agent
    def visualization_expert(self) -> Agent:
        """Creates a data visualization expert agent."""
        config = self.agents_config.get('visualization_expert', {})
        agent_llm = self.get_agent_llm('visualization_expert')
        
        return Agent(
            role=config.get('role', "Data Visualization Expert"),
            goal=config.get('goal', "Create descriptive visualizations for complex data"),
            backstory=config.get('backstory', "You are an expert in data visualization who can describe how to represent complex data in clear, compelling visuals."),
            verbose=config.get('verbose', True),
            allow_delegation=config.get('allow_delegation', False),
            llm=agent_llm
        )

    @task
    def create_executive_summary(self) -> Task:
        """Creates a task for summarizing detailed reports into executive summaries."""
        config = self.tasks_config.get('create_executive_summary', {})
        return Task(
            description=config.get('description', "Create a concise executive summary of the detailed analysis report"),
            expected_output=config.get('expected_output', "A one-page executive summary highlighting key insights and recommendations"),
            agent=self.executive_summarizer()
        )

    @task
    def suggest_visualizations(self) -> Task:
        """Creates a task for suggesting data visualizations."""
        config = self.tasks_config.get('suggest_visualizations', {})
        return Task(
            description=config.get('description', "Suggest appropriate data visualizations to illustrate the key findings"),
            expected_output=config.get('expected_output', "A list of recommended visualizations with descriptions"),
            agent=self.visualization_expert(),
            context=[self.create_executive_summary()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the data summary crew."""
        return Crew(
            agents=self.agents,  # Automatically populated by @agent decorators
            tasks=self.tasks,    # Automatically populated by @task decorators
            process=Process.sequential,
            verbose=True
        ) 