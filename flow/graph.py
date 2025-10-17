"""
flow/graph.py

¡Bienvenido al mapa de nuestro chatbot! 🗺️

Este archivo es como el plano que muestra cómo viaja cada mensaje desde que lo escribes
hasta que recibes una respuesta. Imagina que es como una línea de metro donde cada
estación (nodo) tiene una tarea específica.

¿Qué necesitamos para construir este mapa?
1. BaseModel: Es como un formulario que nos dice qué información guardamos
2. StateGraph: Es nuestro constructor de mapas, viene de la biblioteca LangGraph
3. Los nodos: Son las "estaciones" por donde pasa cada mensaje
"""

from typing import Optional
from pydantic import BaseModel
from langgraph.graph import StateGraph
from flow.nodes import (
    nodo_entrada_runnable,
    nodo_procesador_runnable,
    nodo_respuesta_runnable
)


class EstadoApp(BaseModel):
    """
    Este es como el sobre que lleva la información entre estaciones.
    
    Tiene dos bolsillos:
    - texto: donde guardamos lo que escribe el usuario
    - salida: donde ponemos la respuesta del chatbot (puede estar vacío al inicio)
    """
    texto: str
    salida: Optional[str] = None


def construir_grafo():
    """
    Esta función es como armar el mapa del metro: conecta todas las estaciones
    en el orden correcto para que el mensaje sepa por dónde tiene que pasar.
    
    Es como decir:
    1. Empiezas en la estación de entrada
    2. Luego vas a la estación de procesamiento
    3. Terminas en la estación de respuesta
    """

    # Creamos un nuevo mapa usando nuestro sobre especial (EstadoApp)
    grafo = StateGraph(state_schema=EstadoApp)

    # Registramos cada estación en el mapa
    grafo.add_node("EstacionEntrada", nodo_entrada_runnable)
    grafo.add_node("EstacionProcesamiento", nodo_procesador_runnable)
    grafo.add_node("EstacionRespuesta", nodo_respuesta_runnable)

    # Dibujamos las líneas que conectan las estaciones
    grafo.set_entry_point("EstacionEntrada")  # Aquí empieza el viaje
    grafo.add_edge("EstacionEntrada", "EstacionProcesamiento")  # Primera conexión
    grafo.add_edge("EstacionProcesamiento", "EstacionRespuesta")  # Segunda conexión

    # El mapa está listo para usarse
    return grafo.compile()
