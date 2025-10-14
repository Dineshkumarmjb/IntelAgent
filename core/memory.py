"""
Conversation memory management
"""
from typing import List, Dict, Any
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseMessage, HumanMessage, AIMessage


class MemoryManager:
    """Manages conversation history and memory"""
    
    def __init__(self):
        self.sessions: Dict[str, ConversationBufferMemory] = {}
    
    def get_session_memory(self, session_id: str) -> ConversationBufferMemory:
        """Get or create memory for a session"""
        if session_id not in self.sessions:
            self.sessions[session_id] = ConversationBufferMemory(
                return_messages=True,
                memory_key="chat_history"
            )
        return self.sessions[session_id]
    
    def add_message(self, session_id: str, human_msg: str, ai_msg: str):
        """Add a conversation turn to memory"""
        memory = self.get_session_memory(session_id)
        memory.chat_memory.add_user_message(human_msg)
        memory.chat_memory.add_ai_message(ai_msg)
    
    def get_history(self, session_id: str) -> List[BaseMessage]:
        """Get conversation history"""
        memory = self.get_session_memory(session_id)
        return memory.chat_memory.messages
    
    def clear_session(self, session_id: str):
        """Clear session memory"""
        if session_id in self.sessions:
            self.sessions[session_id].clear()
    
    def get_context_string(self, session_id: str, last_n: int = 5) -> str:
        """Get recent conversation as formatted string"""
        history = self.get_history(session_id)
        
        # Get last N messages
        recent = history[-last_n*2:] if len(history) > last_n*2 else history
        
        context_parts = []
        for msg in recent:
            if isinstance(msg, HumanMessage):
                context_parts.append(f"User: {msg.content}")
            elif isinstance(msg, AIMessage):
                context_parts.append(f"Assistant: {msg.content}")
        
        return "\n".join(context_parts)


# Global instance
memory_manager = MemoryManager()

