# 🤖 Private RAG Chatbot: Full-Stack Document Assistant

A complete Retrieval-Augmented Generation (RAG) system that allows you to upload PDF/TXT documents and chat with them locally and securely. This project uses a 100% local AI pipeline to ensure data privacy.

## 🚀 Key Features
- **Full-Stack Architecture:** FastAPI backend with a modern Streamlit frontend  
- **Privacy-First:** Uses local LLMs (FLAN-T5) and embeddings — no external API costs or data leaks  
- **Smart Retrieval:** Optimized recursive chunking and vector search using ChromaDB  
- **Secure API:** Protected endpoints using X-API-Key header authentication  
- **Multi-Page Support:** Tracks and displays exactly which page information was retrieved from  

## 🛠️ Tech Stack
- **Language:** Python 3.10+  
- **LLM:** `google/flan-t5-base`  
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`  
- **Vector DB:** ChromaDB  
- **Frameworks:** FastAPI, Streamlit, LangChain  
- **Deployment:** Hugging Face Spaces  

## 📦 Installation & Setup

### 1. Clone the repository

`git clone https://github.com/HemaRamachandran28/Private-RAG-Chatbot-Full-Stack-Document-Assistant.git
cd rag-chatbot `

### Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

### Install dependencies
pip install -r requirements.txt

###Set up Environment Variables
Create a .env file in the root directory:
API_KEY=your_secret_password_here

### 🎮 How to Run
1. Start the FastAPI Backend
uvicorn app.main:app --reload
2. Start the Streamlit UI
streamlit run app/ui.py

Visit: http://localhost:8501
to start chatting with your documents!

### 🌐 Live Demo

You can find the live deployment of this project on Hugging Face Spaces here:
https://huggingface.co/spaces/Hema28/Rag-Chatbot

### 📜 License
MIT License
