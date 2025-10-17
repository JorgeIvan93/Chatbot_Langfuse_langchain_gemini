from langfuse import Langfuse
from config import LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST


class LangfuseLogger:
    def __init__(self):
        try:
            self.client = Langfuse(
                public_key=LANGFUSE_PUBLIC_KEY,
                secret_key=LANGFUSE_SECRET_KEY,
                host=LANGFUSE_HOST,
            )
        except Exception:
            self.client = None
    
    def log(self, event_name: str, data: dict):
        """
        Registra un evento en Langfuse si está disponible
        """
        if self.client:
            try:
                # Crear una nueva observación
                observation = self.client.trace(
                    name=event_name
                ).generation(
                    name=event_name,
                    input=data.get("entrada", ""),
                    output=data.get("salida", "")
                )
                observation.end()  # Finalizar la observación
            except Exception:
                # Silenciosamente ignorar errores de logging
                pass


logger = LangfuseLogger()