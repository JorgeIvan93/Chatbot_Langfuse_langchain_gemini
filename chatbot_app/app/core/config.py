from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application basic info
    app_name: str = "Chatbot Langfuse Langchain Gemini"

    # JWT configuration for authentication
    secret_key: str  # Secret key for signing JWT tokens
    algorithm: str = "HS256"  # Algorithm used for JWT
    access_token_expire_minutes: int = 30  # Token expiration time in minutes

    # Simple authentication credentials (from .env)
    auth_username: str  # Default username for login
    auth_password: str  # Default password for login

    # Gemini API configuration
    gemini_api_key: str  # API key for Gemini
    gemini_model: str  # Default Gemini model
    llm_temperature: float  # Model temperature for creativity

    # Logging configuration
    log_console_level: str  # Minimum log level for console
    silence_warnings: bool  # Silence Python warnings globally
    quiet_third_party: bool  # Reduce noisy third-party logs

    # Application version info
    app_version: str  # Version of the application

    # Langfuse observability configuration
    enable_langfuse: bool
    langfuse_public_key: str
    langfuse_secret_key: str
    langfuse_base_url: str
    langfuse_tracing_environment: str
    langfuse_debug: bool
    langfuse_sample_rate: float

    class Config:
        env_file = ".env"  # Load environment variables from .env file


# Initialize settings instance
settings = Settings()
