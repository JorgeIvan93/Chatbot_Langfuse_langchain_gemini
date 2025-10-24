from langchain_core.runnables import RunnableLambda #crea nodos ejecutables
from services.gemini import AsistenteGemini
from utils.langfuse_logger import logger #registro de eventos en Langfuse

def obtener_texto_del_estado(estado) -> str:   #busca el texto en el estado proporcionado en graph
    #verificamos que tipo de estado es para extraer el texto y evitar errores de tipos de escritura
    # Si es un objeto Pydantic
    if hasattr(estado, "texto"):
        return estado.texto 
    # Si es un diccionario
    elif isinstance(estado, dict):
        return estado.get("texto", "")
    # Si es otro tipo de objeto
    return str(estado)


def nodo_entrada(estado):
    #Recibe el mensaje del usuario y lo prepara para procesarlo
    texto = obtener_texto_del_estado(estado)
    from flow.graph import EstadoApp #importamos el esquema de estado
    return EstadoApp(texto=texto)


def nodo_procesador(estado):
    #Procesa el mensaje y genera la respuesta, nuestro asistente Gemini lee el mensaje y genera una respuesta
    try:
        # Extraer el texto del mensaje
        texto = obtener_texto_del_estado(estado)
        
        # Si no hay texto, devuelve un mensaje de error
        if not texto:
            return {"error": "porfavor, ingresa un mensaje para responderlo"}
        
        # obtiene respuesta del modelo de gemini
        respuesta = asistente_gemini.preguntar(texto)
        
        # registra la interacción
        logger.log("procesar_mensaje", {
            "entrada": texto,
            "salida": respuesta
        })
        
        # Devuelve el EstadoApp actualizado
        from flow.graph import EstadoApp
        return EstadoApp(texto=texto, salida=respuesta.content)
        
    except Exception as e:
        # Si hay un error, devolvuelve un mensaje de error
        return {
            "error": f"Error al procesar el mensaje: {str(e)}"
        }


def nodo_respuesta(estado):    #Formatea y devuelve la respuesta final
    # Si el estado es un diccionario con error
    if isinstance(estado, dict) and "error" in estado:
        return {"error": estado["error"]}
    
    # Si el estado es un objeto Pydantic entrega los valores correspondientes
    if hasattr(estado, "texto") and hasattr(estado, "salida"):
        texto = estado.texto
        salida = estado.salida
    # Si el estado es un diccionario devuelve los valores correspondientes
    elif isinstance(estado, dict):
        texto = estado.get("texto", "")
        salida = estado.get("salida", "")
    # Caso por defecto devuelve el estado como texto y una salida vacía
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
