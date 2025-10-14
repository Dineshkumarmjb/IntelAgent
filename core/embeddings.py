"""
Embedding models for IntelAgent
"""
from langchain_openai import OpenAIEmbeddings
from app.config import settings


class EmbeddingManager:
    """Manages embedding models"""
    
    def __init__(self):
        self.model = settings.EMBEDDING_MODEL
        self._embeddings = None
    
    def get_embeddings(self) -> OpenAIEmbeddings:
        """Get OpenAI embeddings instance (cached)"""
        if self._embeddings is None:
            self._embeddings = OpenAIEmbeddings(
                model=self.model,
                api_key=settings.OPENAI_API_KEY
            )
        return self._embeddings


# Global instance
embedding_manager = EmbeddingManager()

