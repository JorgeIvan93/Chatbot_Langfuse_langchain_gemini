# Chatbot LangGraph con Gemini

Aplicación de chatbot basada en LangGraph que utiliza el modelo Gemini de Google AI para procesar y responder preguntas.

## Características

- Utiliza LangGraph para gestionar el flujo de la conversación
- Integración con Gemini (Google AI) como LLM
- Manejo de estado y flujo mediante grafos
- Logging con LangFuse para monitoreo

## Requisitos

- Python 3.8+
- Cuenta de Google AI con acceso a Gemini
- API Key de Google AI (Gemini)
- API Key de LangFuse (opcional, para logging)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/JorgeIvan93/Chatbot_Langfuse_langchain_gemini.git
cd Chatbot_Langfuse_langchain_gemini
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
   - Copiar `.env.example` a `.env`
   - Añadir las API keys necesarias

## Uso

1. Activar el entorno virtual:
```bash
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

2. Ejecutar la aplicación:
```bash
python main.py
```

## Estructura del Proyecto

- `main.py`: Punto de entrada de la aplicación
- `flow/`: Módulos del grafo de conversación
  - `graph.py`: Definición del grafo de estado
  - `nodes.py`: Nodos del grafo (input, procesamiento, respuesta)
- `services/`: Servicios externos
  - `gemini.py`: Wrapper para la API de Gemini
- `utils/`: Utilidades
  - `langfuse_logger.py`: Logger para LangFuse
- `config.py`: Configuración del proyecto
- `requirements.txt`: Dependencias del proyecto

## Contribuir

1. Fork del repositorio
2. Crear rama para la feature (`git checkout -b feature/nombre`)
3. Commit de cambios (`git commit -am 'Añadir feature'`)
4. Push a la rama (`git push origin feature/nombre`)
5. Crear Pull Request

## Licencia

MIT