"""
Text chunking utilities
"""
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


class TextChunker:
    """Chunk text documents"""
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Chunk documents into smaller pieces"""
        return self.splitter.split_documents(documents)
    
    def chunk_text(self, text: str) -> List[str]:
        """Chunk plain text"""
        return self.splitter.split_text(text)


# Default chunker instance
default_chunker = TextChunker()

