# 🐾 AI Study Assistant

> A locally running AI-powered study tool that learns from your own class notes and quizzes you on them.

No cloud. No API keys. Runs entirely on your machine using a local LLM.

## Why I Built This
Studying from notes is slow. I wanted a tool that could answer questions *based on my actual class material* — not generic internet answers. So I built one.

## Features
- 💬 Chat with an AI about any subject using your own notes as context
- 📚 Upload class notes in PDF or TXT format
- 🧠 Persistent memory between study sessions
- 📝 Quiz mode — generates practice questions from your notes
- 🎯 Subject-specific assistants

## Tech Stack
| Tool | Purpose |
|---|---|
| Python | Core language |
| Ollama | Local LLM runner |
| LLaMA 3.2 (3B) | AI model (runs offline) |
| Streamlit | Web UI |
| pypdf | PDF parsing |

## How to Run
```bash
# 1. Install Ollama
# https://ollama.com

# 2. Pull the model
ollama pull llama3.2

# 3. Install Python dependencies
pip install streamlit pypdf

# 4. Run the app
python -m streamlit run app.py
```
Then open http://localhost:8501 in your browser.

## What I Learned
- Integrating local LLMs into a real Python application
- Building document-aware AI context (RAG-style)
- Designing a practical tool that solves an actual problem

## Contact
- Email: kostiantyn_pa@gmail.com  
- LinkedIn: https://www.linkedin.com/in/kostiantynpavlyshyn/
