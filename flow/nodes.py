# flow/nodes.py
# Definición de los nodos (runnables) que forman parte del grafo.
# Cada nodo es una función que recibe el `state` actual y retorna un diccionario
# con los campos que actualizan el estado. Luego se envuelven en `RunnableLambda`
# para ser usados por LangGraph.
# Imports:
# - `RunnableLambda` desde `langchain_core.runnables` (parte de LangChain Core).
# - `gemini_llm` desde `services.gemini` (wrapper local que normaliza llamadas al LLM).

from typing import Any
from langchain_core.runnables import RunnableLambda
from services.gemini import gemini_llm


def _get_text_from_state(state: Any) -> str:
    """Extrae el campo 'text' desde el estado, sea dict o BaseModel."""
    if hasattr(state, "dict"):
        data = state.dict()
    else:
        data = dict(state)
    return data.get("text", "")


def input_node(state):
    """Nodo de entrada: toma el texto del usuario y lo pasa al siguiente nodo."""
    return {"text": _get_text_from_state(state)}


def text_loader_node(state):
    """Nodo que simula la carga de contenido sobre el texto dado."""
    topic = _get_text_from_state(state)
    return {"text": f"Contenido simulado sobre {topic}"}


def answer_node(state):
    """Nodo que invoca el LLM para resumir el contenido."""
    prompt = f"Resume el siguiente contenido: {_get_text_from_state(state)}"
    # Intenta invocar el LLM usando diferentes APIs
    try:
        response = gemini_llm.invoke(prompt)
        content = getattr(response, "content", str(response))
    except Exception:
        try:
            result = gemini_llm.generate([{"role": "user", "content": prompt}])
            content = getattr(result, "generations", None)
            if content:
                content = content[0][0].text if isinstance(content[0], list) and hasattr(content[0][0], "text") else str(content)
            else:
                content = str(result)
        except Exception:
            try:
                content = gemini_llm(prompt)
            except RuntimeError as e:
                content = f"Error invoking LLM: {e}"
            except Exception as e:
                content = f"Error invoking LLM: {e}"
    return {"output": content}

# Envuelve cada función como Runnable para el grafo
input_node_runnable = RunnableLambda(input_node)
text_loader_runnable = RunnableLambda(text_loader_node)
answer_node_runnable = RunnableLambda(answer_node)
