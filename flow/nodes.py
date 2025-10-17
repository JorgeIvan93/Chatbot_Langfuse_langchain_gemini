# flow/nodes.py
# Este archivo es el cerebro de nuestro chatbot. Aquí definimos las diferentes
# "estaciones" por las que pasa cada mensaje antes de dar una respuesta.

from langchain_core.runnables import RunnableLambda
from services.gemini import asistente_gemini
from utils.langfuse_logger import logger

def obtener_texto_del_estado(estado) -> str:
    """
    Esta función es como un ayudante que busca el mensaje en diferentes lugares.
    Es como buscar un papel que puede estar en diferentes cajones.
    """
    # Si es un objeto Pydantic
    if hasattr(estado, "texto"):
        return estado.texto
    # Si es un diccionario
    elif isinstance(estado, dict):
        return estado.get("texto", "")
    # Si es otro tipo de objeto
    return str(estado)


def nodo_entrada(estado):
    """
    Primera estación: Recibe el mensaje del usuario
    Es como una recepcionista que toma tu mensaje y lo prepara para procesarlo
    """
    texto = obtener_texto_del_estado(estado)
    from flow.graph import EstadoApp
    return EstadoApp(texto=texto)


def nodo_procesador(estado):
    """
    Segunda estación: Procesa el mensaje y genera la respuesta
    Aquí es donde la magia ocurre: nuestro asistente Gemini lee tu mensaje
    y genera una respuesta inteligente.
    """
    try:
        # Extraer el texto del mensaje
        texto = obtener_texto_del_estado(estado)
        
        # Si no hay texto, devolver un mensaje de error
        if not texto:
            return {"error": "No se proporcionó texto para procesar"}
        
        # Obtener respuesta del modelo
        respuesta = asistente_gemini.preguntar(texto)
        
        # Registrar la interacción
        logger.log("procesar_mensaje", {
            "entrada": texto,
            "salida": respuesta
        })
        
        # Devolver un objeto EstadoApp actualizado
        from flow.graph import EstadoApp
        return EstadoApp(texto=texto, salida=respuesta.content)
        
    except Exception as e:
        # Si hay un error, devolver un mensaje de error
        return {
            "error": f"Error al procesar el mensaje: {str(e)}"
        }


def nodo_respuesta(estado):
    """
    Tercera estación: Formatea y devuelve la respuesta final
    """
    # Si el estado es un diccionario con error
    if isinstance(estado, dict) and "error" in estado:
        return {"error": estado["error"]}
    
    # Si el estado es un objeto Pydantic
    if hasattr(estado, "texto") and hasattr(estado, "salida"):
        texto = estado.texto
        salida = estado.salida
    # Si el estado es un diccionario
    elif isinstance(estado, dict):
        texto = estado.get("texto", "")
        salida = estado.get("salida", "")
    # Caso por defecto
    else:
        texto = str(estado)
        salida = ""
    
    return {
        "texto": texto,
        "salida": salida
    }


# Convertimos nuestras funciones en "estaciones" del chatbot
nodo_entrada_runnable = RunnableLambda(nodo_entrada)
nodo_procesador_runnable = RunnableLambda(nodo_procesador)
nodo_respuesta_runnable = RunnableLambda(nodo_respuesta)
