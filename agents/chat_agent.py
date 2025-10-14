"""
Chat Agent for general conversation
"""
from typing import Dict, Any
from core.llm import llm_manager
from core.memory import memory_manager
from utils.prompts import CHAT_SYSTEM_PROMPT


class ChatAgent:
    """Agent for general conversation"""
    
    def __init__(self):
        self.llm = llm_manager.get_primary_llm()
        self.name = "Chat Agent"
    
    def process(self, query: str, session_id: str = "default") -> Dict[str, Any]:
        """
        Process general conversation
        
        Args:
            query: User message
            session_id: Session identifier
        
        Returns:
            Dict with answer
        """
        try:
            # Get conversation history
            history = memory_manager.get_context_string(session_id, last_n=3)
            
            # Create prompt with context
            if history:
                prompt = f"""{CHAT_SYSTEM_PROMPT}

Conversation History:
{history}

User: {query}

Please respond naturally and helpfully."""
            else:
                prompt = f"""{CHAT_SYSTEM_PROMPT}

User: {query}

Please respond naturally and helpfully."""
            
            # Get LLM response
            response = self.llm.invoke(prompt)
            answer = response.content
            
            return {
                'success': True,
                'answer': answer
            }
        
        except Exception as e:
            return {
                'success': False,
                'answer': f"Error in chat processing: {str(e)}"
            }


# Global instance
chat_agent = ChatAgent()