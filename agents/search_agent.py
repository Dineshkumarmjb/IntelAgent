"""
Search Agent for web search
"""
from typing import Dict, Any
from core.llm import llm_manager
from tools.web_search import web_search_tool
from utils.prompts import SEARCH_SYSTEM_PROMPT


class SearchAgent:
    """Agent for web search"""
    
    def __init__(self):
        self.llm = llm_manager.get_primary_llm()
        self.name = "Search Agent"
    
    def process(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Process query using web search
        
        Args:
            query: Search query
            max_results: Max number of results
        
        Returns:
            Dict with answer and sources
        """
        try:
            # Perform web search
            search_results = web_search_tool.search(query, max_results=max_results)
            
            if not search_results or search_results[0].get('title') == 'Web search unavailable':
                return {
                    'success': False,
                    'answer': search_results[0].get('content', 'Web search is not available.'),
                    'sources': []
                }
            
            # Format search results for LLM
            context = web_search_tool.format_results(search_results)
            
            # Create prompt
            prompt = f"""{SEARCH_SYSTEM_PROMPT}

Search Results:
{context}

User Query: {query}

Please provide a comprehensive answer based on the search results above."""
            
            # Get LLM response
            response = self.llm.invoke(prompt)
            answer = response.content
            
            # Format sources
            sources = [
                {
                    'title': result['title'],
                    'url': result['url'],
                    'snippet': result['content'][:200] + '...' if len(result['content']) > 200 else result['content']
                }
                for result in search_results
            ]
            
            return {
                'success': True,
                'answer': answer,
                'sources': sources
            }
        
        except Exception as e:
            return {
                'success': False,
                'answer': f"Error in search processing: {str(e)}",
                'sources': []
            }


# Global instance
search_agent = SearchAgent()

