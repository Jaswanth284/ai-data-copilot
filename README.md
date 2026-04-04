🚀 AI Data Copilot

An end-to-end AI-powered data assistant that enables users to query datasets using natural language.
Built using FastAPI, Streamlit, OpenAI, and a real Retrieval-Augmented Generation (RAG) pipeline.

🔥 Features
📊 Query CSV datasets using natural language
🧠 LLM-powered answer generation using OpenAI
🔍 RAG (Retrieval-Augmented Generation) using FAISS
⚡ FastAPI backend with structured APIs
🎨 Streamlit frontend for interactive usage
🌐 Fully deployed (Render + Streamlit Cloud)
📦 Supports dataset-based contextual answers (no hallucinations)
🧠 How It Works
User enters a question in the UI
Backend converts the question into embeddings
FAISS retrieves the most relevant dataset chunks
Retrieved chunks are passed to the LLM
LLM generates a grounded, accurate response

👉 This ensures context-aware answers instead of hallucinated responses

🏗️ Tech Stack
Backend: FastAPI
Frontend: Streamlit
LLM: OpenAI API
Vector DB: FAISS
Deployment: Render (Backend), Streamlit Cloud (Frontend)
🔗 Live Demo
🌐 Frontend: https://jaswanth-ai-copilot.streamlit.app/
⚙️ Backend API: https://ai-data-copilot-api.onrender.com/docs