"""
Tool Agent for calculations and utilities
"""
from typing import Dict, Any
from core.llm import llm_manager
from tools.calculator import calculator
from utils.prompts import TOOL_SYSTEM_PROMPT
import re


class ToolAgent:
    """Agent for calculations and utility functions"""
    
    def __init__(self):
        self.llm = llm_manager.get_primary_llm()
        self.name = "Tool Agent"
    
    def process(self, query: str) -> Dict[str, Any]:
        """
        Process query using tools
        
        Args:
            query: User request for calculation or utility
        
        Returns:
            Dict with answer
        """
        try:
            # Try to detect calculation patterns
            calc_result = self._try_calculate(query)
            
            if calc_result:
                return {
                    'success': True,
                    'answer': calc_result
                }
            
            # Otherwise, use LLM with tool assistance
            prompt = f"""{TOOL_SYSTEM_PROMPT}

User Query: {query}

Please provide a detailed answer with step-by-step calculations if applicable."""
            
            response = self.llm.invoke(prompt)
            answer = response.content
            
            return {
                'success': True,
                'answer': answer
            }
        
        except Exception as e:
            return {
                'success': False,
                'answer': f"Error in tool processing: {str(e)}"
            }
    
    def _try_calculate(self, query: str) -> str:
        """Try to perform direct calculation"""
        # Pattern: "calculate X% of Y"
        percentage_pattern = r'(?:calculate|what\s+is|find)\s+(\d+\.?\d*)\s*%\s+of\s+(\d+\.?\d*)'
        match = re.search(percentage_pattern, query.lower())
        
        if match:
            percentage = float(match.group(1))
            value = float(match.group(2))
            result = calculator.percentage(value, percentage)
            return f"{percentage}% of {value} = {result}"
        
        # Pattern: "X + Y", "X * Y", etc.
        math_pattern = r'(\d+\.?\d*)\s*([\+\-\*/])\s*(\d+\.?\d*)'
        match = re.search(math_pattern, query)
        
        if match:
            expr = f"{match.group(1)} {match.group(2)} {match.group(3)}"
            result = calculator.evaluate(expr)
            if result['success']:
                return f"{expr} = {result['result']}"
        
        return None


# Global instance
tool_agent = ToolAgent()

