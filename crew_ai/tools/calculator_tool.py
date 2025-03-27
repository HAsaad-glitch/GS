from typing import Dict, Any, ClassVar
import json
import numexpr
from crewai.tools import tool

@tool("calculator_tool")
def calculate(expression: str) -> str:
    """A tool to evaluate mathematical expressions.
    
    Args:
        expression: The mathematical expression to evaluate
        
    Returns:
        A JSON string with the result of the calculation
    """
    try:
        # Safely evaluate the expression using numexpr
        result = numexpr.evaluate(expression).item()
        data = {
            "expression": expression,
            "result": result,
            "success": True
        }
        return json.dumps(data, indent=2)
    except Exception as e:
        data = {
            "expression": expression,
            "error": str(e),
            "success": False
        }
        return json.dumps(data, indent=2)

# Create an instance of the tool for import
CalculatorTool = calculate 