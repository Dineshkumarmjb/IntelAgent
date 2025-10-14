# IntelAgent Usage Guide

## 🚀 Getting Started

### Step 1: Installation

```bash
# Navigate to the project directory
cd IntelAgent/v1

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-actual-key-here
TAVILY_API_KEY=tvly-your-key-here  # Optional for web search
```

### Step 3: Run the Application

```bash
# Run Gradio UI (recommended)
python ui/gradio_app.py

# Or run FastAPI backend separately
python -m uvicorn app.main:app --reload
```

### Step 4: Access the UI

Open your browser and go to: **http://127.0.0.1:7860**

---

## 💬 Using the Chat Interface

### Example Queries

**Document Analysis:**
```
1. Upload a PDF in the "Document Upload" tab
2. Go to "Chat" tab
3. Ask: "Summarize the main points in this document"
4. Ask: "What are the key findings on page 5?"
```

**Web Search:**
```
- "What's the latest news about artificial intelligence?"
- "Search for the current price of Bitcoin"
- "What's the weather forecast for New York?"
```

**Code Execution:**
```
- "Write Python code to calculate the Fibonacci sequence up to 100"
- "Create a bar chart showing [10, 20, 30, 40, 50]"
- "Calculate the mean and standard deviation of [1, 2, 3, 4, 5]"
```

**Calculations:**
```
- "Calculate 15% of 1000"
- "What's the compound interest on $10,000 at 5% for 10 years?"
- "Calculate the NPV of cash flows [100, 200, 300] at 10% discount rate"
```

**General Chat:**
```
- "Explain quantum computing in simple terms"
- "What are the benefits of meditation?"
- "Tell me about the history of the internet"
```

---

## 📄 Document Management

### Supported Formats
- PDF (.pdf)
- Word (.docx, .doc)
- Text (.txt)

### Best Practices
1. **File Size**: Keep files under 50MB for optimal performance
2. **Quality**: Clear, text-based PDFs work best (not scanned images)
3. **Organization**: Upload related documents together for comparison
4. **Naming**: Use descriptive filenames

### Ingestion Process
1. Upload → Extract text → Chunk into pieces → Create embeddings → Store in ChromaDB

---

## 🔍 Advanced Features

### Multi-Agent Collaboration

The Supervisor Agent can route to multiple agents for complex queries:

```
Query: "Search for the latest Tesla earnings report and calculate the P/E ratio"

Flow:
1. Supervisor routes to SEARCH agent
2. SEARCH agent finds earnings data
3. Supervisor routes to CODE agent
4. CODE agent calculates P/E ratio
5. Results combined and returned
```

### Conversation Memory

The system remembers context within a session:

```
You: "What was Apple's revenue in 2023?"
Bot: "According to the document, Apple's revenue was $394.3B in 2023."

You: "How does that compare to 2022?"  # Context maintained!
Bot: "In 2022, revenue was $365.8B, so 2023 showed a 7.8% increase."
```

### Source Citations

Every RAG answer includes sources:

```
Answer: The revenue was $5.2M in Q3 2024.

Sources:
- [1] quarterly_report.pdf, page 3
- [2] financial_summary.pdf, page 12
```

---

## 🛠️ Troubleshooting

### Issue: "OpenAI API key not found"
**Solution:** 
- Create `.env` file in project root
- Add `OPENAI_API_KEY=your-key-here`
- Restart the application

### Issue: "No documents found"
**Solution:**
- Upload documents in the "Document Upload" tab first
- Wait for "Processing complete" message
- Then ask questions

### Issue: "Web search unavailable"
**Solution:**
- Web search requires Tavily API key
- Add `TAVILY_API_KEY=your-key-here` to `.env`
- Or questions will default to other agents

### Issue: "Code execution timeout"
**Solution:**
- Code is limited to 10 seconds execution
- Simplify complex calculations
- Adjust timeout in `.env`: `CODE_TIMEOUT_SECONDS=30`

### Issue: "Import Error"
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

---

## 📊 Performance Optimization

### For Large Documents
- Split very large PDFs into smaller sections
- Use specific page numbers in queries: "What's on page 5?"

### For Speed
- Use GPT-4o-mini (default) for faster responses
- Enable GPT-4o for complex reasoning by adjusting config

### For Cost
- GPT-4o-mini is 10x cheaper than GPT-4o
- Adjust `PRIMARY_MODEL` in `.env`

---

## 🔐 Security Notes

1. **Code Execution**: Sandboxed with timeouts and memory limits
2. **API Keys**: Store in `.env`, never commit to git
3. **File Uploads**: Validated for type and size
4. **Local Storage**: All data stored locally in `data/` folder

---

## 📝 API Usage

### Chat Endpoint

```python
import requests

response = requests.post("http://localhost:8000/api/chat", json={
    "query": "What's in this document?",
    "session_id": "user123"
})

print(response.json())
```

### Document Ingestion

```python
import requests

with open("report.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/ingest",
        files={"file": f}
    )

print(response.json())
```

### Get Status

```python
import requests

response = requests.get("http://localhost:8000/api/status")
print(response.json())
```

---

## 🎯 Example Workflows

### Financial Analysis
1. Upload 10-K reports for multiple companies
2. Ask: "Compare revenue growth across all companies"
3. Ask: "Which company has the best profit margin?"
4. Ask: "Calculate the average P/E ratio"

### Research Paper Review
1. Upload multiple research papers
2. Ask: "What are the common methodologies?"
3. Ask: "Summarize the key findings from each paper"
4. Ask: "What are the contradictions between studies?"

### Data Analysis
1. Upload CSV or Excel file (via code agent)
2. Ask: "Analyze this data and show trends"
3. Ask: "Create visualizations"
4. Ask: "Identify outliers"

---

## 🚧 Limitations

1. **Context Window**: Each query limited to ~4000 tokens of retrieved context
2. **File Size**: Maximum 50MB per file (configurable)
3. **Code Execution**: 10-second timeout, limited libraries
4. **Web Search**: Requires Tavily API key (limited free tier)
5. **Memory**: Session-based, cleared on restart

---

## 💡 Tips & Tricks

1. **Be Specific**: Instead of "Tell me about this", ask "What are the revenue figures in Q3?"
2. **Upload First**: Upload documents before asking questions
3. **Use Follow-ups**: Leverage conversation memory
4. **Combine Agents**: Ask complex queries that need multiple capabilities
5. **Check Sources**: Always verify source citations for accuracy

---

## 🤝 Getting Help

- Check logs in `logs/app.log`
- Review system status in UI
- Clear database if issues persist
- Restart application for fresh start

---

**Happy Agent Building! 🚀**

