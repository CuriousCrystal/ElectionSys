from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from app.config import settings

router = APIRouter(prefix="/api/chat", tags=["AI Assistant"])

# Initialize OpenAI client for Grok/xAI
client = OpenAI(api_key=settings.xai_api_key, base_url="https://api.x.ai/v1")

# Conversation history storage (can be moved to MongoDB later)
conversation_histories = {}


class ChatMessage(BaseModel):
    message: str
    session_id: str = "default"


@router.post("/")
async def chat_with_assistant(chat_input: ChatMessage):
    """Send message to AI assistant and get response"""
    if not settings.xai_api_key:
        raise HTTPException(
            status_code=503,
            detail="AI service not configured. Please set XAI_API_KEY in environment."
        )
    
    # Initialize history if needed
    if chat_input.session_id not in conversation_histories:
        conversation_histories[chat_input.session_id] = [
            {
                "role": "system",
                "content": "You are August, the friendly Election Process Guide. Help users understand election steps, registration, voting day procedures, timelines, and voter rights. Provide clear, easy-to-follow guidance with practical examples and next steps. Keep tone supportive and educational."
            }
        ]
    
    # Add user message
    conversation_histories[chat_input.session_id].append(
        {"role": "user", "content": chat_input.message}
    )
    
    try:
        response = client.chat.completions.create(
            model="grok-beta",
            messages=conversation_histories[chat_input.session_id],
            temperature=0.7,
            max_tokens=512
        )
        
        assistant_reply = response.choices[0].message.content
        conversation_histories[chat_input.session_id].append(
            {"role": "assistant", "content": assistant_reply}
        )
        
        return {"response": assistant_reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")
