"""Centralized application configuration loaded via Pydantic Settings from `.env`/environment."""

from typing import Literal  # Constrained string literal for console-level values
from pydantic import Field, AliasChoices  # Field metadata + flexible env key aliases
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)  # Settings loader backed by .env/env

ConsoleLevel = Literal[
    "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
]  # Allowed console levels


class Settings(BaseSettings):
    """Holds all application settings; values come from `.env` or environment variables."""

    #  LLM (Google Gemini)
    gemini_api_key: str = Field(
        "", alias="GOOGLE_API_KEY"
    )  # API key for Gemini Developer API
    gemini_model: str = Field(
        "gemini-2.5-pro", alias="GEMINI_MODEL"
    )  # Default chat model
    LLM_TEMPERATURE: float = Field(
        0.7, alias="LLM_TEMPERATURE"
    )  # Default decoding temperature

    #  Langfuse (Observability)
    LANGFUSE_PUBLIC_KEY: str = Field(
        "", alias="LANGFUSE_PUBLIC_KEY"
    )  # Public key for Langfuse
    LANGFUSE_SECRET_KEY: str = Field(
        "", alias="LANGFUSE_SECRET_KEY"
    )  # Secret key for Langfuse
    LANGFUSE_BASE_URL: str = Field(
        "", alias="LANGFUSE_BASE_URL"
    )  # Preferred base URL (region-aware)
    LANGFUSE_HOST: str = Field(
        "https://cloud.langfuse.com", alias="LANGFUSE_HOST"
    )  # Fallback host

    # Enable/disable Langfuse tracing (accept both ENABLE_LANGFUSE and enable_langfuse)
    ENABLE_LANGFUSE: bool = Field(
        False,
        validation_alias=AliasChoices("ENABLE_LANGFUSE", "enable_langfuse"),
    )

    #  Logging / Warnings
    LOG_CONSOLE_LEVEL: ConsoleLevel = Field(
        "WARNING",
        validation_alias=AliasChoices("LOG_CONSOLE_LEVEL", "log_console_level"),
    )  # Console handler level

    SILENCE_WARNINGS: bool = Field(
        True,
        validation_alias=AliasChoices("SILENCE_WARNINGS", "silence_warnings"),
    )  # Toggle Python warnings

    QUIET_THIRD_PARTY: bool = Field(
        True,
        validation_alias=AliasChoices("QUIET_THIRD_PARTY", "quiet_third_party"),
    )  # Reduce noise from vendor loggers

    #  App
    APP_NAME: str = Field(
        "Advanced LangGraph Chatbot", alias="APP_NAME"
    )  # Banner title
    APP_VERSION: str = Field("1.0.1", alias="APP_VERSION")  # Version string

    # Pydantic Settings config: load from `.env`, ignore unknown keys (won't fail on extras)
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Shared, ready-to-use settings instance for the whole application
settings = Settings()
