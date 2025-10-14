"""
Document loading utilities
"""
from typing import List
from pathlib import Path
from langchain.schema import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader
)


class DocumentLoader:
    """Load documents from various formats"""
    
    @staticmethod
    def load_pdf(file_path: str) -> List[Document]:
        """Load PDF document"""
        loader = PyPDFLoader(file_path)
        return loader.load()
    
    @staticmethod
    def load_txt(file_path: str) -> List[Document]:
        """Load text document"""
        loader = TextLoader(file_path)
        return loader.load()
    
    @staticmethod
    def load_docx(file_path: str) -> List[Document]:
        """Load Word document"""
        loader = Docx2txtLoader(file_path)
        return loader.load()
    
    @staticmethod
    def load_document(file_path: str) -> List[Document]:
        """Load document based on file extension"""
        file_path_obj = Path(file_path)
        extension = file_path_obj.suffix.lower()
        
        loaders = {
            '.pdf': DocumentLoader.load_pdf,
            '.txt': DocumentLoader.load_txt,
            '.docx': DocumentLoader.load_docx,
            '.doc': DocumentLoader.load_docx,
        }
        
        if extension not in loaders:
            raise ValueError(f"Unsupported file format: {extension}")
        
        return loaders[extension](file_path)

