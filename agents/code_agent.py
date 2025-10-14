"""
Code Execution Agent
"""
from typing import Dict, Any
from core.llm import llm_manager
from tools.code_executor import code_executor
from utils.prompts import CODE_SYSTEM_PROMPT
from utils.parsers import extract_code_blocks


class CodeAgent:
    """Agent for Python code execution"""
    
    def __init__(self):
        self.llm = llm_manager.get_primary_llm()
        self.name = "Code Agent"
    
    def process(self, query: str) -> Dict[str, Any]:
        """
        Process query by generating and executing code
        
        Args:
            query: User request for code execution
        
        Returns:
            Dict with code, output, and explanation
        """
        try:
            # Create prompt to generate code
            prompt = f"""{CODE_SYSTEM_PROMPT}

User Request: {query}

Please write Python code to fulfill this request. Wrap your code in ```python ``` blocks."""
            
            # Get LLM response with code
            response = self.llm.invoke(prompt)
            llm_response = response.content
            
            # Extract code blocks
            code_blocks = extract_code_blocks(llm_response)
            
            if not code_blocks:
                return {
                    'success': False,
                    'answer': "I couldn't generate appropriate code for this request.",
                    'code': None,
                    'output': None
                }
            
            # Execute the first code block
            code = code_blocks[0]
            execution_result = code_executor.execute(code)
            
            # Format response
            if execution_result['success']:
                answer = f"Code executed successfully!\n\n**Code:**\n```python\n{code}\n```\n\n**Output:**\n```\n{execution_result['output']}\n```"
            else:
                answer = f"Code execution encountered an error.\n\n**Code:**\n```python\n{code}\n```\n\n**Error:**\n```\n{execution_result['error']}\n```"
            
            return {
                'success': execution_result['success'],
                'answer': answer,
                'code': code,
                'output': execution_result['output'],
                'error': execution_result['error']
            }
        
        except Exception as e:
            return {
                'success': False,
                'answer': f"Error in code processing: {str(e)}",
                'code': None,
                'output': None,
                'error': str(e)
            }


# Global instance
code_agent = CodeAgent()

