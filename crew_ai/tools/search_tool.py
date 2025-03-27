from typing import Dict, Any, ClassVar
import json
from crewai.tools import tool

@tool("search_tool")
def search(query: str) -> str:
    """A tool to search for information online.
    
    Args:
        query: The search query to look up online
        
    Returns:
        A JSON string with the search results
    """
    # In a real implementation, this would use an API to search online
    # e.g., using Google, Bing, or a similar search service
    
    # This is a mock implementation that returns dummy results
    data = {
        "results": [
            {
                "title": "Sample search result 1",
                "link": "https://example.com/result1",
                "snippet": "This is the first search result for your query."
            },
            {
                "title": "Sample search result 2",
                "link": "https://example.com/result2",
                "snippet": "This is the second search result related to your search."
            }
        ],
        "query": query,
        "total_results": 2
    }
    
    return json.dumps(data, indent=2)

# Create an instance of the tool for import
SearchTool = search 