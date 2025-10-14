"""
Health check endpoints
"""
from fastapi import APIRouter
from core.vectorstore import vector_manager

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "IntelAgent"
    }


@router.get("/status")
async def get_status():
    """Get system status"""
    try:
        doc_count = vector_manager.get_document_count()
        
        return {
            "status": "operational",
            "documents_indexed": doc_count,
            "agents": ["RAG", "SEARCH", "CODE", "TOOL", "CHAT"]
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

