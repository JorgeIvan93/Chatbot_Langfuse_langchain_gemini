"""
services/gemini.py

🤖 Este archivo es nuestro intérprete con el modelo Gemini de Google.
Es como un traductor que sabe cómo hablar con Gemini y asegurarse
de que siempre obtengamos una respuesta comprensible.
"""

import os
from types import SimpleNamespace
from config import GEMINI_API_KEY

# Intentamos importar el chat de Gemini
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    modelo_base = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
        google_api_key=GEMINI_API_KEY,
    )
except Exception:
    ChatGoogleGenerativeAI = None
    modelo_base = None


class AsistenteGemini:
    """
    Esta es nuestra herramienta para hablar con Gemini.
    
    Es como un teléfono especial que:
    1. Sabe cómo llamar a Gemini
    2. Entiende diferentes formas de respuesta
    3. Siempre nos da una respuesta entendible
    """
    def __init__(self, modelo=modelo_base, mensaje_respaldo: str = None):
        self.modelo = modelo
        self.mensaje_respaldo = mensaje_respaldo or "Lo siento, no puedo conectar con Gemini en este momento."

    def preguntar(self, pregunta: str):
        """
        Esta función es como hacer una llamada a Gemini.
        Le hacemos una pregunta y nos aseguramos de obtener una respuesta.
        """
        # Si no podemos conectar con Gemini, usamos el mensaje de respaldo
        if not self.modelo:
            return SimpleNamespace(content=self.mensaje_respaldo)

        try:
            # Primera forma: pregunta directa
            if hasattr(self.modelo, "invoke"):
                respuesta = self.modelo.invoke(pregunta)
                # Asegurarnos de que la respuesta sea entendible
                if isinstance(respuesta, str):
                    return SimpleNamespace(content=respuesta)
                if hasattr(respuesta, "content"):
                    return SimpleNamespace(content=respuesta.content)
                generaciones = getattr(respuesta, "generations", None)
                if generaciones:
                    try:
                        texto = generaciones[0][0].text if isinstance(generaciones[0], list) and hasattr(generaciones[0][0], "text") else str(generaciones)
                        return SimpleNamespace(content=texto)
                    except Exception:
                        return SimpleNamespace(content=str(respuesta))
                return SimpleNamespace(content=str(respuesta))

            # Segunda forma: generación estructurada
            if hasattr(self.modelo, "generate"):
                resultado = self.modelo.generate([{"role": "user", "content": pregunta}])
                generaciones = getattr(resultado, "generations", None)
                if generaciones:
                    try:
                        texto = generaciones[0][0].text if isinstance(generaciones[0], list) and hasattr(generaciones[0][0], "text") else str(generaciones)
                        return SimpleNamespace(content=texto)
                    except Exception:
                        return SimpleNamespace(content=str(resultado))
                return SimpleNamespace(content=str(resultado))

            # Tercera forma: llamada simple
            if callable(self.modelo):
                respuesta = self.modelo(pregunta)
                if isinstance(respuesta, str):
                    return SimpleNamespace(content=respuesta)
                if hasattr(respuesta, "content"):
                    return SimpleNamespace(content=respuesta.content)
                return SimpleNamespace(content=str(respuesta))

            return SimpleNamespace(content=str(self.llm))

        except Exception as e:
            # Ajustar mensaje si es error de modelo no encontrado
            msg = str(e)
            if "not found" in msg.lower() or "models/" in msg.lower() or "NotFound" in msg:
                raise RuntimeError(
                    f"LLM model error: {msg}. Verifica que la variable de entorno GEMINI_MODEL y la clave GEMINI_API_KEY sean correctas y que el modelo exista. Ejecuta ListModels para ver los modelos disponibles."
                ) from e
            raise

    def __call__(self, prompt: str):
        return self.invoke(prompt)


# Inicializar LLM real si está disponible y se proporcionó clave
GEMINI_MODEL = os.getenv("GEMINI_MODEL")
_real_llm = None
if ChatGoogleGenerativeAI is not None and GEMINI_API_KEY:
    try:
        if GEMINI_MODEL:
            _real_llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, google_api_key=GEMINI_API_KEY)
        else:
            # Si no se especifica modelo, crear instancia sin modelo (la librería puede elegir defecto)
            _real_llm = ChatGoogleGenerativeAI(google_api_key=GEMINI_API_KEY)
    except Exception:
        _real_llm = None

# Verificar silenciosamente la disponibilidad del modelo
_model_available = bool(_real_llm)

# Crear instancia global del asistente
asistente_gemini = AsistenteGemini(_real_llm, mensaje_respaldo="Respuesta simulada por fallback: LLM no configurado o modelo no disponible.")
