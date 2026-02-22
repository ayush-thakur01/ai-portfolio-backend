from fastapi import FastAPI
from pydantic import BaseModel
import requests

from database import engine, SessionLocal
from models import ChatMessage, Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Request body model
class ChatRequest(BaseModel):
    message: str


OPENROUTER_API_KEY = "xxxxx"

@app.post("/chat")
async def chat(request: ChatRequest):

    db = SessionLocal()

    # Save user message
    db.add(ChatMessage(role="user", content=request.message))
    db.commit()

    # Call OpenRouter
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-3.5-turbo",
           "messages": [
    {
        "role": "system",
        "content": """
You are an AI assistant for Ayush Thakur's portfolio website.

Only answer questions related to Ayush's skills, projects, education, and technical experience.

If a question is unrelated to Ayush, politely respond:
"I am designed to answer questions only about Ayush's portfolio and professional work."

Here is Ayush's information:

Name: Ayush Thakur
Education: B.Tech in Computer Science

Skills:
- React
- TypeScript
- Python
- FastAPI
- SQLite
- MySQL
- Node.js
- REST API Design
- SQLAlchemy
- Git & GitHub

Projects:

1) AI-Integrated Portfolio System:
Full-stack portfolio website with AI chat assistant.
Backend built using FastAPI, persistent chat storage with SQLite,
OpenRouter integration for AI responses.

2) GitHub Profile Analyzer:
Tool that analyzes public GitHub profiles using GitHub API.
Evaluates repositories, languages, commit activity, and contributions.

3) Krishi Sahyog:
Web-based agricultural support platform designed to assist farmers
with crop guidance and digital resource management.

4) Smart Composting Bin:
IoT-based compost system integrating temperature and moisture sensors,
rotating cutting mechanism, water spray system, and heating elements.
Designed to accelerate biodegradable waste decomposition.

Always respond professionally and clearly.
"""
    },
    {
        "role": "user",
        "content": request.message
    }
],
        }
    )

    ai_response = response.json()["choices"][0]["message"]["content"]

    # Save AI message
    db.add(ChatMessage(role="ai", content=ai_response))
    db.commit()

    db.close()

    return {"response": ai_response}

@app.delete("/clear")
def clear_history():
    db = SessionLocal()
    db.query(ChatMessage).delete()
    db.commit()
    db.close()
    return {"message": "Chat history cleared"}

# NEW HISTORY ENDPOINT
@app.get("/history")
def get_history():
    db = SessionLocal()
    messages = db.query(ChatMessage).all()
    db.close()

    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]
