"""
Output parsing utilities
"""
import re
from typing import Dict, List, Any


def parse_citations(text: str) -> Dict[str, List[str]]:
    """Extract citations from text"""
    citations = {}
    
    # Pattern: [Source: filename, page X]
    pattern = r'\[Source:\s*([^,]+),\s*page\s*(\d+)\]'
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    for idx, (filename, page) in enumerate(matches, 1):
        citations[str(idx)] = f"{filename.strip()}, page {page}"
    
    # Alternative pattern: - [Source with URL]
    url_pattern = r'-\s*\[([^\]]+)\]\s*\(([^)]+)\)'
    url_matches = re.findall(url_pattern, text)
    
    for idx, (title, url) in enumerate(url_matches, len(citations) + 1):
        citations[str(idx)] = f"{title.strip()}: {url}"
    
    return citations


def extract_code_blocks(text: str) -> List[str]:
    """Extract code blocks from text"""
    pattern = r'```python\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches


def format_agent_response(
    answer: str,
    agent_name: str,
    citations: List[str] = None
) -> Dict[str, Any]:
    """Format agent response"""
    response = {
        "answer": answer,
        "agent": agent_name,
        "citations": citations or []
    }
    return response

