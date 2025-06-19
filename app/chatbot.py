import openai
import os
from dotenv import load_dotenv
from app.rag_engine import RAGEngine

load_dotenv()

openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"

rag = RAGEngine("app/company_context.txt")

MODEL = "llama3-8b-8192"
MAX_CONTEXT_MESSAGES = 20

system_instructions = (
    "You are Aarvasa's AI assistant, specializing in real estate. "
    "You must only answer real estate-related queries. "
    "Avoid unrelated topics. "
    "Keep answers short, friendly, and persuasive. "
    "Encourage users to explore or buy Aarvasa's properties when appropriate. "
    "Try to keep your response as small as possible. within 3 lines"
)

def get_chat_response(user_message: str, chat_history=None) -> str:
    try:
        relevant_context = rag.retrieve_relevant_chunks(user_message)

        messages = [{"role": "system", "content": f"{system_instructions}\n\n{relevant_context}"}]

        if chat_history and isinstance(chat_history, list):
            trimmed = chat_history[-MAX_CONTEXT_MESSAGES:]
            for user_msg, bot_msg in trimmed:
                messages.append({"role": "user", "content": user_msg})
                messages.append({"role": "assistant", "content": bot_msg})

        messages.append({"role": "user", "content": user_message})

        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
            temperature=0.5,
        )

        return response.choices[0].message["content"].strip()

    except Exception as e:
        return f"Error from AI: {str(e)}"
