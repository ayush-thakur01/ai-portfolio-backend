# AI Portfolio Backend

Backend service for an AI-powered portfolio assistant built using FastAPI.

This backend integrates with OpenRouter to provide AI responses specifically tailored to portfolio-related queries. It also supports persistent chat history using SQLite and SQLAlchemy.

---

## 🚀 Overview

The backend is designed to:

- Expose REST APIs using FastAPI
- Integrate AI responses via OpenRouter
- Store chat history in SQLite
- Handle secure environment variables
- Support production deployment on Render

This service powers the AI assistant on the frontend portfolio.

---

## 🛠 Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- OpenRouter API
- Uvicorn
- Render (Deployment)

---

## 📂 Project Structure
    ai-portfolio-backend/
│
├── main.py # FastAPI application
├── models.py # Database models
├── database.py # Database configuration
├── requirements.txt # Project dependencies
└── README.md

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:
OPENROUTER_API_KEY=your_api_key_here

⚠ Important:
- Do NOT commit `.env` to GitHub
- Ensure `.gitignore` contains `.env`

In production (Render), set the environment variable from the dashboard.

---

## 📦 Local Setup & Installation

### 1️⃣ Clone Repository
git clone https://github.com/YOUR_USERNAME/ai-portfolio-backend.git

cd ai-portfolio-backend

### 2️⃣ Create Virtual Environment

Windows:python -m venv venv
venv\Scripts\activate
