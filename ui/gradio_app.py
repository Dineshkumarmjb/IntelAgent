"""
Gradio UI for IntelAgent
"""
import sys
import os
from pathlib import Path

# Disable ChromaDB telemetry to avoid PostHog errors
os.environ["ANONYMIZED_TELEMETRY"] = "False"

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import gradio as gr
from agents.supervisor import supervisor
from core.vectorstore import vector_manager
from utils.document_loader import DocumentLoader
from utils.chunking import default_chunker
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def chat_with_agent(message, history, session_id="default"):
    """
    Chat function for Gradio interface
    
    Args:
        message: User message
        history: Chat history (list of tuples)
        session_id: Session identifier
    
    Returns:
        Updated history
    """
    if not message or not message.strip():
        return history
    
    try:
        # Process query
        result = supervisor.process(query=message, session_id=session_id)
        
        # Format response
        response = result['answer']
        
        # Add agent info
        agent_info = f"\n\n*[Handled by: {result['agent_used']}]*"
        
        # Add sources if available
        if result.get('sources'):
            sources_text = "\n\n**Sources:**\n"
            for idx, source in enumerate(result['sources'][:5], 1):
                if isinstance(source, dict):
                    if 'url' in source:
                        sources_text += f"{idx}. [{source.get('title', 'Source')}]({source['url']})\n"
                    else:
                        sources_text += f"{idx}. {source.get('source', 'Unknown')}, Page {source.get('page', 'N/A')}\n"
            response += sources_text
        
        response += agent_info
        
        # Append to history
        history.append((message, response))
        
        return history
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        error_response = f"Sorry, I encountered an error: {str(e)}"
        history.append((message, error_response))
        return history


def ingest_documents(files, progress=gr.Progress()):
    """
    Ingest documents into vector database
    
    Args:
        files: List of uploaded files
        progress: Gradio progress tracker
    
    Returns:
        Status message
    """
    if not files:
        return "No files uploaded."
    
    results = []
    total_chunks = 0
    
    for file_idx, file in enumerate(files):
        try:
            file_path = Path(file.name)
            filename = file_path.name
            
            progress(file_idx / len(files), desc=f"Processing {filename}...")
            logger.info(f"Processing file: {filename}")
            
            # Load document
            progress(file_idx / len(files), desc=f"Loading {filename}...")
            documents = DocumentLoader.load_document(file.name)
            logger.info(f"Loaded {len(documents)} pages/sections")
            
            # Chunk documents
            progress(file_idx / len(files), desc=f"Chunking {filename}...")
            chunks = default_chunker.chunk_documents(documents)
            logger.info(f"Created {len(chunks)} chunks")
            
            # Add metadata
            for chunk in chunks:
                chunk.metadata['source'] = filename
                if 'page' not in chunk.metadata:
                    chunk.metadata['page'] = 'N/A'
            
            # Add to vector store
            progress(file_idx / len(files), desc=f"Embedding {filename}...")
            logger.info("Adding to vector store...")
            vector_manager.add_documents(chunks)
            logger.info("Successfully added to vector store")
            
            total_chunks += len(chunks)
            results.append(f"✅ {filename}: {len(chunks)} chunks")
        
        except Exception as e:
            logger.error(f"Error processing {filename}: {str(e)}", exc_info=True)
            results.append(f"❌ {filename}: {str(e)}")
    
    progress(1.0, desc="Complete!")
    
    summary = f"**Ingestion Complete**\n\n"
    summary += f"Total chunks created: {total_chunks}\n\n"
    summary += "\n".join(results)
    
    logger.info(f"Ingestion complete: {total_chunks} total chunks")
    
    return summary


def get_system_status():
    """Get current system status"""
    try:
        doc_count = vector_manager.get_document_count()
        
        status = f"""**System Status**

📊 **Documents Indexed:** {doc_count} chunks

🤖 **Available Agents:**
- RAG Agent (Document Q&A)
- Search Agent (Web Search)
- Code Agent (Python Execution)
- Tool Agent (Calculations)
- Chat Agent (General Conversation)

✅ **Status:** Operational
"""
        return status
    
    except Exception as e:
        return f"Error getting status: {str(e)}"


def clear_database():
    """Clear all documents from database"""
    try:
        vector_manager.delete_collection()
        return "✅ Database cleared successfully!"
    except Exception as e:
        return f"❌ Error clearing database: {str(e)}"


# Create Gradio interface
with gr.Blocks(
    title="IntelAgent - Universal AI Assistant",
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="indigo"
    )
) as demo:
    
    gr.Markdown("""
    # 🤖 IntelAgent - Universal Multi-Agent Intelligence System
    
    Ask anything! Upload documents for analysis, search the web, execute code, or just chat.
    """)
    
    with gr.Tab("💬 Chat"):
        gr.Markdown("""
        ### Intelligent Chat Interface
        
        The supervisor agent will automatically route your query to the best agent(s):
        - **Document questions** → RAG Agent
        - **Current events/search** → Search Agent  
        - **Code/calculations** → Code Agent
        - **Simple math** → Tool Agent
        - **General chat** → Chat Agent
        """)
        
        chatbot = gr.Chatbot(
            height=500,
            label="Conversation",
            show_label=True,
            avatar_images=(None, "🤖")
        )
        
        with gr.Row():
            msg_input = gr.Textbox(
                placeholder="Ask me anything...",
                label="Your Message",
                scale=4
            )
            submit_btn = gr.Button("Send", variant="primary", scale=1)
        
        with gr.Row():
            clear_btn = gr.Button("Clear Chat", variant="secondary")
        
        # Examples
        gr.Examples(
            examples=[
                "What's in the uploaded document?",
                "Search for the latest AI news",
                "Calculate 15% of 1000",
                "Write Python code to calculate fibonacci numbers",
                "Hello! How are you?",
            ],
            inputs=msg_input
        )
        
        # Chat functionality
        msg_input.submit(
            chat_with_agent,
            inputs=[msg_input, chatbot],
            outputs=[chatbot]
        ).then(
            lambda: "",
            outputs=[msg_input]
        )
        
        submit_btn.click(
            chat_with_agent,
            inputs=[msg_input, chatbot],
            outputs=[chatbot]
        ).then(
            lambda: "",
            outputs=[msg_input]
        )
        
        clear_btn.click(lambda: [], outputs=[chatbot])
    
    with gr.Tab("📄 Document Upload"):
        gr.Markdown("""
        ### Upload Documents for Analysis
        
        Upload PDF, DOCX, or TXT files. The system will:
        1. Extract text content
        2. Split into chunks
        3. Create embeddings
        4. Store in vector database
        
        Then you can ask questions about the documents in the Chat tab!
        """)
        
        file_upload = gr.File(
            label="Upload Documents",
            file_count="multiple",
            file_types=[".pdf", ".docx", ".doc", ".txt"]
        )
        
        ingest_btn = gr.Button("Process Documents", variant="primary")
        ingest_status = gr.Markdown()
        
        ingest_btn.click(
            ingest_documents,
            inputs=[file_upload],
            outputs=[ingest_status]
        )
    
    with gr.Tab("⚙️ System Status"):
        gr.Markdown("""
        ### System Information
        
        View system status and manage the document database.
        """)
        
        status_display = gr.Markdown()
        
        with gr.Row():
            refresh_btn = gr.Button("Refresh Status", variant="secondary")
            clear_db_btn = gr.Button("Clear Database", variant="stop")
        
        clear_status = gr.Markdown()
        
        refresh_btn.click(
            get_system_status,
            outputs=[status_display]
        )
        
        clear_db_btn.click(
            clear_database,
            outputs=[clear_status]
        ).then(
            get_system_status,
            outputs=[status_display]
        )
        
        # Load status on page load
        demo.load(get_system_status, outputs=[status_display])
    
    with gr.Tab("📖 Documentation"):
        gr.Markdown("""
        ## 📚 How to Use IntelAgent
        
        ### 🤖 Available Agents
        
        1. **RAG Agent** - Document Intelligence
           - Upload PDFs, Word docs, or text files
           - Ask questions about the content
           - Get answers with source citations
           - Example: "What was the revenue in Q3 2024?"
        
        2. **Search Agent** - Web Search
           - Get real-time information from the internet
           - Stays up-to-date with current events
           - Example: "What's the latest news about AI?"
        
        3. **Code Agent** - Python Execution
           - Run Python code securely
           - Data analysis and visualization
           - Example: "Create a bar chart of [1,2,3,4,5]"
        
        4. **Tool Agent** - Calculations & Utilities
           - Mathematical calculations
           - Financial formulas (NPV, ROI, etc.)
           - Example: "Calculate 15% of 1000"
        
        5. **Chat Agent** - General Conversation
           - Natural conversation
           - Helpful information
           - Example: "Explain quantum computing"
        
        ---
        
        ### 💡 Tips
        
        - **Be specific**: More details = better answers
        - **Upload first**: Upload documents before asking about them
        - **Combine queries**: "Search for Tesla stock and calculate P/E ratio"
        - **Follow up**: The system remembers conversation context
        
        ---
        
        ### 🎯 Example Use Cases
        
        **Finance:**
        - Analyze financial reports
        - Calculate investment metrics
        - Compare company performances
        
        **Research:**
        - Summarize academic papers
        - Extract key findings
        - Compare multiple documents
        
        **Coding:**
        - Analyze data from CSV files
        - Create visualizations
        - Perform statistical analysis
        
        **General:**
        - Get current information
        - Solve math problems
        - General knowledge questions
        
        ---
        
        ### ⚡ Quick Start
        
        1. Go to **Document Upload** tab
        2. Upload some documents
        3. Go to **Chat** tab
        4. Ask questions about your documents!
        
        ---
        
        ### 🔐 Privacy & Security
        
        - Code execution is sandboxed
        - All data stored locally
        - API keys kept secure
        - No data sent to third parties (except OpenAI/Tavily APIs)
        """)
    
    gr.Markdown("""
    ---
    **IntelAgent v1.0** | Built with LangChain, OpenAI, and Gradio
    """)


if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True
    )

