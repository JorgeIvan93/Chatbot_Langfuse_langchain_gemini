"""flujo de los mensajes, manejo de nodos y estados."""

from typing import Optional #se usa en el estado para definir que salida puede ser None al iniciar el chat
from pydantic import BaseModel   # indica informacion que guardamos
from langgraph.graph import StateGraph # modelo que maneja el flujo
from flow.nodes import (nodo_entrada_runnable, nodo_procesador_runnable, nodo_respuesta_runnable)


class EstadoApp(BaseModel):
    texto: str  #guarda lo que escribe el usuario
    salida: Optional[str] = None #respuesta del chatbot (puede estar vacío al inicio)


def construir_grafo():    #ruta del mensaje por los nodos, entrada, procesamiento y respuesta.
    
    # creacion de la ruta
    grafo = StateGraph(state_schema=EstadoApp)

    # agregamos los nodos a la ruta
    grafo.add_node("EstacionEntrada", nodo_entrada_runnable)
    grafo.add_node("EstacionProcesamiento", nodo_procesador_runnable)
    grafo.add_node("EstacionRespuesta", nodo_respuesta_runnable)

    # flujo del mensaje
    grafo.set_entry_point("EstacionEntrada")
    grafo.add_edge("EstacionEntrada", "EstacionProcesamiento")  
    grafo.add_edge("EstacionProcesamiento", "EstacionRespuesta")  

    # compilacion del grafo
    return grafo.compile()
