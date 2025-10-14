"""
Example usage of IntelAgent programmatically
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.supervisor import supervisor
from core.vectorstore import vector_manager
from utils.document_loader import DocumentLoader
from utils.chunking import default_chunker


def example_chat():
    """Example: Simple chat"""
    print("="*50)
    print("Example 1: Simple Chat")
    print("="*50)
    
    result = supervisor.process(
        query="Hello! What can you help me with?",
        session_id="example1"
    )
    
    print(f"Agent Used: {result['agent_used']}")
    print(f"Answer: {result['answer']}")
    print()


def example_calculation():
    """Example: Calculation"""
    print("="*50)
    print("Example 2: Calculation")
    print("="*50)
    
    result = supervisor.process(
        query="Calculate 15% of 1000",
        session_id="example2"
    )
    
    print(f"Agent Used: {result['agent_used']}")
    print(f"Answer: {result['answer']}")
    print()


def example_code_execution():
    """Example: Code execution"""
    print("="*50)
    print("Example 3: Code Execution")
    print("="*50)
    
    result = supervisor.process(
        query="Write Python code to calculate the first 10 Fibonacci numbers",
        session_id="example3"
    )
    
    print(f"Agent Used: {result['agent_used']}")
    print(f"Answer: {result['answer'][:500]}...")  # Truncate for display
    print()


def example_web_search():
    """Example: Web search"""
    print("="*50)
    print("Example 4: Web Search")
    print("="*50)
    
    result = supervisor.process(
        query="What are the latest developments in AI?",
        session_id="example4"
    )
    
    print(f"Agent Used: {result['agent_used']}")
    print(f"Answer: {result['answer'][:300]}...")  # Truncate for display
    if result.get('sources'):
        print(f"Sources found: {len(result['sources'])}")
    print()


def example_document_qa():
    """Example: Document Q&A"""
    print("="*50)
    print("Example 5: Document Q&A")
    print("="*50)
    
    # First, check if any documents are loaded
    doc_count = vector_manager.get_document_count()
    
    if doc_count == 0:
        print("No documents loaded. Upload documents first!")
        print("You can upload documents via:")
        print("1. Gradio UI (recommended)")
        print("2. FastAPI endpoint: POST /api/ingest")
        print()
        return
    
    result = supervisor.process(
        query="What are the main topics discussed in the documents?",
        session_id="example5"
    )
    
    print(f"Agent Used: {result['agent_used']}")
    print(f"Answer: {result['answer'][:300]}...")
    if result.get('sources'):
        print(f"\nSources:")
        for source in result['sources'][:3]:
            print(f"  - {source}")
    print()


def example_conversation_context():
    """Example: Conversation with context"""
    print("="*50)
    print("Example 6: Conversation Context")
    print("="*50)
    
    # First question
    result1 = supervisor.process(
        query="What is machine learning?",
        session_id="context_example"
    )
    print("Q1: What is machine learning?")
    print(f"A1: {result1['answer'][:200]}...")
    print()
    
    # Follow-up question (uses context)
    result2 = supervisor.process(
        query="Can you give me an example?",  # "example" refers to ML from previous context
        session_id="context_example"
    )
    print("Q2: Can you give me an example?")
    print(f"A2: {result2['answer'][:200]}...")
    print()


def example_ingest_document(file_path: str):
    """
    Example: Programmatically ingest a document
    
    Args:
        file_path: Path to document file
    """
    print("="*50)
    print("Example 7: Document Ingestion")
    print("="*50)
    
    try:
        # Check if file exists
        if not Path(file_path).exists():
            print(f"File not found: {file_path}")
            print("Please provide a valid file path")
            return
        
        # Load document
        print(f"Loading document: {file_path}")
        documents = DocumentLoader.load_document(file_path)
        print(f"Loaded {len(documents)} pages/sections")
        
        # Chunk documents
        print("Chunking document...")
        chunks = default_chunker.chunk_documents(documents)
        print(f"Created {len(chunks)} chunks")
        
        # Add metadata
        filename = Path(file_path).name
        for chunk in chunks:
            chunk.metadata['source'] = filename
        
        # Add to vector store
        print("Adding to vector database...")
        ids = vector_manager.add_documents(chunks)
        print(f"Successfully added {len(ids)} chunks to database")
        
        # Verify
        total_docs = vector_manager.get_document_count()
        print(f"Total documents in database: {total_docs}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    print()


def main():
    """Run all examples"""
    print("\n" + "="*50)
    print("  IntelAgent - Example Usage")
    print("="*50 + "\n")
    
    # Run examples
    example_chat()
    example_calculation()
    example_code_execution()
    
    # Web search (may fail if no Tavily key)
    try:
        example_web_search()
    except Exception as e:
        print(f"Web search example skipped: {e}\n")
    
    # Document Q&A
    example_document_qa()
    
    # Conversation context
    example_conversation_context()
    
    # Document ingestion (optional - provide your own file)
    # example_ingest_document("path/to/your/document.pdf")
    
    print("="*50)
    print("Examples complete!")
    print("="*50)


if __name__ == "__main__":
    main()

