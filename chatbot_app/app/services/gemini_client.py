"""
Gemini client wrapper without Langfuse duplication.
"""

from __future__ import annotations
from langchain_google_genai import ChatGoogleGenerativeAI
from app.services.standard_logger import logger
from app.core.config import settings

class GeminiClient:
    def __init__(self) -> None:
        model = settings.gemini_model
        temperature = settings.llm_temperature
        api_key = settings.gemini_api_key

        if not api_key:
            msg = "GOOGLE_API_KEY is missing. Define it in .env."
            logger.error(msg)
            raise ValueError(msg)

        logger.info(f"Initializing Gemini client with model: {model}, temperature={temperature}")
        self.llm = ChatGoogleGenerativeAI(model=model, temperature=temperature, api_key=api_key)

    def invoke_model(self, prompt: str) -> str:
        try:
            response = self.llm.invoke(prompt)
            return getattr(response, "content", str(response))
        except Exception as e:
            logger.exception(f"Error during Gemini invocation: {e}")
            return "Sorry, I encountered an error while processing your request."

gemini_client = GeminiClient()