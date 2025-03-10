"""
Code assistant agent implementation.
"""
from typing import Dict, Any, List, Optional, Union
from GS.agents_rag_system.agents.base.agent import BaseAgent
from GS.agents_rag_system.config.config import AgentConfig

class CodeAssistantAgent(BaseAgent):
    """Code assistant agent implementation."""
    
    def __init__(self, config: AgentConfig):
        """Initialize the code assistant agent."""
        super().__init__(config)
        
        # Default programming languages and frameworks if not provided in config
        self.languages = getattr(self.config, "languages", "Python, JavaScript, TypeScript, Java, C++, C#")
        self.frameworks = getattr(self.config, "frameworks", "React, Django, Flask, Spring, Node.js, Express.js")
    
    def process_query(self, query: str) -> str:
        """
        Process a code-related query and return a response.
        
        Args:
            query: User query about code.
            
        Returns:
            Response to the user with code assistance.
        """
        return self.query_with_rag(
            query=query,
            prompt_key="QUERY_PROMPT",
            user_question=query
        )
    
    def chat(self, message: str) -> str:
        """
        Chat with a user about code.
        
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
                languages=self.languages,
                frameworks=self.frameworks
            ),
            query=query
        )
        
        # Generate the response using the LLM
        llm_response = self.llm.generate_with_chat_history(self.conversation_history)
        
        # Add the response to the conversation history
        self.add_to_conversation("assistant", llm_response)
        
        return llm_response
    
    def analyze_code(self, code: str, language: str = None) -> str:
        """
        Analyze a piece of code and provide feedback.
        
        Args:
            code: Code to analyze.
            language: Programming language of the code.
            
        Returns:
            Analysis of the code.
        """
        prompt = f"""
Please analyze the following code and provide feedback on:
1. Code quality and best practices
2. Potential bugs or issues
3. Performance considerations
4. Security considerations
5. Suggestions for improvement

Programming language: {language or 'auto-detect'}

Code to analyze:
```
{code}
```

Please provide a detailed analysis with specific suggestions for improvement.
"""
        # Add relevant code examples to the knowledge base for context
        self.add_text(code, {"language": language, "type": "code_to_analyze"})
        
        # Generate a response using RAG
        return self.rag.augment_prompt(prompt, code)
    
    def generate_code(self, requirement: str, language: str = None) -> str:
        """
        Generate code based on requirements.
        
        Args:
            requirement: Code requirement.
            language: Programming language to use.
            
        Returns:
            Generated code.
        """
        language = language or "Python"
        
        prompt = f"""
Please generate code based on the following requirement:

Requirement: {requirement}

Programming language: {language}

Please provide:
1. Well-commented and clean code that meets the requirement
2. A brief explanation of how the code works
3. Any assumptions made
4. Instructions for running or testing the code
"""
        # Generate a response using RAG
        return self.query_with_rag(
            query=requirement,
            prompt_key="SYSTEM_PROMPT",
            languages=self.languages,
            frameworks=self.frameworks
        ) 