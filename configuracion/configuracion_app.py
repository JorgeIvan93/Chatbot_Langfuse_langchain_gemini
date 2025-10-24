from pydantic_settings import BaseSettings
from pydantic import Field

class ConfiguracionApp(BaseSettings):
    clave_api_gemini: str = Field(..., alias="GEMINI_API_KEY")
    clave_langfuse: str = Field(..., alias="LANGFUSE_PUBLIC_KEY")
    clave_privada_langfuse: str = Field(..., alias="LANGFUSE_SECRET_KEY")
    url_langfuse: str = Field(..., alias="LANGFUSE_HOST")
    modelo_gemini: str = Field(..., alias="GEMINI_MODEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        populate_by_name = True