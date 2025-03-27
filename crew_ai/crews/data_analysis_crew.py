from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from GS.crew_ai.tools import DataRetrievalTool, SearchTool, CalculatorTool
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from typing import Dict, Any, Optional

@CrewBase
class DataAnalysisCrew:
    """Data analysis crew for analyzing and reporting on data."""

    def __init__(self, agents_config: Dict[str, Any] = None, tasks_config: Dict[str, Any] = None, llm = None):
        """Initialize the DataAnalysisCrew with configurations.
        
        Args:
            agents_config: Configuration for crew agents
            tasks_config: Configuration for crew tasks
            llm: Default LLM to use if not specified in agent configs
        """
        super().__init__()
        self.agents_config = agents_config or {}
        self.tasks_config = tasks_config or {}
        self.default_llm = llm  # Global LLM can be passed to the crew
    
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
    def data_analyzer(self) -> Agent:
        """Creates a data analyst agent."""
        config = self.agents_config.get('data_analyzer', {})
        agent_llm = self.get_agent_llm('data_analyzer')
        
        return Agent(
            role=config.get('role', "Data Analyst"),
            goal=config.get('goal', "Analyze data comprehensively and provide actionable insights"),
            backstory=config.get('backstory', "You are an expert data analyst with years of experience."),
            verbose=config.get('verbose', True),
            allow_delegation=config.get('allow_delegation', False),
            tools=[DataRetrievalTool, CalculatorTool],
            llm=agent_llm
        )

    @agent
    def researcher(self) -> Agent:
        """Creates a research specialist agent."""
        config = self.agents_config.get('researcher', {})
        agent_llm = self.get_agent_llm('researcher')
        
        return Agent(
            role=config.get('role', "Research Specialist"),
            goal=config.get('goal', "Conduct thorough research on given topics"),
            backstory=config.get('backstory', "You are a skilled researcher with a background in multiple disciplines."),
            verbose=config.get('verbose', True),
            allow_delegation=config.get('allow_delegation', True),
            tools=[SearchTool],
            llm=agent_llm
        )

    @agent
    def report_writer(self) -> Agent:
        """Creates a report writer agent."""
        config = self.agents_config.get('report_writer', {})
        agent_llm = self.get_agent_llm('report_writer')
        
        return Agent(
            role=config.get('role', "Report Writer"),
            goal=config.get('goal', "Create clear, concise, and informative reports"),
            backstory=config.get('backstory', "You are a professional writer specialized in creating reports."),
            verbose=config.get('verbose', True),
            allow_delegation=config.get('allow_delegation', False),
            llm=agent_llm
        )

    @task
    def data_analysis_task(self) -> Task:
        """Creates a task for analyzing data."""
        config = self.tasks_config.get('data_analysis_task', {})
        return Task(
            description=config.get('description', "Analyze the provided data to identify key trends, patterns, and insights"),
            expected_output=config.get('expected_output', "A comprehensive analysis report"),
            agent=self.data_analyzer()
        )

    @task
    def research_task(self) -> Task:
        """Creates a task for researching related information."""
        config = self.tasks_config.get('research_task', {})
        return Task(
            description=config.get('description', "Research the specified topic and gather relevant information"),
            expected_output=config.get('expected_output', "Detailed research findings"),
            agent=self.researcher()
        )

    @task
    def report_generation_task(self) -> Task:
        """Creates a task for generating a report based on analysis and research."""
        config = self.tasks_config.get('report_generation_task', {})
        return Task(
            description=config.get('description', "Create a professional report based on the analysis and research findings"),
            expected_output=config.get('expected_output', "A well-structured, comprehensive report"),
            agent=self.report_writer(),
            context=[self.data_analysis_task(), self.research_task()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the data analysis crew."""
        return Crew(
            agents=self.agents,  # Automatically populated by @agent decorators
            tasks=self.tasks,    # Automatically populated by @task decorators
            process=Process.sequential,
            verbose=True
        )