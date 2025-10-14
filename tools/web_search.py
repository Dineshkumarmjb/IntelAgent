"""
Web search tool using Tavily
"""
from typing import List, Dict, Any
from app.config import settings

try:
    from tavily import TavilyClient
    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False


class WebSearchTool:
    """Web search using Tavily API"""
    
    def __init__(self):
        self.api_key = settings.TAVILY_API_KEY
        self.client = None
        
        if TAVILY_AVAILABLE and self.api_key and self.api_key != "your_tavily_api_key_here":
            try:
                self.client = TavilyClient(api_key=self.api_key)
            except Exception as e:
                print(f"Tavily initialization failed: {e}")
    
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search the web"""
        if not self.client:
            return [{
                "title": "Web search unavailable",
                "content": "Tavily API key not configured. Please set TAVILY_API_KEY in .env file.",
                "url": ""
            }]
        
        try:
            response = self.client.search(
                query=query,
                max_results=max_results
            )
            
            results = []
            for item in response.get('results', []):
                results.append({
                    "title": item.get('title', ''),
                    "content": item.get('content', ''),
                    "url": item.get('url', '')
                })
            
            return results
        
        except Exception as e:
            return [{
                "title": "Search error",
                "content": f"Error performing web search: {str(e)}",
                "url": ""
            }]
    
    def format_results(self, results: List[Dict[str, Any]]) -> str:
        """Format search results as text"""
        if not results:
            return "No results found."
        
        formatted = []
        for idx, result in enumerate(results, 1):
            formatted.append(
                f"{idx}. {result['title']}\n"
                f"   {result['content']}\n"
                f"   URL: {result['url']}\n"
            )
        
        return "\n".join(formatted)


# Global instance
web_search_tool = WebSearchTool()

