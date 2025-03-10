"""
Research agent implementation.
"""
from typing import Dict, Any, List, Optional, Union
from GS.agents_rag_system.agents.base.agent import BaseAgent
from GS.agents_rag_system.config.config import AgentConfig

class ResearchAgent(BaseAgent):
    """Research agent implementation."""
    
    def __init__(self, config: AgentConfig):
        """Initialize the research agent."""
        super().__init__(config)
        
        # Default research fields if not provided in config
        self.research_fields = getattr(self.config, "research_fields", 
                                     "AI, Machine Learning, Computer Science, Medicine, Biology, Physics")
    
    def process_query(self, query: str) -> str:
        """
        Process a research query and return a response.
        
        Args:
            query: Research query.
            
        Returns:
            Response with research findings.
        """
        return self.query_with_rag(
            query=query,
            prompt_key="QUERY_PROMPT",
            research_question=query
        )
    
    def chat(self, message: str) -> str:
        """
        Chat with a user about research topics.
        
        Args:
            message: User message.
            
        Returns:
            Response to the user.
        """
        # Add the user message to the conversation history
        self.add_to_conversation("user", message)
        
        # Get the conversation history
        history = self.get_conversation_history()
        
        # Format the history for RAG
        query = " ".join([msg["content"] for msg in history])
        
        # Generate a response using RAG
        response = self.rag.augment_prompt(
            prompt=self.get_formatted_prompt(
                "CHAT_PROMPT",
                research_fields=self.research_fields
            ),
            query=query
        )
        
        # Generate the response using the LLM
        llm_response = self.llm.generate_with_chat_history(self.conversation_history)
        
        # Add the response to the conversation history
        self.add_to_conversation("assistant", llm_response)
        
        return llm_response
    
    def summarize_paper(self, paper_text: str, max_length: int = 500) -> str:
        """
        Summarize a research paper.
        
        Args:
            paper_text: Text of the research paper.
            max_length: Maximum length of the summary.
            
        Returns:
            Summary of the research paper.
        """
        prompt = f"""
Please summarize the following research paper in approximately {max_length} words:

1. Focus on the key findings and contributions
2. Include the research methodology
3. Highlight any limitations mentioned
4. Note the implications of the research

Please structure the summary with these headings:
- Key Findings
- Methodology
- Limitations
- Implications
"""
        # Add the paper to the knowledge base for context
        self.add_text(paper_text, {"type": "research_paper"})
        
        # Generate a response using RAG
        return self.rag.augment_prompt(prompt, paper_text)
    
    def find_related_research(self, topic: str, num_results: int = 5) -> str:
        """
        Find related research on a topic.
        
        Args:
            topic: Research topic.
            num_results: Number of results to return.
            
        Returns:
            Related research findings.
        """
        prompt = f"""
Please find {num_results} related research papers or studies on the topic of "{topic}".

For each paper or study, please provide:
1. Title
2. Authors
3. Year of publication
4. Brief description of findings (1-2 sentences)
5. How it relates to the topic

Please organize the results from most relevant to least relevant.
"""
        return self.query_with_rag(
            query=topic,
            prompt_key="SYSTEM_PROMPT",
            research_fields=self.research_fields
        ) 