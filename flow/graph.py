"""
Define y compila el grafo de estado usado por la aplicación.

Este módulo construye un `StateGraph` (de LangGraph) con un `state_schema` que
describe la forma del estado que se pasa entre nodos. También registra los
nodos (`InputNode`, `TextLoaderNode`, `AnswerNode`) y sus conexiones.

Imports:
- `BaseModel` de `pydantic` para definir el esquema del estado.
- `StateGraph` desde `langgraph.graph` (paquete externo `langgraph`).
- Los `Runnable` de los nodos vienen desde `flow.nodes` (módulo local).
"""

from typing import Optional
from pydantic import BaseModel

# `StateGraph` es la clase principal que representa un grafo de estado en LangGraph.
# Se importa desde el paquete `langgraph` instalado en el entorno.
from langgraph.graph import StateGraph

# Los nodos del grafo (instancias Runnable) se definen en el módulo local
# `flow.nodes`.
from flow.nodes import input_node_runnable, text_loader_runnable, answer_node_runnable


class AppState(BaseModel):
    """Modelo Pydantic que describe el estado que viaja entre los nodos.

    Campos:
    - text: texto de entrada o pregunta del usuario.
    - output: resultado generado por el LLM o por el flujo (opcional).
    """

    text: str
    output: Optional[str] = None


def build_graph():
    """Construye y compila un StateGraph usando `AppState` como esquema.

    Retorna:
        graph.compile() -> grafo compilado listo para invocar mediante `invoke`.
    """

    # Instanciar el grafo con el esquema de estado Pydantic
    graph = StateGraph(state_schema=AppState)

    # Registrar nodos: cada uno es un Runnable creado en `flow.nodes`.
    graph.add_node("InputNode", input_node_runnable)
    graph.add_node("TextLoaderNode", text_loader_runnable)
    graph.add_node("AnswerNode", answer_node_runnable)

    # Definir el punto de entrada y las aristas (flujo)
    graph.set_entry_point("InputNode")
    graph.add_edge("InputNode", "TextLoaderNode")
    graph.add_edge("TextLoaderNode", "AnswerNode")

    # Compilar y devolver el grafo listo para ejecutar
    return graph.compile()
