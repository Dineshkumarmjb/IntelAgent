"""
LLM client management for IntelAgent
"""
from langchain_openai import ChatOpenAI
from app.config import settings


class LLMManager:
    """Manages LLM instances for different use cases"""
    
    def __init__(self):
        self.primary_model = settings.PRIMARY_MODEL
        self.advanced_model = settings.ADVANCED_MODEL
        self.temperature = settings.TEMPERATURE
    
    def get_primary_llm(self, temperature: float = None) -> ChatOpenAI:
        """Get primary LLM (fast, cost-effective)"""
        return ChatOpenAI(
            model=self.primary_model,
            temperature=temperature or self.temperature,
            api_key=settings.OPENAI_API_KEY
        )
    
    def get_advanced_llm(self, temperature: float = None) -> ChatOpenAI:
        """Get advanced LLM (for complex reasoning)"""
        return ChatOpenAI(
            model=self.advanced_model,
            temperature=temperature or self.temperature,
            api_key=settings.OPENAI_API_KEY
        )
    
    def get_vision_llm(self) -> ChatOpenAI:
        """Get vision-capable LLM"""
        return ChatOpenAI(
            model="gpt-4o",  # Vision requires GPT-4o
            temperature=self.temperature,
            api_key=settings.OPENAI_API_KEY
        )


# Global instance
llm_manager = LLMManager()

