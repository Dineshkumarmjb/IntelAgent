# 🚀 Quick Start Guide - IntelAgent

Get up and running in 5 minutes!

## Step 1: Setup (2 minutes)

### Windows:
```bash
# Double-click setup.bat or run in terminal:
setup.bat
```

### Mac/Linux:
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configure (1 minute)

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # Mac/Linux
   ```

2. Edit `.env` and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

3. (Optional) Add Tavily API key for web search:
   ```env
   TAVILY_API_KEY=tvly-your-key-here
   ```

## Step 3: Run (30 seconds)

### Windows:
```bash
run.bat
```

### Mac/Linux:
```bash
source venv/bin/activate
python ui/gradio_app.py
```

## Step 4: Use! (Right away)

1. Open browser: **http://127.0.0.1:7860**

2. Try these examples:
   - **Chat**: "Hello! What can you do?"
   - **Calculate**: "What's 15% of 1000?"
   - **Code**: "Calculate first 10 Fibonacci numbers"
   - **Upload**: Drop a PDF in the "Document Upload" tab
   - **Ask**: "What's in this document?"

---

## 🎯 Common Use Cases

### Financial Analysis
```
1. Upload: quarterly_report.pdf
2. Ask: "What was the revenue in Q3?"
3. Ask: "Calculate the YoY growth rate"
```

### Research
```
1. Upload: research_paper.pdf
2. Ask: "Summarize the methodology"
3. Ask: "What are the key findings?"
```

### Data Analysis
```
Ask: "Write Python code to calculate mean of [1,2,3,4,5]"
Ask: "Create a bar chart showing sales data"
```

### Current Events
```
Ask: "What's the latest news about AI?"
Ask: "Search for current Bitcoin price"
```

---

## 🆘 Troubleshooting

**"OpenAI API key not found"**
→ Make sure `.env` file exists with `OPENAI_API_KEY`

**"Module not found"**
→ Run `pip install -r requirements.txt`

**"No documents found"**
→ Upload documents in "Document Upload" tab first

---

## ✅ You're Ready!

The system will automatically:
- Route queries to the right agent
- Remember conversation context
- Cite sources for answers
- Handle complex multi-step tasks

**Have fun exploring! 🎉**

