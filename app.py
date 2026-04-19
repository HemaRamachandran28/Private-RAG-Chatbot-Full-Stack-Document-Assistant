import streamlit as st
import os
import uuid
import torch
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# --- PAGE CONFIG ---
st.set_page_config(page_title="Safe RAG Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 RAGenius")
st.markdown("I only answer based on your documents. If I don't know, I'll say so.")

# --- CONFIGURATION ---
DB_DIR = "chroma_db_final"

@st.cache_resource
def load_resources():
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = Chroma(persist_directory=DB_DIR, embedding_function=embedding)

    model_id = "google/flan-t5-base"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

    return db, model, tokenizer

db, model, tokenizer = load_resources()

# --- UI LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("📄 Upload Knowledge")
    uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

    if uploaded_file and st.button("Ingest Document"):
        with st.spinner("Analyzing..."):
            temp_path = f"deploy_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            try:
                loader = PyPDFLoader(temp_path) if temp_path.endswith(".pdf") else TextLoader(temp_path)
                docs = loader.load()
                splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
                chunks = splitter.split_documents(docs)
                db.add_documents(chunks)
                st.success("Document added!")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Display Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if query := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Searching..."):
            # 1. Retrieval (Look at 4 chunks)
            retriever = db.as_retriever(search_kwargs={"k": 4})
            docs = retriever.invoke(query)

            if not docs:
                answer = "I don't know based on the documents."
            else:
                # 2. Build Context
                context = "\n---\n".join([f"[Page {d.metadata.get('page', 0)+1}]: {d.page_content}" for d in docs])

                # 3. Strict Prompting
                prompt = (
                    "Answer the following question using only the provided context. "
                    "If the answer is not in the context, say 'I don't know based on the documents'. "
                    "Do not use outside knowledge.\n\n"
                    f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
                )

                input_ids = tokenizer(prompt, return_tensors="pt").input_ids
                # temperature=0.1 stops the model from "guessing" or being creative
                outputs = model.generate(input_ids, max_new_tokens=512, temperature=0.1, do_sample=True)
                answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})