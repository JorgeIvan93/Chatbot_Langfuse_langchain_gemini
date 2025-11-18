from fastapi import APIRouter
from app.api.v1.chatbot import router as chatbot_router

# Router principal que agrupa todos los endpoints
api_router = APIRouter()

# Incluye el router del chatbot con su prefijo y etiqueta
api_router.include_router(chatbot_router, prefix="/api/v1/chatbot", tags=["Chatbot"])