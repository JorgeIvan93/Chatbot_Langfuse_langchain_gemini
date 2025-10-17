"""
punto de entrada

Funcionalidad:
- Construye el grafo de LangGraph llamando a `build_graph` desde `flow.graph`.
- Pide al usuario (por consola) que escriba el texto/pregunta a resumir o procesar.
- Invoca el grafo con la entrada como un diccionario {'text': <usuario>}.
- Imprime la salida final (campo 'output') devuelta por el grafo.

Nota sobre imports:
- `build_graph` se importa desde `flow.graph` (archivo local `flow/graph.py`).

"""

from flow.graph import build_graph


def run_interactive():
    """Construye el grafo y solicita input al usuario por consola.

    Lee la entrada de la consola usando input(), crea el diccionario de estado
    esperado por el grafo y ejecuta `graph.invoke()`.
    """

    # Construir el grafo que contiene los nodos y sus conexiones
    graph = build_graph()

    # Solicitar texto al usuario
    user_text = input("Introduce el texto o la pregunta que quieras procesar: ")

    # Preparar la entrada para el grafo (estado inicial)
    entrada = {"text": user_text}

    # Ejecutar el grafo de estado (síncrono) y obtener resultado
    resultado = graph.invoke(entrada)

    # Imprimir la salida final ('output')
    print("Respuesta final:", resultado.get("output"))


if __name__ == "__main__":
    run_interactive()
