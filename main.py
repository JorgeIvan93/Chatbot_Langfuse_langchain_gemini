"""
🚀 ¡Bienvenido a nuestro Chatbot Inteligente!

Este es el archivo principal de nuestro chatbot. Es como el botón de encendido
que pone todo en marcha. Cuando lo ejecutas:

1. Prepara el sistema de chat (como encender la computadora)
2. Te pregunta qué quieres saber (como un amigo que está listo para ayudar)
3. Procesa tu pregunta (piensa la respuesta)
4. Te muestra una respuesta clara y útil

Es muy fácil de usar - solo tienes que escribir tu pregunta y esperar la respuesta.
"""

import os
import sys
import logging
from flow.graph import construir_grafo

# Configurar logging para suprimir mensajes de depuración
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suprimir mensajes de TensorFlow
logging.getLogger('tensorflow').setLevel(logging.ERROR)
logging.getLogger('absl').setLevel(logging.ERROR)

# Redirigir STDERR a un archivo nulo
if sys.platform.startswith('win'):
    import ctypes
    kernel32 = ctypes.WinDLL('kernel32')
    kernel32.SetStdHandle(-12, None)  # STD_ERROR_HANDLE
    os.environ['PYTHONWARNINGS'] = 'ignore'  # Suprimir warnings de Python


def iniciar_chat():
    """
    Esta función es como el encargado de un restaurante:
    1. Prepara todo para atenderte
    2. Toma tu pedido (pregunta)
    3. La lleva a la cocina (procesa)
    4. Te trae la respuesta
    """

    print("🤖 ¡Hola! Soy tu asistente virtual.")
    print("💡 Puedes preguntarme lo que quieras y haré lo posible por ayudarte.")
    print("❔ Por ejemplo: '¿puedes explicarme qué es la inteligencia artificial?'")
    print("💬 Para cerrar el chat, escribe 'cerrar' en cualquier momento.")
    print("----------------------------------------")

    # Preparamos el sistema (como abrir el restaurante)
    sistema = construir_grafo()

    while True:
        try:
            # Pedimos la pregunta al usuario
            pregunta = input("\n👤 Tu pregunta: ")
            
            # Si el usuario quiere salir (ahora incluyendo 'cerrar')
            if pregunta.lower() in ['cerrar', 'salir', 'exit', 'quit', 'q']:
                print("\n👋 ¡Gracias por chatear conmigo! ¡Hasta pronto!")
                break

            # Preparamos la pregunta para procesarla
            entrada = {"texto": pregunta}

            print("\n🤔 Pensando...")
            # Procesamos la pregunta y obtenemos la respuesta
            resultado = sistema.invoke(entrada)

            # Mostramos la respuesta de manera amigable
            print("\n🤖 Respuesta:")
            print("----------------------------------------")
            print(resultado.get("salida", "Lo siento, no pude procesar tu pregunta."))
            print("----------------------------------------")
            print("💬 Para hacer otra pregunta, escribe tu pregunta.")
            print("💬 Para cerrar el chat, escribe 'cerrar'.")
            print("----------------------------------------")

        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta pronto! Gracias por usar el chatbot.")
            break
        except Exception as e:
            print(f"\n❌ Ups, algo salió mal: {str(e)}")
            print("Por favor, intenta de nuevo.")


if __name__ == "__main__":
    try:
        # Iniciamos el chat con un mensaje de bienvenida
        print("\n" + "="*50)
        print("🤖 Chatbot Inteligente - Versión 1.0")
        print("="*50 + "\n")
        
        iniciar_chat()
    except Exception as e:
        print(f"\n❌ Error al iniciar el chat: {str(e)}")
        print("Por favor, asegúrate de que todas las dependencias estén instaladas.")
