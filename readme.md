# AI Portfolio Backend

This is the backend service for the AI-integrated portfolio system.

## Overview

The backend is built using FastAPI and integrates with OpenRouter to provide AI responses tailored specifically to portfolio-related queries.

It also supports persistent chat storage using SQLite.

## Tech Stack

- FastAPI
- Python
- SQLite
- SQLAlchemy
- OpenRouter API
- Render (Deployment)

## API Endpoints

### POST /chat
Accepts user message and returns AI response.

### GET /history
Returns stored chat history.

### DELETE /clear
Clears chat history.

## Environment Variables

The following environment variable is required:
