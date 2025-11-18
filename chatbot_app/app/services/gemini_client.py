"""
Provides a thin wrapper around the Google Gemini chat model via LangChain.
Centralizes model configuration and exposes a single, reusable client instance.
"""

from __future__ import annotations
from langchain_google_genai import ChatGoogleGenerativeAI  # LangChain integration for Google Gemini
from app.services.standard_logger import logger  # Application logger
from app.core.config import settings  # Centralized settings loaded from .env using Pydantic


class GeminiClient:
    def __init__(self) -> None:
        # Read model configuration from settings
        model = settings.gemini_model
        temperature = settings.LLM_TEMPERATURE
        api_key = settings.gemini_api_key

        # Validate API key presence (do not log the secret)
        if not api_key:
            msg = (
                "GOOGLE_API_KEY is not configured in settings. "
                "Define the variable in your .env or environment (GOOGLE_API_KEY)."
            )
            logger.error(msg)
            raise ValueError(msg)

        # Log safe initialization details
        logger.info(f"Initializing Gemini client with model: {model}, temperature={temperature}")

        # Create LangChain Gemini chat model with explicit API key
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            api_key=api_key,
        )

    def get_llm_instance(self) -> ChatGoogleGenerativeAI:
        """Return the Gemini chat model instance for reuse across the app."""
        return self.llm

    def invoke_model(self, prompt: str) -> str:
        """
        Invoke the Gemini model with a simple text prompt and return the response text.
        Logs errors and returns a safe fallback message if something fails.
        """
        try:
            response = self.llm.invoke(prompt)
            return getattr(response, "content", str(response))
        except Exception as e:
            logger.exception(f"Error during Gemini invocation: {e}")
            return "Sorry, I encountered an error while processing your request."


# Create a singleton instance for reuse
gemini_client = GeminiClient()