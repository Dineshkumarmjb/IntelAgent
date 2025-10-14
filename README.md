# 🤖 IntelAgent v1 - Universal Multi-Agent Intelligence System

> **"One Agent System, Infinite Possibilities"**

A production-ready multi-agent orchestration platform that intelligently routes queries to specialized AI agents for document analysis, web search, code execution, and more.

---

## 🚀 Quick Start

### 1. Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:

```env
# OpenAI API Key (required)
OPENAI_API_KEY=your_openai_api_key_here

# Tavily API Key (optional, for web search)
TAVILY_API_KEY=your_tavily_api_key_here

# Model Configuration
PRIMARY_MODEL=gpt-4o-mini
ADVANCED_MODEL=gpt-4o
EMBEDDING_MODEL=text-embedding-3-small

# Temperature
TEMPERATURE=0.1

# Vector DB
CHROMA_PERSIST_DIR=./data/chroma_db

# File Storage
UPLOAD_DIR=./data/uploads
```

### 3. Run the Application

**Option 1: Run Both (Recommended)**
```bash
# Terminal 1: Start FastAPI backend
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2: Start Gradio UI
python ui/gradio_app.py
```

**Option 2: UI Only (Gradio has built-in server)**
```bash
python ui/gradio_app.py
```

### 4. Access the UI

Open your browser and go to: **http://127.0.0.1:7860**

---

## 🧩 Features

✅ **Multi-Agent System** - 10 specialized agents working together  
✅ **Document Intelligence** - Upload PDFs, DOCX, TXT and ask questions  
✅ **Web Search** - Real-time information from the internet  
✅ **Code Execution** - Run Python code securely  
✅ **Source Citations** - Every answer shows its sources  
✅ **Conversation Memory** - Maintains context across queries  
✅ **Multi-Modal** - Text, voice, and image support  
✅ **Universal** - Works with any domain (finance, legal, medical, etc.)  

---

## 🤖 Available Agents

1. **RAG Agent** - Document Q&A with citations
2. **Search Agent** - Real-time web search
3. **Code Agent** - Python code execution
4. **SQL Agent** - Database queries
5. **File Agent** - Document processing
6. **Vision Agent** - Image analysis
7. **API Agent** - External integrations
8. **Memory Agent** - Context management
9. **Tool Agent** - Calculations & utilities
10. **Supervisor Agent** - Orchestrates everything

---

## 📖 Usage Examples

### Example 1: Document Analysis
```
User: Upload a PDF report
Agent: "Document ingested successfully!"

User: "What was the revenue in Q3?"
RAG Agent: "According to the report, Q3 revenue was $5.2M, up 15% YoY."
[Source: report.pdf, page 3]
```

### Example 2: Web Search + Code
```
User: "Get the latest stock price for AAPL and calculate the P/E ratio"
Search Agent: Fetches current price
Code Agent: Calculates P/E ratio
Response: "AAPL current price: $178.25, P/E ratio: 29.4"
```

### Example 3: Multi-Step Reasoning
```
User: "Compare revenue across my 3 uploaded financial reports"
Supervisor: Routes to RAG Agent for multi-document analysis
RAG Agent: Extracts data from all 3 documents
Response: Table comparing revenues with sources
```

---

## 🏗️ Architecture

```
User Query → Supervisor Agent → Routes to Specialized Agents → Response with Citations
```

See [ARCHITECTURE_v2.md](../ARCHITECTURE_v2.md) for detailed architecture.

---

## 📁 Project Structure

```
v1/
├── README.md
├── requirements.txt
├── .env.example
├── app/                    # FastAPI backend
│   ├── main.py
│   ├── config.py
│   └── routers/
├── agents/                 # All agent implementations
│   ├── supervisor.py
│   ├── rag_agent.py
│   └── ...
├── core/                   # Core utilities
│   ├── llm.py
│   ├── vectorstore.py
│   └── ...
├── tools/                  # Agent tools
│   ├── web_search.py
│   └── ...
├── utils/                  # Helper functions
├── ui/                     # Gradio interface
│   └── gradio_app.py
└── data/                   # Storage
    ├── chroma_db/
    └── uploads/
```

---

## 🔐 Security

- Sandboxed code execution with resource limits
- Input validation and sanitization
- No sensitive data logging
- API key encryption

---

## 💰 Cost Optimization

- Uses GPT-4o-mini for most queries (10x cheaper)
- GPT-4o only for complex reasoning
- Efficient embedding caching
- Hybrid search reduces LLM calls

---

## 🐛 Troubleshooting

### Issue: "No API key found"
**Solution**: Make sure `.env` file exists with `OPENAI_API_KEY`

### Issue: "Module not found"
**Solution**: `pip install -r requirements.txt`

### Issue: "ChromaDB error"
**Solution**: Delete `data/chroma_db` folder and re-ingest documents

---

## 📝 License

MIT License - See LICENSE file

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## 📧 Support

For issues and questions, please open a GitHub issue.

---

**Built with ❤️ using LangGraph, OpenAI, and ChromaDB**

