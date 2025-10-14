"""
Vector store management with ChromaDB
"""
from typing import List, Dict, Any
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from core.embeddings import embedding_manager
from app.config import settings
import chromadb
from chromadb.config import Settings as ChromaSettings
import os


class VectorStoreManager:
    """Manages vector database operations"""
    
    def __init__(self):
        self.persist_dir = settings.CHROMA_PERSIST_DIR
        self.collection_name = settings.COLLECTION_NAME
        self._vectorstore = None
        self._client = None
        
        # Create persist directory if it doesn't exist
        Path(self.persist_dir).mkdir(parents=True, exist_ok=True)
    
    def get_client(self):
        """Get ChromaDB client directly (like FinBot_Final)"""
        if self._client is None:
            # Disable telemetry
            os.environ["ANONYMIZED_TELEMETRY"] = "False"
            print(f"[ChromaDB] Using path: {self.persist_dir}")
            self._client = chromadb.PersistentClient(path=self.persist_dir)
        return self._client
    
    def get_collection(self):
        """Get or create collection directly"""
        client = self.get_client()
        collection = client.get_or_create_collection(name=self.collection_name)
        print(f"[ChromaDB] Collection '{self.collection_name}' count = {collection.count()}")
        return collection
    
    def get_vectorstore(self) -> Chroma:
        """Get or create vector store (for LangChain compatibility)"""
        if self._vectorstore is None:
            # Disable telemetry to avoid PostHog errors
            os.environ["ANONYMIZED_TELEMETRY"] = "False"
            
            # Initialize using direct client first
            client = self.get_client()
            collection = self.get_collection()
            
            # Now create LangChain wrapper
            self._vectorstore = Chroma(
                client=client,
                collection_name=self.collection_name,
                embedding_function=embedding_manager.get_embeddings()
            )
        return self._vectorstore
    
    def add_documents(
        self, 
        documents: List[Document],
        metadatas: List[Dict[str, Any]] = None
    ) -> List[str]:
        """Add documents to vector store (hybrid approach)"""
        try:
            print(f"[VectorStore] Adding {len(documents)} documents...")
            
            # Add metadata if provided
            if metadatas:
                for doc, metadata in zip(documents, metadatas):
                    doc.metadata.update(metadata)
            
            # Get collection directly (like FinBot_Final)
            collection = self.get_collection()
            embeddings_model = embedding_manager.get_embeddings()
            
            # Process in batches
            batch_size = 50
            all_ids = []
            
            for i in range(0, len(documents), batch_size):
                batch = documents[i:i + batch_size]
                print(f"[VectorStore] Processing batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1} ({len(batch)} documents)")
                
                # Generate embeddings
                texts = [doc.page_content for doc in batch]
                metadatas_batch = [doc.metadata for doc in batch]
                
                print(f"[VectorStore] Generating embeddings...")
                embeddings = embeddings_model.embed_documents(texts)
                print(f"[VectorStore] Generated {len(embeddings)} embeddings")
                
                # Create IDs
                import uuid
                ids = [str(uuid.uuid4()) for _ in range(len(batch))]
                
                # Add to collection using upsert (safer)
                print(f"[VectorStore] Adding to ChromaDB...")
                collection.upsert(
                    ids=ids,
                    embeddings=embeddings,
                    documents=texts,
                    metadatas=metadatas_batch
                )
                
                all_ids.extend(ids)
                print(f"[VectorStore] Batch added. Total count: {collection.count()}")
            
            print(f"[VectorStore] Successfully added {len(all_ids)} documents")
            print(f"[VectorStore] Total documents in collection: {collection.count()}")
            
            return all_ids
            
        except Exception as e:
            print(f"[VectorStore][ERROR] Failed to add documents: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def similarity_search(
        self,
        query: str,
        k: int = 5,
        filter_dict: Dict[str, Any] = None
    ) -> List[Document]:
        """Search for similar documents"""
        vectorstore = self.get_vectorstore()
        
        if filter_dict:
            results = vectorstore.similarity_search(
                query, 
                k=k,
                filter=filter_dict
            )
        else:
            results = vectorstore.similarity_search(query, k=k)
        
        return results
    
    def similarity_search_with_score(
        self,
        query: str,
        k: int = 5
    ) -> List[tuple]:
        """Search with relevance scores"""
        vectorstore = self.get_vectorstore()
        return vectorstore.similarity_search_with_score(query, k=k)
    
    def delete_collection(self):
        """Delete the entire collection"""
        if self._vectorstore:
            self._vectorstore.delete_collection()
            self._vectorstore = None
    
    def get_document_count(self) -> int:
        """Get total number of documents"""
        try:
            collection = self.get_collection()
            return collection.count()
        except Exception as e:
            print(f"[VectorStore] Error getting count: {e}")
            return 0


# Global instance
vector_manager = VectorStoreManager()

