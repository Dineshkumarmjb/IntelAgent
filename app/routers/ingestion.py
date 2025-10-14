"""
Document ingestion endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
from pathlib import Path
from app.config import settings
from utils.document_loader import DocumentLoader
from utils.chunking import default_chunker
from core.vectorstore import vector_manager

router = APIRouter()


@router.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    """
    Ingest a document into the vector database
    
    Args:
        file: Uploaded file (PDF, DOCX, TXT)
    
    Returns:
        Status and metadata
    """
    try:
        # Validate file type
        allowed_extensions = ['.pdf', '.docx', '.doc', '.txt']
        file_ext = Path(file.filename).suffix.lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_ext}. Allowed: {allowed_extensions}"
            )
        
        # Save file temporarily
        upload_path = Path(settings.UPLOAD_DIR) / file.filename
        
        with open(upload_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Check file size
        file_size_mb = len(content) / (1024 * 1024)
        if file_size_mb > settings.MAX_FILE_SIZE_MB:
            os.remove(upload_path)
            raise HTTPException(
                status_code=400,
                detail=f"File too large: {file_size_mb:.2f}MB. Max: {settings.MAX_FILE_SIZE_MB}MB"
            )
        
        # Load document
        documents = DocumentLoader.load_document(str(upload_path))
        
        # Chunk documents
        chunks = default_chunker.chunk_documents(documents)
        
        # Add metadata
        for chunk in chunks:
            chunk.metadata['source'] = file.filename
            if 'page' not in chunk.metadata:
                chunk.metadata['page'] = 'N/A'
        
        # Add to vector store
        ids = vector_manager.add_documents(chunks)
        
        return {
            "success": True,
            "filename": file.filename,
            "file_size_mb": round(file_size_mb, 2),
            "chunks_created": len(chunks),
            "document_ids": ids[:5] + ['...'] if len(ids) > 5 else ids
        }
    
    except HTTPException:
        raise
    except Exception as e:
        if upload_path.exists():
            os.remove(upload_path)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest/batch")
async def ingest_multiple_documents(files: List[UploadFile] = File(...)):
    """
    Ingest multiple documents
    
    Args:
        files: List of uploaded files
    
    Returns:
        Status for each file
    """
    results = []
    
    for file in files:
        try:
            result = await ingest_document(file)
            results.append({
                "filename": file.filename,
                "success": True,
                "details": result
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })
    
    return {
        "total_files": len(files),
        "successful": sum(1 for r in results if r['success']),
        "failed": sum(1 for r in results if not r['success']),
        "results": results
    }


@router.get("/documents")
async def get_document_status():
    """Get status of ingested documents"""
    try:
        doc_count = vector_manager.get_document_count()
        
        # List uploaded files
        upload_dir = Path(settings.UPLOAD_DIR)
        uploaded_files = [f.name for f in upload_dir.iterdir() if f.is_file()]
        
        return {
            "total_chunks": doc_count,
            "uploaded_files": uploaded_files,
            "file_count": len(uploaded_files)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/documents")
async def clear_all_documents():
    """Clear all documents from vector database"""
    try:
        vector_manager.delete_collection()
        
        # Optionally clear uploaded files
        upload_dir = Path(settings.UPLOAD_DIR)
        for file in upload_dir.iterdir():
            if file.is_file():
                os.remove(file)
        
        return {
            "success": True,
            "message": "All documents cleared"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

