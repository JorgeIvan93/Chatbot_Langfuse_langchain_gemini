"""
Provides a thin wrapper around the Google Gemini chat model via LangChain.
Centralizes model configuration and exposes a single, reusable client instance.
"""

from __future__ import annotations

# LangChain's integration for Google Gemini chat models
from langchain_google_genai import ChatGoogleGenerativeAI

# Application logger (console + rotating file via services/standard_logger.py)
from services.standard_logger import logger

# Centralized settings loaded from .env through pydantic-settings (config/config.py)
from config import settings


class GeminiClient:
    def __init__(self) -> None:
        # Read model configuration from centralized settings
        model = settings.gemini_model
        temperature = settings.LLM_TEMPERATURE
        api_key = settings.gemini_api_key

        # Validate presence of the API key early (never log the secret itself)
        if not api_key:
            msg = (
                "GOOGLE_API_KEY no está configurada en settings. "
                "Define la variable en tu .env o entorno (GOOGLE_API_KEY)."
            )
            logger.error(msg)
            raise ValueError(msg)

        # Inform about model initialization (safe: does not print secrets)
        logger.info(
            f"Initializing Gemini client with model: {model}, temperature={temperature}"
        )

        # Instantiate the LangChain chat model with explicit API key
        # (avoids falling back to ADC/environment auto-discovery)
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            api_key=api_key,  # No dependemos de env ni ADC
        )

    def get_llm_instance(self) -> ChatGoogleGenerativeAI:
        """Return the underlying LangChain chat model for reuse across the app."""
        return self.llm

    def invoke_model(self, prompt: str) -> str:
        """
        Invoke the chat model with a simple text prompt and return text content.
        Errors are logged and a user-friendly message is returned.
        """
        try:
            # Keep logs safe and concise: do not print full prompts in production
            response = self.llm.invoke(prompt)
            # LangChain responses typically expose `.content`; fallback to str if missing
            return getattr(response, "content", str(response))
        except Exception as e:
            # Log full exception details for troubleshooting
            logger.exception(f"Error durante la invocación de Gemini: {e}")
            return "Sorry, I encountered an error while processing your request."


# Eagerly create a singleton instance so other modules can import and reuse it
gemini_client = GeminiClient()
