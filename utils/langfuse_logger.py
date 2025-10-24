from langfuse import Langfuse
from config import config  # Importación de configuración centralizada

# Clase para manejar el logging en Langfuse
class LangfuseLogger:
    def __init__(self):
        try:
            self.client = Langfuse(
                public_key=config.clave_langfuse,
                secret_key=config.clave_privada_langfuse,
                host=config.url_langfuse,
            )
        except Exception:
            self.client = None

    def log(self, nombre_evento: str, datos: dict):  # Registra un evento en Langfuse si está disponible
        if self.client:
            try:
                # Crear una nueva observación
                observacion = self.client.trace(
                    name=nombre_evento
                ).generation(
                    name=nombre_evento,
                    input=datos.get("entrada", ""),
                    output=datos.get("salida", "")
                )
                observacion.end()  # Finalizar la observación
            except Exception:
                # Silenciosamente ignorar errores de logging
                pass

# Instancia global del logger
logger = LangfuseLogger()