"""
Chat endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from agents.supervisor import supervisor
from core.memory import memory_manager

router = APIRouter()


class ChatRequest(BaseModel):
    """Chat request model"""
    query: str
    session_id: Optional[str] = "default"


class ChatResponse(BaseModel):
    """Chat response model"""
    success: bool
    answer: str
    sources: List[Dict[str, Any]] = []
    citations: Dict[str, str] = {}
    agent_used: str
    routing: str


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat query
    
    Args:
        request: Chat request with query and session_id
    
    Returns:
        Chat response with answer and metadata
    """
    try:
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Process query through supervisor
        result = supervisor.process(
            query=request.query,
            session_id=request.session_id
        )
        
        return ChatResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{session_id}")
async def get_history(session_id: str):
    """Get conversation history for a session"""
    try:
        history = memory_manager.get_history(session_id)
        
        return {
            "session_id": session_id,
            "message_count": len(history),
            "messages": [
                {
                    "type": msg.__class__.__name__,
                    "content": msg.content
                }
                for msg in history
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/history/{session_id}")
async def clear_history(session_id: str):
    """Clear conversation history for a session"""
    try:
        memory_manager.clear_session(session_id)
        
        return {
            "success": True,
            "message": f"History cleared for session: {session_id}"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

