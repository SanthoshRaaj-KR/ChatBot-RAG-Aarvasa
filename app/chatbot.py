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
    "You are Aarvasa's friendly AI assistant helping users with anything related to real estate. "
    "Start by answering naturally in a helpful and friendly tone. "
    "Always try to find answers from the company context file first. "
    "If not found and if the question is about where to find something on the site, check the navigation.json file. "
    "If neither helps, still try to give your best answer in a clear, short, and persuasive way. "
    "If users ask to 'show properties under a price' (e.g., under 30 lakhs), inform them to visit the Listings or Search page. "
    "Avoid going off-topic and keep your response brief (within 3 lines unless really needed). "
    "If you dont know dont cook up be honest and tell dont know."
)



# Initialize both RAG engines
company_rag = CompanyRAG("app/company_context.txt")
nav_rag = NavigationRAG("app/navigation.json")

def get_chat_response(user_message: str, chat_history=None) -> str:
    try:
        user_msg_lower = user_message.lower()

        # Short-circuit common small talk or general queries
        general_keywords = ["hello", "hi", "hey", "how are you", "what's up", "thank you", "thanks"]
        if any(word in user_msg_lower for word in general_keywords):
            return "Hey! I'm Aarvasa's assistant. Let me know how I can help with your property queries. 😊"

        # If it's about 'where', 'find', 'navigate', etc., then use navigation.json
        if any(kw in user_msg_lower for kw in ["where", "find", "go to", "navigate", "open", "page", "how to"]):
            nav_results = nav_rag.retrieve_navigation_info(user_message, top_k=1)
            nav_match = nav_results[0] if nav_results else None
            if nav_match:
                return f"{nav_match['description']} You can find it on the '{nav_match['name']}' page."

        # Otherwise, try to use company RAG
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
