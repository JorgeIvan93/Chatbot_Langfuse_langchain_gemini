# intérprete con el modelo Gemini, verifica que siempre obtengamos una respuesta comprensible.

from types import SimpleNamespace  # estructura simple para respuestas
from config import config  # Importación de configuración centralizada
  # clave de API para Gemini

# Intentamos importar el chat de Gemini
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    modelo_base = ChatGoogleGenerativeAI(
        model=config.modelo_gemini,  # modelo definido en .env
        temperature=0.7,  # nivel de creatividad en respuestas
        google_api_key=config.clave_api_gemini  # clave API desde configuración,
    )
except Exception as e:
    print("Error al inicializar modelo_base:", e)
    ChatGoogleGenerativeAI = None
    modelo_base = None


class AsistenteGemini:  # herramienta para hablar con gemini, generando respuestas comprensibles
    def __init__(self, modelo=modelo_base, mensaje_respaldo: str = None):
        self.modelo = modelo
        self.mensaje_respaldo = mensaje_respaldo or "Lo siento, no puedo conectar con Gemini en este momento."

    def preguntar(self, pregunta: str):  # hacemos una pregunta y obtenemos una respuesta.
        if not self.modelo:
            return SimpleNamespace(content=self.mensaje_respaldo)

        try:
            if hasattr(self.modelo, "invoke"):
                respuesta = self.modelo.invoke(pregunta)
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

            if callable(self.modelo):
                respuesta = self.modelo(pregunta)
                if isinstance(respuesta, str):
                    return SimpleNamespace(content=respuesta)
                if hasattr(respuesta, "content"):
                    return SimpleNamespace(content=respuesta.content)
                return SimpleNamespace(content=str(respuesta))

            return SimpleNamespace(content=str(self.llm))

        except Exception as e:
            msg = str(e)
            if "not found" in msg.lower() or "models/" in msg.lower() or "NotFound" in msg:
                raise RuntimeError(
                    f"LLM model error: {msg}. Verifica que la variable de entorno GEMINI_MODEL y la clave GEMINI_API_KEY sean correctas y que el modelo exista. Ejecuta ListModels para ver los modelos disponibles."
                ) from e
            raise

    def __call__(self, prompt: str):
        return self.preguntar(prompt)


# Inicializar LLM real si está disponible y se proporcionó clave
_real_llm = None
if ChatGoogleGenerativeAI is not None and config.clave_api_gemini:
    try:
        if config.modelo_gemini:
            _real_llm = ChatGoogleGenerativeAI(model=config.modelo_gemini, google_api_key=config.clave_api_gemini)
        else:
            _real_llm = ChatGoogleGenerativeAI(google_api_key=config.clave_api_gemini)
    except Exception as e:
        print("Error al inicializar _real_llm:", e)
        _real_llm = None

_model_available = bool(_real_llm)

# Crear instancia global del asistente
asistente_gemini = AsistenteGemini(_real_llm, mensaje_respaldo="Respuesta simulada por fallback: LLM no configurado o modelo no disponible.")