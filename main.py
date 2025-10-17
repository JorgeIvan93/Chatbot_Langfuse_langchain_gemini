#archivo principal para el chatbot. es la puerta de entrada que inicia todo el proceso del chat.

import os
import sys
import logging #importar el modulo de logging para manejar los mensajes de log
from flow.graph import construir_grafo #importa la funcion que construye el grafo de flujo de mensajes

# Configurar logging para suprimir mensajes de depuración
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suprimir mensajes de TensorFlow sirve para que no muestre muchos mensajes en consola
logging.getLogger('tensorflow').setLevel(logging.ERROR)
logging.getLogger('absl').setLevel(logging.ERROR)

# Redirigir STDERR a un archivo nulo
if sys.platform.startswith('win'):
    import ctypes
    kernel32 = ctypes.WinDLL('kernel32')
    kernel32.SetStdHandle(-12, None)  # setea el manejador de error estándar a nulo
    os.environ['PYTHONWARNINGS'] = 'ignore'  # Suprimir warnings de Python


def iniciar_chat(): #incia el chat con el usuario y lo mantiene activo hasta que el usuario decida salir.

    #mensaje de bienvenida 
    print("¡Hola! Soy tu asistente virtual.")
    print("Puedes preguntarme lo que quieras y haré lo posible por ayudarte.")
    print("Para cerrar el chat, escribe 'cerrar' en cualquier momento.")
    print("__________________________________________________")

    #preparamos el sistema de flujo de mensajes
    sistema = construir_grafo()
        #bucle principal del chat
    while True:
        try:
            # Pedimos la pregunta al usuario
            pregunta = input("\nEscribe tu pregunta: ")
            
            #condicional si el usuario quiere salir estandarizando varios comandos y el tipo de letra
            if pregunta.lower() in ['cerrar', 'salir', 'exit', 'quit', 'q']:
                print("\n¡Gracias por chatear conmigo! ¡Hasta pronto!")
                break

            # Preparamos la pregunta para procesarla
            entrada = {"texto": pregunta}

            print("\n Preparando la respuesta mas adecuada, espera unos segundos...")
            # Procesamos la pregunta y obtenemos la respuesta
            resultado = sistema.invoke(entrada)

            # Mostramos la respuesta de manera amigable
            print("\nTu Respuesta es:")
            print("______________________________________________")
            print(resultado.get("salida", "Lo siento, no pude procesar tu pregunta."))
            print("______________________________________________")
            print(" Si quieres seguir con la conversacion, escribe tu proxima pregunta.")
            print(" Para cerrar el chat, escribe 'cerrar', 'quit', 'exit' o 'salir'.")
            print("______________________________________________")

        except KeyboardInterrupt:
            print("\n\nGracias por usar el chatbot. ¡te espero pronto!.")
            break
        except Exception as e:
            print(f"\n Lo siento, algo salió mal: {str(e)}")
            print("Por favor, intenta preguntarme nuevamente.")


if __name__ == "__main__":
    try:
        # Iniciamos el chat con un mensaje de bienvenida
        print("\n" + "="*50)
        print("Chatbot Inteligente - Versión 1.0")
        print("="*50 + "\n")
        
        iniciar_chat()
    except Exception as e:
        print(f"\n Error al iniciar el chat: {str(e)}")
        print("Por favor, asegúrate de que todas las dependencias estén instaladas.")
