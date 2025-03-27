from typing import Dict, Any, ClassVar
import json
from crewai.tools import tool

@tool("data_retrieval_tool")
def retrieve_data(query: str, limit: int = 10) -> str:
    """A tool to retrieve data from internal databases or data sources.
    
    Args:
        query: The search query for retrieving data
        limit: The maximum number of results to return, defaults to 10
        
    Returns:
        A JSON string with the retrieved data
    """
    # In a real implementation, this would connect to your database
    # or other data source and retrieve the actual data
    
    # This is a mock implementation that returns dummy data
    data = {
        "results": [
            {"id": 1, "title": "Sample data 1", "content": "This is sample data retrieved based on your query."},
            {"id": 2, "title": "Sample data 2", "content": "More sample data that matches your search criteria."},
        ],
        "count": 2,
        "query": query,
        "limit": limit
    }
    
    return json.dumps(data, indent=2)

# Create an instance of the tool for import
DataRetrievalTool = retrieve_data 