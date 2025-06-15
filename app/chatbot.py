# app/chatbot.py

from app.rag_engine import RAGEngine
import requests

rag = RAGEngine()
rag.load_knowledge()
rag.build_index()

def build_prompt(user_query: str):
    relevant_context = rag.retrieve_context(user_query)

    return f"""
You are a helpful real estate assistant working for Aarvasa.

Use the context below to answer the user's question:
------------------
{relevant_context}
------------------

User: {user_query}
Answer in a friendly and helpful tone.
"""

def ask_ollama(prompt: str):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }

    res = requests.post(url, json=payload)
    if res.ok:
        return res.json().get("response", "").strip()
    return "Sorry, I couldn't generate a response right now."
