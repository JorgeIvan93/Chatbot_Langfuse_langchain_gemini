from fastapi import APIRouter
from app.api.v1.chatbot import router as chatbot_router
from app.api.v1.auth import router as auth_router

# Main router that groups all endpoints
api_router = APIRouter()

# Include authentication router
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# Include chatbot router with its prefix and tag
api_router.include_router(chatbot_router, prefix="/api/v1/chatbot", tags=["Chatbot"])
