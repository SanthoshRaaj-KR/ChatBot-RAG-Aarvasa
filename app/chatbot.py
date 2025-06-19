import openai
import os
from dotenv import load_dotenv
from app.rag_engine import RAGEngine

load_dotenv()

openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"

# Initialize RAG engine
rag = RAGEngine("app/company_context.txt")

def get_chat_response(user_message: str) -> str:
    try:
        relevant_context = rag.retrieve_relevant_chunks(user_message)

        system_instructions = (
            "You are Aarvasa's AI assistant, specializing in real estate. "
            "You must only answer real estate-related queries. "
            "Avoid unrelated topics. "
            "Keep answers short, friendly, and persuasive. "
            "Encourage users to explore or buy Aarvasa's properties when appropriate. "
            "Try to keep your response as small as possible"
        )

        messages = [
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_message}
        ]

        response = openai.ChatCompletion.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=0.5,
        )
        return response.choices[0].message["content"].strip()

    except Exception as e:
        return f"Error from AI: {str(e)}"
