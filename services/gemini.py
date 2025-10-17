import os
from types import SimpleNamespace
from config import GEMINI_API_KEY

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except Exception:
    ChatGoogleGenerativeAI = None


class GeminiLLMWrapper:
    """Wrapper que normaliza invocaciones al LLM y devuelve un objeto con .content."""
    def __init__(self, llm=None, fallback_text: str = None):
        self.llm = llm
        self.fallback_text = fallback_text or "Respuesta simulada: LLM no disponible."

    def invoke(self, prompt: str):
        # Si no hay LLM real, devolver fallback
        if not self.llm:
            return SimpleNamespace(content=self.fallback_text)

        try:
            # Preferir invoke si está disponible
            if hasattr(self.llm, "invoke"):
                resp = self.llm.invoke(prompt)
                # Normalizar respuesta
                if isinstance(resp, str):
                    return SimpleNamespace(content=resp)
                if hasattr(resp, "content"):
                    return SimpleNamespace(content=resp.content)
                gens = getattr(resp, "generations", None)
                if gens:
                    try:
                        text = gens[0][0].text if isinstance(gens[0], list) and hasattr(gens[0][0], "text") else str(gens)
                        return SimpleNamespace(content=text)
                    except Exception:
                        return SimpleNamespace(content=str(resp))
                return SimpleNamespace(content=str(resp))

            # Intentar generate
            if hasattr(self.llm, "generate"):
                result = self.llm.generate([{"role": "user", "content": prompt}])
                gens = getattr(result, "generations", None)
                if gens:
                    try:
                        text = gens[0][0].text if isinstance(gens[0], list) and hasattr(gens[0][0], "text") else str(gens)
                        return SimpleNamespace(content=text)
                    except Exception:
                        return SimpleNamespace(content=str(result))
                return SimpleNamespace(content=str(result))

            # Intentar llamada directa
            if callable(self.llm):
                r = self.llm(prompt)
                if isinstance(r, str):
                    return SimpleNamespace(content=r)
                if hasattr(r, "content"):
                    return SimpleNamespace(content=r.content)
                return SimpleNamespace(content=str(r))

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

print(f"[gemini] GEMINI_MODEL={'(none)' if not GEMINI_MODEL else GEMINI_MODEL}; LLM available: {bool(_real_llm)}")

gemini_llm = GeminiLLMWrapper(_real_llm, fallback_text="Respuesta simulada por fallback: LLM no configurado o modelo no disponible.")
