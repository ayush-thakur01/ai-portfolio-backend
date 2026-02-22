import requests
import os
from dotenv import load_dotenv

load_dotenv()

def ask_ai(question: str, resume_text: str):
    url = "https://openrouter.ai/api/v1/chat/completions"

    prompt = f"""
    You are an AI assistant answering questions about this candidate.
    Only answer using the resume below.
    If information is not available, say 'Not mentioned in resume'.

    Resume:
    {resume_text}

    Question:
    {question}
    """

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    return response.json()
print(os.getenv("OPENROUTER_API_KEY"))