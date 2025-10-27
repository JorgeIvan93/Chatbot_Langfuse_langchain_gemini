from langchain_core.runnables import RunnableLambda  # crea nodos ejecutables
from services.gemini import asistente_gemini  # nuestro asistente Gemini
from utils.langfuse_logger import logger  # registro de eventos en Langfuse

def obtener_texto_del_estado(estado) -> str:
    if hasattr(estado, "texto"):
        return estado.texto
    elif isinstance(estado, dict):
        return estado.get("texto", "")
    return str(estado)

def nodo_entrada(estado):
    texto = obtener_texto_del_estado(estado)
    from flow.graph import EstadoApp
    return EstadoApp(texto=texto)

def nodo_procesador(estado):
    try:
        texto = obtener_texto_del_estado(estado)
        if not texto:
            return {"error": "por favor, ingresa un mensaje para responderlo"}

        respuesta = asistente_gemini.preguntar(texto)

        # Asegurar que la salida sea texto plano
        salida_texto = getattr(respuesta, "content", str(respuesta))

        logger.log("procesar_mensaje", {
            "entrada": texto,
            "salida": salida_texto
        })

        from flow.graph import EstadoApp
        return EstadoApp(texto=texto, salida=salida_texto)

    except Exception as e:
        return {"error": f"Error al procesar el mensaje: {str(e)}"}

def nodo_respuesta(estado):
    if isinstance(estado, dict) and "error" in estado:
        return {"error": estado["error"]}

    if hasattr(estado, "texto") and hasattr(estado, "salida"):
        texto = estado.texto
        salida = estado.salida
    elif isinstance(estado, dict):
        texto = estado.get("texto", "")
        salida = estado.get("salida", "")
    else:
        texto = str(estado)
        salida = ""

    return {
        "texto": texto,
        "salida": salida
    }

# Convertimos las funciones del chatbot en nodos ejecutables
nodo_entrada_runnable = RunnableLambda(nodo_entrada)
nodo_procesador_runnable = RunnableLambda(nodo_procesador)
nodo_respuesta_runnable = RunnableLambda(nodo_respuesta)