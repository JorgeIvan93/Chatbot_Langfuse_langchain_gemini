from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App basic info
    app_name: str = "Chatbot Langfuse Langchain Gemini"

    # JWT config
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Gemini config
    gemini_api_key: str
    gemini_model: str
    llm_temperature: float

    # Logging config
    log_console_level: str
    silence_warnings: bool
    quiet_third_party: bool

    # App version
    app_version: str

    # Langfuse config
    enable_langfuse: bool
    langfuse_public_key: str
    langfuse_secret_key: str
    langfuse_base_url: str
    langfuse_tracing_environment: str
    langfuse_debug: bool
    langfuse_sample_rate: float

    # SQLite database config
    database_url: str = "sqlite:///./chatbot.db"
    sqlite_check_same_thread: bool = False  # allow cross-thread usage in FastAPI

    class Config:
        env_file = ".env"


settings = Settings()
