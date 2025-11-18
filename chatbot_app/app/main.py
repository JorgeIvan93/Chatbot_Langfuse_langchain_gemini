from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes import api_router
from app.services.standard_logger import logger

# Inicialized FastAPI app
app = FastAPI(
    title="LangGraph Gemini Chatbot API",
    description="API for chatbot powered by LangGraph and Gemini LLM.",
    version="1.0.0"
)

# Middleware for CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# state verification endpoint
@app.get("/")
def root():
    return {"message": "Chatbot API is running. Use chatbot endpoint."}

# centralized router
app.include_router(api_router)

# driver error global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error. Please try again later."}
    )