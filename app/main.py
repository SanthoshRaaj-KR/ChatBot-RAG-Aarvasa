# app/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from app.chatbot import build_prompt, ask_ollama

app = FastAPI()

class Query(BaseModel):
    message: str

@app.post("/ask-bot")
def ask_bot(query: Query):
    prompt = build_prompt(query.message)
    reply = ask_ollama(prompt)
    return {"reply": reply}
