"""
RAG Agent for document-based question answering
"""
from typing import Dict, Any, List
from langchain.schema import Document
from core.llm import llm_manager
from core.vectorstore import vector_manager
from utils.prompts import RAG_SYSTEM_PROMPT
from utils.parsers import parse_citations


class RAGAgent:
    """Agent for document Q&A with RAG"""
    
    def __init__(self):
        self.llm = llm_manager.get_primary_llm()
        self.name = "RAG Agent"
    
    def process(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Process query using RAG
        
        Args:
            query: User question
            top_k: Number of documents to retrieve
        
        Returns:
            Dict with answer and citations
        """
        try:
            # Check if vector store has documents
            doc_count = vector_manager.get_document_count()
            
            if doc_count == 0:
                return {
                    'success': False,
                    'answer': "No documents have been uploaded yet. Please upload documents first.",
                    'citations': [],
                    'sources': []
                }
            
            # Retrieve relevant documents
            results = vector_manager.similarity_search_with_score(query, k=top_k)
            
            if not results:
                return {
                    'success': False,
                    'answer': "I couldn't find relevant information in the uploaded documents.",
                    'citations': [],
                    'sources': []
                }
            
            # Build context from retrieved documents
            context_parts = []
            sources = []
            
            for idx, (doc, score) in enumerate(results, 1):
                # Get metadata
                source_name = doc.metadata.get('source', 'Unknown')
                page = doc.metadata.get('page', 'N/A')
                
                # Add to context
                context_parts.append(
                    f"[Document {idx}] (Source: {source_name}, Page: {page})\n{doc.page_content}\n"
                )
                
                # Track sources
                sources.append({
                    'source': source_name,
                    'page': page,
                    'relevance_score': float(score)
                })
            
            context = "\n---\n".join(context_parts)
            
            # Create prompt
            prompt = f"""{RAG_SYSTEM_PROMPT}

Context from documents:
{context}

Question: {query}

Please provide a detailed answer based on the context above, and cite your sources."""
            
            # Get LLM response
            response = self.llm.invoke(prompt)
            answer = response.content
            
            # Parse citations from answer
            citations = parse_citations(answer)
            
            return {
                'success': True,
                'answer': answer,
                'citations': citations,
                'sources': sources
            }
        
        except Exception as e:
            return {
                'success': False,
                'answer': f"Error in RAG processing: {str(e)}",
                'citations': [],
                'sources': []
            }


# Global instance
rag_agent = RAGAgent()

