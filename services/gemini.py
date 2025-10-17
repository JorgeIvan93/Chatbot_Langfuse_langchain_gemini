#intérprete con el modelo Gemini, verifica que siempre obtengamos una respuesta comprensible.

import os # lee variables de entorno 
from types import SimpleNamespace # estructura simple para respuestas
from config import GEMINI_API_KEY # clave de API para Gemini

# Intentamos importar el chat de Gemini
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    modelo_base = ChatGoogleGenerativeAI(
        model="gemini-pro", 
        temperature=0.7, # nivel de creatividad en respuestas
        google_api_key=GEMINI_API_KEY,
    )
except Exception:       # Si falla la importación, usamos None
    ChatGoogleGenerativeAI = None
    modelo_base = None


class AsistenteGemini: #herramienta para hablar con gemini, generando respuestas comprensibles
    # funcion para inicializar el asistente generando respuestas al usuario al conectarse a gemini 
    def __init__(self, modelo=modelo_base, mensaje_respaldo: str = None): 
        self.modelo = modelo
        self.mensaje_respaldo = mensaje_respaldo or "Lo siento, no puedo conectar con Gemini en este momento."

    def preguntar(self, pregunta: str): #hacemos una pregunta y obtenenemos una respuesta.
        
        # Si no podemos conectar con Gemini, usamos el mensaje de respaldo
        if not self.modelo:
            return SimpleNamespace(content=self.mensaje_respaldo)

        try:
            # Primera forma: pregunta directa invocando el modelo
            if hasattr(self.modelo, "invoke"):
                respuesta = self.modelo.invoke(pregunta)
                #intentamos que la respuesta sea entendible
                if isinstance(respuesta, str):
                    return SimpleNamespace(content=respuesta)
                    # Si la respuesta tiene atributo content, lo usamos
                if hasattr(respuesta, "content"):
                    return SimpleNamespace(content=respuesta.content)
                    # Si la respuesta tiene generaciones, intentamos extraer texto
                generaciones = getattr(respuesta, "generations", None)
                if generaciones:
                    try:
                        # Extraemos el texto de la primera generación usando atributos para evitar errores
                        texto = generaciones[0][0].text if isinstance(generaciones[0], list) and hasattr(generaciones[0][0], "text") else str(generaciones)
                        return SimpleNamespace(content=texto)
                    except Exception:
                        return SimpleNamespace(content=str(respuesta))
                return SimpleNamespace(content=str(respuesta))

            # generación de modelo estructurado para obtener respuesta
            if hasattr(self.modelo, "generate"):
                resultado = self.modelo.generate([{"role": "user", "content": pregunta}])
                generaciones = getattr(resultado, "generations", None)
                #intentamos extraer texto de las generaciones
                if generaciones:
                    try:
                        texto = generaciones[0][0].text if isinstance(generaciones[0], list) and hasattr(generaciones[0][0], "text") else str(generaciones)
                        return SimpleNamespace(content=texto)
                    # Si falla, devolvemos el resultado como cadena
                    except Exception:
                        return SimpleNamespace(content=str(resultado))
                return SimpleNamespace(content=str(resultado))

            # llamada simple 
            if callable(self.modelo):
                respuesta = self.modelo(pregunta)
                if isinstance(respuesta, str):
                    return SimpleNamespace(content=respuesta)
                    # Si la respuesta tiene atributo content, lo usamos
                if hasattr(respuesta, "content"):
                    return SimpleNamespace(content=respuesta.content)
                return SimpleNamespace(content=str(respuesta))
            # Si nada de lo anterior funciona, devolvemos el modelo como cadena
            return SimpleNamespace(content=str(self.llm))

        except Exception as e:
            # Ajusta el mensaje si es error de modelo no encontrado
            msg = str(e)
            if "not found" in msg.lower() or "models/" in msg.lower() or "NotFound" in msg:
                raise RuntimeError(
                    f"LLM model error: {msg}. Verifica que la variable de entorno GEMINI_MODEL y la clave GEMINI_API_KEY sean correctas y que el modelo exista. Ejecuta ListModels para ver los modelos disponibles."
                ) from e
            raise
    # permitimos llamar al asistente directamente
    def __call__(self, prompt: str):
        return self.invoke(prompt)


# Inicializar LLM real si está disponible y se proporcionó clave
GEMINI_MODEL = os.getenv("GEMINI_MODEL")
_real_llm = None
# si el chat de gemini está disponible y tenemos clave intentamos crear la instancia para usar el modelo
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
