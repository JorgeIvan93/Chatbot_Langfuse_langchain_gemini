# archivo principal para el chatbot. es la puerta de entrada que inicia todo el proceso del chat.
from config import config
import sys
import logging  # importar el módulo de logging para manejar los mensajes de log
from flow.graph import construir_grafo  # importa la función que construye el grafo de flujo de mensajes

# Configurar logging para suprimir mensajes de depuración

logging.getLogger('tensorflow').setLevel(logging.ERROR)
logging.getLogger('absl').setLevel(logging.ERROR)

# Redirigir STDERR a un archivo nulo
if sys.platform.startswith('win'):
    import ctypes
    kernel32 = ctypes.WinDLL('kernel32')
    kernel32.SetStdHandle(-12, None)  # setea el manejador de error estándar a nulo
    # Suprimir warnings de Python
    import os
    os.environ['PYTHONWARNINGS'] = 'ignore'
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def iniciar_chat():  # inicia el chat con el usuario y lo mantiene activo hasta que el usuario decida salir.

    # mensaje de bienvenida
    print("¡Hola! Soy tu asistente virtual.")
    print("Puedes preguntarme lo que quieras y haré lo posible por ayudarte.")
    print("Para cerrar el chat, escribe 'cerrar' en cualquier momento.")
    print("__________________________________________________")

    # preparamos el sistema de flujo de mensajes
    sistema = construir_grafo()

    # bucle principal del chat
    while True:
        try:
            # Pedimos la pregunta al usuario
            pregunta = input("Escribe tu pregunta: ")

            # condicional si el usuario quiere salir estandarizando varios comandos y el tipo de letra
            if pregunta.lower() in ['cerrar', 'salir', 'exit', 'quit', 'q']:
                print("¡Gracias por chatear conmigo! ¡Hasta pronto!")
                break

            # Preparamos la pregunta para procesarla
            entrada = {"texto": pregunta}

            print(" Preparando la respuesta más adecuada, espera unos segundos...")
            # Procesamos la pregunta y obtenemos la respuesta
            resultado = sistema.invoke(entrada)

            # Mostramos la respuesta de manera amigable
            print("Tu Respuesta es:")
            print("______________________________________________")
            print(resultado.get("salida", "Lo siento, no pude procesar tu pregunta."))
            print("______________________________________________")
            print(" Si quieres seguir con la conversación, escribe tu próxima pregunta.")
            print(" Para cerrar el chat, escribe 'cerrar', 'quit', 'exit' o 'salir'.")
            print("______________________________________________")

        except KeyboardInterrupt:
            print("Gracias por usar el chatbot. ¡Te espero pronto!.")
            break
        except Exception as e:
            print(f" Lo siento, algo salió mal: {str(e)}")
            print("Por favor, intenta preguntarme nuevamente.")


if __name__ == "__main__":
    try:
        # Iniciamos el chat con un mensaje de bienvenida
        print("" + "="*50)
        print("Chatbot Inteligente - Versión 1.0")
        print("="*50 + "")

        iniciar_chat()
    except Exception as e:
        print(f" Error al iniciar el chat: {str(e)}")
        print("Por favor, asegúrate de que todas las dependencias estén instaladas.")
