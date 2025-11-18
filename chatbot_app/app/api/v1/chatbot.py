from fastapi import APIRouter
from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import process_chat

# Create router for chatbot endpoints
router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Receives a user message and returns a chatbot response.
    """
    response = await process_chat(request)
    return response