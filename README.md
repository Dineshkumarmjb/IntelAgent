# 🤖 IntelAgent - Universal Multi-Agent AI System

> **A production-ready multi-agent orchestration platform that intelligently routes queries to specialized AI agents.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-brightgreen.svg)](https://openai.com/)

---

## 🎯 Overview

IntelAgent is a universal multi-agent AI system that automatically routes user queries to specialized agents based on intent. Built with Python, LangChain, OpenAI GPT-4, ChromaDB, and Tavily, it provides intelligent document analysis, web search, code execution, and natural conversation capabilities.

### ✨ Key Features

- **🧠 Intelligent Routing**: Supervisor agent analyzes queries and routes to optimal agent(s)
- **📄 Document Q&A**: RAG pipeline with ChromaDB vector database and source citations
- **🌐 Web Search**: Real-time information retrieval via Tavily API
- **💻 Code Execution**: Sandboxed Python execution with safety controls
- **🧮 Calculations**: Mathematical and financial computations
- **💬 Conversation Memory**: Context-aware multi-turn conversations
- **🔍 100% Source Attribution**: Every answer includes verifiable sources

---

## 🏗️ Architecture

```
User Query → Supervisor Agent → Specialized Agents → Unified Response
                    ↓
        ┌─────────────┬──────────────┬───────────────┬──────────┐
        ↓             ↓              ↓               ↓          ↓
    RAG Agent   Search Agent   Code Agent   Tool Agent   Chat Agent
        ↓             ↓              ↓               ↓          ↓
    ChromaDB     Tavily API    Sandboxed      Calculator    GPT-4
                                Python
```

### 🤖 Available Agents

1. **RAG Agent** - Document intelligence with vector search
2. **Search Agent** - Real-time web search and summarization
3. **Code Agent** - Python code generation and execution
4. **Tool Agent** - Mathematical and financial calculations
5. **Chat Agent** - General conversation and Q&A

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key
- (Optional) Tavily API key for web search

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd IntelAgent/final

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. Create `.env` file from template:
```bash
cp .env.example .env  # Windows: copy .env.example .env
```

2. Add your API keys to `.env`:
```env
OPENAI_API_KEY=sk-your-actual-key-here
TAVILY_API_KEY=tvly-your-key-here  # Optional
```

### Run the Application

```bash
# Start the Gradio UI
python ui/gradio_app.py

# Access at http://127.0.0.1:7860
```

---

## 📖 Usage Examples

### Document Analysis
```
1. Upload PDF/DOCX in "Document Upload" tab
2. Go to "Chat" tab
3. Ask: "What are the key findings in this document?"
   → RAG Agent provides answer with page citations
```

### Web Search
```
Ask: "What's the latest news about AI?"
→ Search Agent fetches real-time information with sources
```

### Code Execution
```
Ask: "Calculate the Fibonacci sequence up to 100"
→ Code Agent generates and executes Python code
```

### Calculations
```
Ask: "Calculate 15% of 1000"
→ Tool Agent performs calculation with explanation
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **LLM** | OpenAI GPT-4o, GPT-4o-mini |
| **Embeddings** | OpenAI text-embedding-3-small |
| **Vector DB** | ChromaDB |
| **Web Search** | Tavily API |
| **Framework** | LangChain, LangGraph |
| **Backend** | FastAPI |
| **Frontend** | Gradio |
| **Language** | Python 3.11+ |

---

## 📁 Project Structure

```
final/
├── agents/          # AI agent implementations
│   ├── supervisor.py    # Main orchestrator
│   ├── rag_agent.py     # Document Q&A
│   ├── search_agent.py  # Web search
│   ├── code_agent.py    # Code execution
│   ├── tool_agent.py    # Calculations
│   └── chat_agent.py    # General chat
├── core/            # Core functionality
│   ├── llm.py           # LLM management
│   ├── embeddings.py    # Embedding models
│   ├── vectorstore.py   # ChromaDB operations
│   └── memory.py        # Conversation memory
├── tools/           # Agent tools
│   ├── web_search.py    # Tavily integration
│   ├── code_executor.py # Sandboxed Python
│   └── calculator.py    # Math operations
├── utils/           # Utilities
│   ├── document_loader.py  # PDF/DOCX loading
│   ├── chunking.py         # Text splitting
│   └── prompts.py          # Prompt templates
├── app/             # FastAPI application
│   └── routers/         # API endpoints
├── ui/              # Gradio interface
│   └── gradio_app.py
└── requirements.txt
```

---

## 🔐 Security

- ✅ Sandboxed code execution with resource limits
- ✅ Input validation and sanitization
- ✅ API key encryption via environment variables
- ✅ No hardcoded credentials
- ✅ Gitignore prevents accidental key commits

---

## 📊 Use Cases

### Business & Finance
- Financial report analysis
- Investment research
- Metric calculations

### Research & Education
- Academic paper review
- Literature summarization
- Multi-document comparison

### Data Analysis
- CSV/Excel processing
- Statistical analysis
- Data visualization

### General Productivity
- Current events research
- Mathematical calculations
- Code generation

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI** for GPT-4 and embedding models
- **LangChain** for agent orchestration framework
- **ChromaDB** for vector database
- **Tavily** for web search API
- **Gradio** for the beautiful UI

---

## 📧 Contact

For questions and support, please open an issue on GitHub.

---

**Built with ❤️ using Python, LangChain, OpenAI, and ChromaDB**

⭐ Star this repo if you find it helpful!

