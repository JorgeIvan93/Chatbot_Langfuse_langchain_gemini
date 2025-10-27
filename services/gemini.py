from types import SimpleNamespace
from config import config

# Inicializar el modelo Gemini
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    modelo_base = ChatGoogleGenerativeAI(
        model=config.modelo_gemini,
        temperature=0.7,
        google_api_key=config.clave_api_gemini
    )
except Exception as e:
    ChatGoogleGenerativeAI = None
    modelo_base = None

class AsistenteGemini:
    def __init__(self, modelo=modelo_base, mensaje_respaldo: str = None):
        self.modelo = modelo
        self.mensaje_respaldo = mensaje_respaldo or "Lo siento, no puedo conectar con Gemini en este momento."

    def preguntar(self, pregunta: str):
        if not self.modelo:
            return SimpleNamespace(content=self.mensaje_respaldo)

        try:
            respuesta = self.modelo.invoke(pregunta)

            contenido = getattr(respuesta, "content", None)
            if contenido:
                return SimpleNamespace(content=contenido)

            if isinstance(respuesta, str):
                return SimpleNamespace(content=respuesta)

            if hasattr(respuesta, "text") and respuesta.text:
                return SimpleNamespace(content=respuesta.text)

            generaciones = getattr(respuesta, "generations", None)
            if generaciones:
                try:
                    texto = generaciones[0][0].text if isinstance(generaciones[0], list) and hasattr(generaciones[0][0], "text") else str(generaciones)
                    return SimpleNamespace(content=texto)
                except Exception:
                    return SimpleNamespace(content=str(generaciones))

            return SimpleNamespace(content=str(respuesta))

        except Exception:
            return SimpleNamespace(content=self.mensaje_respaldo)

    def __call__(self, prompt: str):
        return self.preguntar(prompt)

# Inicializar LLM real si está disponible
_real_llm = None
if ChatGoogleGenerativeAI is not None and config.clave_api_gemini:
    try:
        if config.modelo_gemini:
            _real_llm = ChatGoogleGenerativeAI(model=config.modelo_gemini, google_api_key=config.clave_api_gemini)
        else:
            _real_llm = ChatGoogleGenerativeAI(google_api_key=config.clave_api_gemini)
    except Exception:
        _real_llm = None

_model_available = bool(_real_llm)

# Instancia global del asistente
asistente_gemini = AsistenteGemini(_real_llm, mensaje_respaldo="Respuesta simulada por fallback: LLM no configurado o modelo no disponible.")