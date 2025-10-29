# Chatbot LangGraph con Gemini

Aplicación de consola basada en **LangGraph** que usa **Google Gemini** (vía LangChain) para responder al usuario, con **observabilidad opcional en Langfuse**. El proyecto prioriza una configuración centralizada (Pydantic Settings), buen logging y trazas reproducibles.

---

## ✨ Características

- **Conversación** orquestada con **LangGraph** (nodos y estado tipado).
- **Modelo LLM**: Gemini vía `langchain-google-genai`.
- **Config centralizada** con `pydantic-settings` (sin acceder a `os.environ` en el código).
- **Logging** a consola y archivo con rotación.
- **Tracing opcional** con **Langfuse** (handler para LangChain + spans por sesión/turno).
- **Comentarios pedagógicos** en el código para facilitar el mantenimiento.

---

## 🧱 Requisitos

- **Python 3.13** (recomendado para usar Langfuse hoy).
  - *Nota:* Con Python 3.14, el SDK de Langfuse puede fallar al importar debido a rutas internas que dependen de Pydantic v1. En 3.14 el tracing está deshabilitado por defecto en el código.
- Clave de **Google AI Studio** (Gemini Developer API) — *no* Vertex AI.
- (Opcional) Proyecto y llaves de **Langfuse Cloud** (EU/US).

---

## 🧰 Stack principal

- **LangChain v1** + **`langchain-google-genai`** (Gemini).
- **LangGraph** para orquestación.
- **Pydantic v2** + `pydantic-settings` para `.env`.
- **Langfuse SDK v3** (tracing opcional).
- Logging estándar de Python con `RotatingFileHandler`.

---

## 📁 Estructura del proyecto
.
├─ config/
│  ├─ init.py
│  └─ config.py            # Loads settings from .env using Pydantic
├─ flow/
│  ├─ init.py
│  ├─ graph_builder.py     # Builds and compiles the LangGraph
│  ├─ processing_nodes.py  # Nodes for user input and LLM response
│  └─ state.py             # Defines the chatbot state (TypedDict)
├─ services/
│  ├─ init.py
│  ├─ standard_logger.py   # Logger setup (console + file rotation)
│  └─ gemini_client.py     # Wrapper for Gemini model via LangChain
├─ utils/
│  ├─ init.py
│  └─ langfuse_traces.py   # Safe Langfuse setup + LangChain callback handler
├─ logs/                   # Log files (rotated)
├─ .env                    # Sensitive keys (ignored by Git)
├─ .env.example            # Template for environment variables
├─ main.py                 # Application entrypoint (loop + tracing)
└─ requirements.txt        # Dependencies

## ⚙️ Configuration
Create a `.env` file based on `.env.example`:

```dotenv
# Gemini API
GOOGLE_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-pro
LLM_TEMPERATURE=0.7

# Logging
LOG_CONSOLE_LEVEL=WARNING
SILENCE_WARNINGS=true
QUIET_THIRD_PARTY=true

# App Info
APP_NAME=Advanced LangGraph Chatbot
APP_VERSION=1.0.1

# Langfuse (optional)
LANGFUSE_PUBLIC_KEY=pk-lf-xxxxxxxx
LANGFUSE_SECRET_KEY=sk-lf-xxxxxxxx
LANGFUSE_BASE_URL=https://cloud.langfuse.com
ENABLE_LANGFUSE=true
LANGFUSE_TRACING_ENVIRONMENT=development
LANGFUSE_DEBUG=True
LANGFUSE_SAMPLE_RATE=1.0
```

🚀 How It Works

Startup: loads settings, configures logger, builds LangGraph, and initializes Langfuse (if enabled).
Chat Loop: reads user input, processes through graph nodes, and returns Gemini’s response.
Observability: when Langfuse is active, creates a root span for the session and spans for each turn.


🛡️ Security Notes

.env is ignored by Git; never commit API keys.
Rotate keys if shared accidentally.
Avoid logging sensitive data (the logger is configured to keep logs safe).


📌 Recommendations

Use Python 3.13 for full Langfuse compatibility (3.14 disables tracing by default).
Keep dependencies updated and remove google-generativeai if using langchain-google-genai >= 3.0.0.


License
MIT
