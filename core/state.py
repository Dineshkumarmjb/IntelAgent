"""
Agent state management for LangGraph
"""
from typing import TypedDict, List, Dict, Any, Annotated, Sequence
from langchain_core.messages import BaseMessage
import operator


class AgentState(TypedDict):
    """State for multi-agent system"""
    
    # Core state
    messages: Annotated[Sequence[BaseMessage], operator.add]
    query: str
    session_id: str
    
    # Agent routing
    next_agent: str
    agents_used: List[str]
    
    # Results
    rag_result: Dict[str, Any]
    search_result: Dict[str, Any]
    code_result: Dict[str, Any]
    tool_result: Dict[str, Any]
    
    # Final output
    final_answer: str
    citations: List[Dict[str, Any]]
    confidence: float
    
    # Metadata
    iteration: int
    max_iterations: int


def create_initial_state(query: str, session_id: str = "default") -> AgentState:
    """Create initial agent state"""
    return AgentState(
        messages=[],
        query=query,
        session_id=session_id,
        next_agent="supervisor",
        agents_used=[],
        rag_result={},
        search_result={},
        code_result={},
        tool_result={},
        final_answer="",
        citations=[],
        confidence=0.0,
        iteration=0,
        max_iterations=5
    )

