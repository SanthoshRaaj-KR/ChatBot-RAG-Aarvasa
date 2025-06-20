import openai
import os
from dotenv import load_dotenv
from app.rag_engine import CompanyRAG, NavigationRAG

load_dotenv()

openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"

MODEL = "llama3-8b-8192"
MAX_CONTEXT_MESSAGES = 15

system_instructions = (
    "You are Aarvasa's AI assistant, specializing in real estate. "
    "You must only answer real estate-related queries. Avoid unrelated topics. "
    "Keep answers short, friendly, and persuasive. "
    "Encourage users to explore or buy Aarvasa's properties when appropriate. "
    "Try to keep your response as small as possible, within 3 lines unless absolutely necessary"
)


# Initialize both RAG engines
company_rag = CompanyRAG("app/company_context.txt")
nav_rag = NavigationRAG("app/navigation.json")

def get_chat_response(user_message: str, chat_history=None) -> str:
    try:
        # First try navigation match
        nav_results = nav_rag.retrieve_navigation_info(user_message, top_k=1)
        nav_match = nav_results[0] if nav_results else None

        if nav_match:
            return f"{nav_match['description']} You can find it on the '{nav_match['name']}' page."

        # If no nav match, fall back to company RAG
        relevant_context = company_rag.retrieve_relevant_chunks(user_message)

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
