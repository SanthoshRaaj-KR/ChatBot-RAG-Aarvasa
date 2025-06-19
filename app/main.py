from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.chatbot import get_chat_response

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str
    history: list[tuple[str, str]] = []

@app.post("/chat")
async def chat_endpoint(payload: Message):
    response = get_chat_response(payload.message, payload.history)
    return JSONResponse(content={"response": response})
