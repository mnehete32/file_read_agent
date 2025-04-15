# 🧠 Simple Agent using LangGraph + Gemini 2.5 + Tools

A conversational AI agent built with `LangGraph`, `Gemini 2.5`. This agent can process user inputs, respond using Gemini, and dynamically invoke tools like reading local files.

## 📦 Features

- Conversational AI with memory using LangGraph.
- Gemini 2.5 model from Google Generative AI.
- Tool support (e.g., file reading).
- Uses `rich` for a beautiful terminal UI.
- Handles tool invocations and returns tool results to the user.
- Interactive command-line interface.

---

## 🛠️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/mnehete32/file_read_agent.git
cd file_read_agent
```

### 2. Install dependencies, Python=3.11.4
```bash
pip install -r requirements.txt
```
### 3. Setup your .env
```bash
GEMINI_API_KEY=your_gemini_api_key
```

## 🚀 Running the Agent
```bash
python agent.py
```

## Preview
![](image/Screenshot%202025-04-15%20at%2022.55.03.png)
