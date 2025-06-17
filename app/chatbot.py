import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"

# Load system prompt from file
with open("app/company_context.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

def get_chat_response(user_message: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.5,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Error from AI: {str(e)}"
