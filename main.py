from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

from database import engine, SessionLocal
from models import ChatMessage, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route (fix 404 on /)
@app.get("/")
def root():
    return {"message": "Ayush Portfolio AI Backend Running Successfully 🚀"}

# Request model
class ChatRequest(BaseModel):
    message: str

# Load API key securely
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not set in environment variables")

@app.post("/chat")
def chat(request: ChatRequest):
    db = SessionLocal()

    try:
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
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an AI assistant for Ayush Thakur's portfolio website. Only answer portfolio-related questions."
                    },
                    {
                        "role": "user",
                        "content": request.message
                    }
                ]
            },
            timeout=30
        )

        data = response.json()

        # Check API error
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=data)

        if "choices" not in data:
            raise HTTPException(status_code=500, detail="Invalid API response format")

        ai_response = data["choices"][0]["message"]["content"]

        # Save AI message
        db.add(ChatMessage(role="ai", content=ai_response))
        db.commit()

        return {"response": ai_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()

@app.get("/history")
def get_history():
    db = SessionLocal()
    try:
        messages = db.query(ChatMessage).all()
        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
    finally:
        db.close()

@app.delete("/clear")
def clear_history():
    db = SessionLocal()
    try:
        db.query(ChatMessage).delete()
        db.commit()
        return {"message": "Chat history cleared"}
    finally:
        db.close()