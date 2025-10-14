"""
Vector store management with ChromaDB
"""
import os
import logging

# Disable ChromaDB telemetry BEFORE any imports
os.environ["ANONYMIZED_TELEMETRY"] = "False"

# Suppress ChromaDB telemetry errors
logging.getLogger("chromadb.telemetry.product.posthog").setLevel(logging.CRITICAL)

from typing import List, Dict, Any
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from core.embeddings import embedding_manager
from app.config import settings
import chromadb
from chromadb.config import Settings as ChromaSettings


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
            
            # Create client with telemetry disabled in settings
            client_settings = ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True
            )
            self._client = chromadb.PersistentClient(
                path=self.persist_dir,
                settings=client_settings
            )
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
    
    def _sanitize_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize metadata for ChromaDB compatibility"""
        clean_metadata = {}
        for key, value in metadata.items():
            # Convert key to string and remove special chars
            clean_key = str(key).replace('\x00', '').replace('\n', ' ')[:63]
            
            # Handle value types
            if value is None:
                continue  # Skip None values
            elif isinstance(value, (str, int, float, bool)):
                # Clean strings
                if isinstance(value, str):
                    clean_value = value.replace('\x00', '').replace('\r', ' ')[:512]
                else:
                    clean_value = value
                clean_metadata[clean_key] = clean_value
            else:
                # Convert other types to string
                clean_metadata[clean_key] = str(value)[:512]
        
        return clean_metadata
    
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
            
            # Sanitize all data first
            import uuid
            all_ids = []
            texts = [doc.page_content.replace('\x00', '') for doc in documents]
            metadatas_list = [self._sanitize_metadata(doc.metadata) for doc in documents]
            
            # Generate embeddings in batches
            print(f"[VectorStore] Generating embeddings in batches...")
            batch_size = 50
            all_embeddings = []
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i+batch_size]
                print(f"[VectorStore] Embedding batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")
                batch_embeddings = embeddings_model.embed_documents(batch_texts)
                all_embeddings.extend(batch_embeddings)
            print(f"[VectorStore] Generated {len(all_embeddings)} embeddings total")
            
            # Generate IDs
            ids = [str(uuid.uuid4()) for _ in range(len(documents))]
            
            # Add to ChromaDB using small batches (10 at a time) to avoid crash
            # ChromaDB has issues with both large batches and rapid individual upserts
            print(f"[VectorStore] Adding {len(documents)} documents in small batches...", flush=True)
            import sys, time
            
            batch_size_upsert = 10  # Very small batches
            for i in range(0, len(documents), batch_size_upsert):
                try:
                    end_idx = min(i + batch_size_upsert, len(documents))
                    batch_ids = ids[i:end_idx]
                    batch_embeddings = all_embeddings[i:end_idx]
                    batch_texts = texts[i:end_idx]
                    batch_metadatas = metadatas_list[i:end_idx]
                    
                    print(f"[VectorStore] Progress: {i}/{len(documents)} documents (batch {i//batch_size_upsert + 1}/{(len(documents)-1)//batch_size_upsert + 1})", flush=True)
                    sys.stdout.flush()
                    
                    # Use existing collection, don't recreate
                    collection.upsert(
                        ids=batch_ids,
                        embeddings=batch_embeddings,
                        documents=batch_texts,
                        metadatas=batch_metadatas
                    )
                    all_ids.extend(batch_ids)
                    
                    # Small delay to let ChromaDB persist
                    time.sleep(0.1)
                    
                except Exception as upsert_err:
                    print(f"[VectorStore][ERROR] Failed at batch {i//batch_size_upsert + 1}: {type(upsert_err).__name__}: {upsert_err}", flush=True)
                    import traceback
                    traceback.print_exc()
                    # Continue with remaining batches
                    continue
            
            print(f"[VectorStore] Successfully added {len(all_ids)} documents")
            
            # Final count check
            try:
                final_count = collection.count()
                print(f"[VectorStore] Total documents in collection: {final_count}")
            except Exception as e:
                print(f"[VectorStore] Final count unavailable: {e}")
            
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

