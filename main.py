
# main.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from dotenv import load_dotenv

# -----------------------
# Load environment variables
# -----------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# -----------------------
# FastAPI setup
# -----------------------
app = FastAPI(title="Koko Cloud AI (Groq)", description="Type and Koko responds!", version="1.0")

# -----------------------
# Pydantic model for user messages
# -----------------------
class UserMessage(BaseModel):
    message: str
    user_id: str = "guest"  # optional for future memory expansion

# -----------------------
# API Endpoint: /chat
# User sends POST with {"message": "Hello Koko"}
# -----------------------
@app.post("/chat")
async def chat(message_data: UserMessage):
    user_input = message_data.message.strip()

    if not user_input:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    # -----------------------
    # Call Groq API
    # -----------------------
    try:
        groq_endpoint = "https://api.groq.com/v1/ai/chat"  # example endpoint
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "input": user_input,
            "model": "groq-chat-1"  # adjust if needed
        }
        response = requests.post(groq_endpoint, json=payload, headers=headers)
        response.raise_for_status()
        koko_reply = response.json().get("output", "Hmm, I'm confused.")  # default fallback
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq API error: {e}")

    return {"reply": koko_reply}

# -----------------------
# Run locally with:
# uvicorn main:app --reload --host 0.0.0.0 --port 8000
# -----------------------
