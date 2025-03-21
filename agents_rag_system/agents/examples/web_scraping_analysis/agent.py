"""
Web Scraping Analysis Agent - Analyzes websites to determine scraping techniques and technologies.
"""
from typing import Dict, Any, List, Optional
from GS.agents_rag_system.agents.base.agent import BaseAgent
from GS.agents_rag_system.config.config import AgentConfig
import requests
import json
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class WebScrapingAnalysisAgent(BaseAgent):
    """Web scraping analysis agent implementation."""
    
    def __init__(self, config: AgentConfig):
        """Initialize the web scraping analysis agent."""
        super().__init__(config)
        
        # Default settings if not provided in config
        self.use_proxies = getattr(self.config, "use_proxies", True)
        self.detect_captcha = getattr(self.config, "detect_captcha", True)
        self.default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Initialize knowledge base with common scraping techniques
        self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """Initialize the knowledge base with common scraping knowledge."""
        scraping_knowledge = [
            {
                "content": "For websites with heavy JavaScript, Selenium or Playwright are preferred over BeautifulSoup.",
                "metadata": {"category": "scraping_techniques", "tool": "selenium"}
            },
            {
                "content": "When encountering reCAPTCHA, solutions like 2Captcha, Anti-Captcha, or browser extensions like Buster can be effective.",
                "metadata": {"category": "captcha_handling", "tool": "captcha_solver"}
            },
            {
                "content": "When dealing with rate limiting, implement exponential backoff and use rotating proxies.",
                "metadata": {"category": "rate_limiting", "tool": "proxies"}
            },
            {
                "content": "For extracting data from APIs, inspect network requests in browser dev tools to identify endpoints.",
                "metadata": {"category": "api_scraping", "tool": "network_analysis"}
            },
            {
                "content": "Headless browsers like Puppeteer can be detected. Set user-agent, viewport, and other browser fingerprints to avoid detection.",
                "metadata": {"category": "anti_detection", "tool": "browser_fingerprinting"}
            }
        ]
        
        # Add this knowledge to the RAG system if available
        if hasattr(self, 'rag') and self.rag:
            for item in scraping_knowledge:
                self.add_text(item["content"], item["metadata"])
    
    def process_query(self, query: str) -> str:
        """
        Process a web scraping related query and return a response.
        
        Args:
            query: User query about web scraping or website analysis.
            
        Returns:
            Response to the user with web scraping guidance.
        """
        return self.query_with_rag(
            query=query,
            prompt_key="QUERY_PROMPT",
            user_question=query
        )
    
    def chat(self, message: str) -> str:
        """
        Chat with a user about web scraping strategies.
        
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
                use_proxies=self.use_proxies,
                detect_captcha=self.detect_captcha
            ),
            query=query
        )
        
        # Generate the response using the LLM
        llm_response = self.llm.generate_with_chat_history(self.conversation_history)
        
        # Add the response to the conversation history
        self.add_to_conversation("assistant", llm_response)
        
        return llm_response
    
    def analyze_website(self, url: str) -> Dict[str, Any]:
        """
        Analyze the website structure and content.
        
        Args:
            url: The URL of the website to analyze.
            
        Returns:
            A dictionary with analysis results.
        """
        try:
            # Use RAG to determine if we should analyze the website
            analysis_decision = self.rag.augment_prompt(
                prompt=self.get_formatted_prompt("ANALYSIS_PROMPT", url=url),
                query=f"Should I analyze {url} for web scraping? What should I look for?"
            )
            
            # Simple checks for now, but would be more sophisticated in a full implementation
            response = self._fetch_website(url)
            if not response:
                return {"error": "Failed to fetch website"}
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check for JavaScript frameworks
            scripts = soup.find_all('script')
            script_srcs = [script.get('src', '') for script in scripts]
            
            analysis_results = {
                "dynamic_content": any(['react' in src.lower() or 'vue' in src.lower() or 'angular' in src.lower() for src in script_srcs if src]),
                "javascript_rendering": len(scripts) > 5,  # Simple heuristic
                "ajax_calls": 'XMLHttpRequest' in response.text or 'fetch(' in response.text,
                "infinite_scroll": 'scroll' in response.text and ('load' in response.text or 'pagination' in response.text),
                "forms": len(soup.find_all('form')) > 0,
                "headers": dict(response.headers)
            }
            
            # Enhanced with LLM analysis
            llm_analysis = self.llm.generate(
                prompt=f"""
                Analyze this website data for scraping complexity:
                URL: {url}
                Headers: {json.dumps(dict(response.headers))}
                Features detected: {json.dumps(analysis_results)}
                
                Provide a detailed technical analysis of scraping challenges.
                """
            )
            
            analysis_results["llm_analysis"] = llm_analysis
            return analysis_results
            
        except Exception as e:
            return {"error": str(e)}
    
    def _fetch_website(self, url: str) -> Optional[requests.Response]:
        """
        Fetch website content with proper error handling.
        
        Args:
            url: The URL to fetch.
            
        Returns:
            A response object or None if fetch failed.
        """
        try:
            response = requests.get(url, headers=self.default_headers, timeout=10)
            return response if response.status_code == 200 else None
        except Exception as e:
            return None

    def detect_proxy_and_captcha(self, url: str) -> Dict[str, Any]:
        """
        Detect if proxies or CAPTCHAs are needed.
        
        Args:
            url: The URL of the website to analyze.
            
        Returns:
            A dictionary indicating if proxies or CAPTCHAs are needed.
        """
        try:
            response = self._fetch_website(url)
            if not response:
                return {
                    "proxy_needed": self.use_proxies,
                    "captcha_present": self.detect_captcha,
                    "captcha_type": "Unknown"
                }
            
            # Check for indications of CAPTCHA
            html = response.text.lower()
            captcha_present = any(term in html for term in ['captcha', 'recaptcha', 'hcaptcha', 'solver'])
            
            # Determine CAPTCHA type
            captcha_type = "None"
            if 'recaptcha' in html:
                captcha_type = "reCAPTCHA"
            elif 'hcaptcha' in html:
                captcha_type = "hCaptcha"
            elif 'captcha' in html:
                captcha_type = "Generic CAPTCHA"
            
            # Check for potential proxy indicators
            headers = response.headers
            server_info = headers.get('Server', '')
            cloudflare_indicators = any(cf in headers.keys() for cf in ['CF-Cache-Status', 'CF-RAY'])
            akamai_indicators = 'Akamai' in server_info
            
            # Use LLM to enhance detection
            proxy_captcha_prompt = f"""
            Based on the following website response information, determine if proxies and CAPTCHA handling are needed:
            
            URL: {url}
            Headers: {json.dumps(dict(headers))}
            Contains CAPTCHA keywords: {captcha_present}
            Security services detected: Cloudflare: {cloudflare_indicators}, Akamai: {akamai_indicators}
            
            Return a JSON with these keys:
            - proxy_needed (boolean): whether proxies are needed
            - captcha_present (boolean): whether CAPTCHA is present
            - captcha_type (string): the type of CAPTCHA if detected
            - reason (string): brief explanation of your assessment
            """
            
            llm_response = self.llm.generate(proxy_captcha_prompt)
            try:
                # Try to parse the LLM response as JSON
                llm_result = json.loads(llm_response)
                return llm_result
            except:
                # Fallback to our detection
                return {
                    "proxy_needed": cloudflare_indicators or akamai_indicators or self.use_proxies,
                    "captcha_present": captcha_present,
                    "captcha_type": captcha_type,
                    "reason": "Detection based on HTML and headers analysis"
                }
                
        except Exception as e:
            return {
                "proxy_needed": self.use_proxies,
                "captcha_present": self.detect_captcha,
                "captcha_type": "Unknown",
                "error": str(e)
            }

    def extract_website_tree(self, url: str) -> str:
        """
        Extract and return the website's DOM tree.
        
        Args:
            url: The URL of the website to analyze.
            
        Returns:
            A string representation of the website's DOM tree.
        """
        try:
            response = self._fetch_website(url)
            if not response:
                return "<error>Failed to fetch website</error>"
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Create a simplified tree structure
            def create_tree(element, depth=0, max_depth=3, max_children=5):
                if depth > max_depth:
                    return "..."
                
                if hasattr(element, 'name') and element.name:
                    attrs = ""
                    if element.attrs:
                        key_attrs = ['id', 'class', 'name', 'href', 'src']
                        attrs_list = []
                        for key in key_attrs:
                            if key in element.attrs:
                                value = element.attrs[key]
                                if isinstance(value, list):
                                    value = ' '.join(value)
                                attrs_list.append(f'{key}="{value}"')
                        if attrs_list:
                            attrs = " " + " ".join(attrs_list)
                    
                    if element.name == 'script' or element.name == 'style':
                        return f"<{element.name}{attrs}>...</{element.name}>"
                    
                    children = list(element.children)
                    if not children:
                        return f"<{element.name}{attrs}/>"
                    
                    if len(children) > max_children:
                        children = children[:max_children] + ["..."]
                    
                    child_trees = [create_tree(child, depth + 1, max_depth, max_children) for child in children if child != "\n"]
                    child_trees = [ct for ct in child_trees if ct]
                    
                    if child_trees:
                        return f"<{element.name}{attrs}>\n{'  ' * (depth + 1)}{('  ' * (depth + 1)).join(child_trees)}\n{'  ' * depth}</{element.name}>"
                    else:
                        return f"<{element.name}{attrs}></{element.name}>"
                elif element == "...":
                    return "  " * depth + "..."
                elif isinstance(element, str) and element.strip():
                    return element.strip()
                return ""
            
            # Generate the tree for the body of the page
            body = soup.body
            if not body:
                return "<html><body>No body found</body></html>"
            
            tree = create_tree(body)
            
            # Use LLM to provide a summary of the tree
            tree_summary = self.llm.generate(
                prompt=f"Analyze this HTML structure and provide a brief summary of the key elements relevant for web scraping:\n\n{tree}"
            )
            
            return f"<html>\n<body>\n{tree}\n</body>\n</html>\n\nTree Summary: {tree_summary}"
            
        except Exception as e:
            return f"<error>{str(e)}</error>"

    def recommend_scraping_techniques(self, analysis: Dict[str, Any]) -> List[str]:
        """
        Recommend scraping techniques based on analysis.
        
        Args:
            analysis: The analysis results of the website.
            
        Returns:
            A list of recommended scraping techniques.
        """
        # Build a base set of recommendations
        techniques = []
        
        # Basic tool selection
        if analysis.get("dynamic_content", False) or analysis.get("javascript_rendering", False):
            techniques.append("Selenium/Playwright for browser automation")
        else:
            techniques.append("Requests + BeautifulSoup for simple HTML parsing")
        
        if analysis.get("infinite_scroll", False):
            techniques.append("Implement scrolling logic with wait times")
        
        if analysis.get("ajax_calls", False):
            techniques.append("Intercept AJAX calls to extract data directly from APIs")
        
        if analysis.get("proxy_needed", False):
            techniques.append("Use rotating proxies to avoid IP blocking")
        
        if analysis.get("captcha_present", False):
            captcha_type = analysis.get("captcha_type", "Unknown")
            techniques.append(f"Implement {captcha_type} solving mechanisms")
        
        # Use RAG to enhance recommendations
        rag_prompt = self.get_formatted_prompt(
            "RECOMMENDATION_PROMPT",
            analysis=json.dumps(analysis)
        )
        
        rag_recommendations = self.rag.augment_prompt(
            prompt=rag_prompt,
            query="What are the best scraping techniques for this website?"
        )
        
        # Use LLM to generate final recommendations
        llm_prompt = f"""
        Based on the website analysis:
        {json.dumps(analysis)}
        
        And these initial recommendations:
        {techniques}
        
        Enhanced with RAG knowledge:
        {rag_recommendations}
        
        Provide a comprehensive list of scraping techniques and tools that would be most effective.
        Format each recommendation on a new line starting with '-'.
        Include specific libraries, tools, and approaches.
        """
        
        llm_response = self.llm.generate(llm_prompt)
        
        # Parse the LLM response to extract recommendations
        enhanced_techniques = [line.strip()[2:].strip() for line in llm_response.split('\n') if line.strip().startswith('-')]
        
        # Combine our basic techniques with the enhanced ones
        return list(set(techniques + enhanced_techniques))

    def process_website(self, url: str) -> Dict[str, Any]:
        """
        Main function to process the website and provide recommendations.
        
        Args:
            url: The URL of the website to process.
            
        Returns:
            A dictionary with the analysis, proxy and CAPTCHA info, website tree, and recommendations.
        """
        # First, add the website to the conversation context
        self.add_to_conversation("system", f"Processing website: {url}")
        
        # Validate URL
        if not url.startswith(('http://', 'https://')):
            return {"error": "Invalid URL. Please provide a URL starting with http:// or https://"}
        
        try:
            # For structured domains, try to add relevant domain information to RAG
            domain = urlparse(url).netloc
            domain_info = {
                "domain": domain,
                "url": url,
                "timestamp": self.get_timestamp()
            }
            self.add_text(f"Analyzing website: {domain}", domain_info)
            
            # Perform the analysis
            analysis = self.analyze_website(url)
            proxy_captcha_info = self.detect_proxy_and_captcha(url)
            
            # Only get website tree if previous steps successful
            website_tree = self.extract_website_tree(url) if "error" not in analysis else "<error>Analysis failed</error>"
            
            # Combine analysis results
            combined_analysis = {**analysis, **proxy_captcha_info}
            
            # Get recommendations
            recommendations = self.recommend_scraping_techniques(combined_analysis)
            
            # Generate a scraping strategy using the LLM
            strategy_prompt = self.get_formatted_prompt(
                "STRATEGY_PROMPT",
                url=url,
                analysis=json.dumps(combined_analysis),
                recommendations="\n".join(recommendations)
            )
            
            scraping_strategy = self.llm.generate(strategy_prompt)
            
            # Build the final result
            result = {
                "analysis": analysis,
                "proxy_captcha_info": proxy_captcha_info,
                "website_tree_summary": website_tree[:500] + "..." if len(website_tree) > 500 else website_tree,
                "recommendations": recommendations,
                "scraping_strategy": scraping_strategy
            }
            
            # Add the result to conversation history
            self.add_to_conversation("assistant", f"Analysis complete for {url}")
            
            return result
            
        except Exception as e:
            error_result = {"error": str(e)}
            self.add_to_conversation("system", f"Error processing {url}: {str(e)}")
            return error_result
            
    def get_formatted_prompt(self, prompt_key, **kwargs):
        """
        Get formatted prompt based on the key.
        
        Args:
            prompt_key: The key of the prompt to format.
            **kwargs: Additional formatting arguments.
            
        Returns:
            Formatted prompt string.
        """
        prompts = {
            "QUERY_PROMPT": """
            You are a web scraping expert assistant. The user has asked: 
            {user_question}
            
            Provide a helpful, detailed response about web scraping techniques, best practices, 
            or specific solutions to their problem. Use your knowledge of web scraping tools, 
            anti-scraping measures, and data extraction methods.
            """,
            
            "CHAT_PROMPT": """
            You are a web scraping expert assistant having a conversation with a user.
            
            Use proxies: {use_proxies}
            Detect CAPTCHA: {detect_captcha}
            
            Based on the conversation history, provide a helpful response about web scraping techniques,
            tools, or solutions to the user's problem.
            """,
            
            "ANALYSIS_PROMPT": """
            I need to analyze the website at {url} for web scraping. What aspects of the website
            should I focus on to determine the best scraping approach? What are the key indicators
            of complexity and potential challenges?
            """,
            
            "RECOMMENDATION_PROMPT": """
            Based on this website analysis:
            {analysis}
            
            What are the most effective web scraping techniques and tools to use? Consider factors like:
            1. Static vs dynamic content
            2. JavaScript rendering requirements
            3. Authentication needs
            4. Rate limiting and anti-bot measures
            5. CAPTCHA presence
            6. Data structure and extraction complexity
            
            Provide specific libraries, tools, and approaches.
            """,
            
            "STRATEGY_PROMPT": """
            Create a detailed web scraping strategy for {url}.
            
            Website Analysis:
            {analysis}
            
            Recommended Techniques:
            {recommendations}
            
            Your strategy should include:
            1. Step-by-step approach to scraping this website
            2. Tools and libraries to use with specific configuration options
            3. Handling of any detected challenges (CAPTCHA, dynamic content, etc.)
            4. Data extraction and processing approach
            5. Rate limiting and politeness considerations
            6. Error handling and recovery strategies
            
            Provide code examples where appropriate.
            """
        }
        
        if prompt_key not in prompts:
            raise ValueError(f"Unknown prompt key: {prompt_key}")
        
        return prompts[prompt_key].format(**kwargs)
    
    def get_timestamp(self):
        """Get the current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat() 