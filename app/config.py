"""
Configuration management for IntelAgent
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys
    OPENAI_API_KEY: str
    TAVILY_API_KEY: Optional[str] = None
    
    # Models
    PRIMARY_MODEL: str = "gpt-4o-mini"
    ADVANCED_MODEL: str = "gpt-4o"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Temperature
    TEMPERATURE: float = 0.1
    
    # Vector Database
    CHROMA_PERSIST_DIR: str = "./data/chroma_db"
    COLLECTION_NAME: str = "intelagent_docs"
    
    # File Storage
    UPLOAD_DIR: str = "./data/uploads"
    MAX_FILE_SIZE_MB: int = 50
    
    # Code Execution
    CODE_TIMEOUT_SECONDS: int = 10
    CODE_MAX_MEMORY_MB: int = 256
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    
    # Session
    SESSION_TIMEOUT_MINUTES: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Initialize settings
settings = Settings()

# Create necessary directories
Path(settings.CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)

# Validate OpenAI API key
if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_openai_api_key_here":
    raise ValueError(
        "OpenAI API key not found! Please set OPENAI_API_KEY in .env file"
    )

