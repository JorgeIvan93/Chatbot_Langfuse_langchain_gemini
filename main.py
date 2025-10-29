"""
Application entrypoint: initializes logging, tracing, builds the LangGraph,
and runs the interactive chat loop powered by the Gemini model.
"""

import warnings  # controls Python warnings (optionally silenced via settings)
import logging  # configures log levels and handlers for the running process
from uuid import uuid4  # creates a simple session identifier per run

# Centralized configuration (loaded from .env by pydantic-settings)
from config import settings

# App logger (console + rotating file), created in services/standard_logger.py
from services.standard_logger import logger

# LangGraph builder and state definition for the conversation flow
from flow.graph_builder import build_chat_graph
from flow.state import ChatbotState

# Langfuse integration helpers (safe setup + optional callback handler)
from utils.langfuse_traces import setup_langfuse_tracer, get_langfuse_callback_handler

# Try to import Langfuse SDK helpers; if unavailable, define safe no-ops.
try:
    # observe/get_client are convenient helpers to create root/child spans
    from langfuse import observe, get_client
except Exception:

    def observe(*args, **kwargs):
        """Fallback no-op decorator when Langfuse is not available."""

        def wrap(fn):
            return fn

        return wrap

    def get_client():
        """Fallback no-op client getter when Langfuse is not available."""
        return None


# --- Warnings and third‑party log noise control (driven by settings) ---
# Keep the logic minimal: only toggle if explicitly requested via .env.
if settings.SILENCE_WARNINGS:
    warnings.filterwarnings("ignore")

if settings.QUIET_THIRD_PARTY:
    for _noisy in (
        "google",
        "google.api_core",
        "grpc",
        "opentelemetry",
        "opentelemetry.sdk",
        "tenacity",
        "httpx",
        "urllib3",
        "langchain_core._api.deprecation",
    ):
        logging.getLogger(_noisy).setLevel(logging.ERROR)


def _lower_console_handler_level(
    log: logging.Logger, level_name: str = "WARNING"
) -> None:
    """
    Lower ONLY the console handler level so the terminal stays clean while
    the file handler continues to capture INFO and DEBUG for troubleshooting.
    """
    try:
        level = getattr(logging, level_name.upper(), logging.WARNING)
    except Exception:
        level = logging.WARNING
    for h in log.handlers:
        if isinstance(h, logging.StreamHandler):
            h.setLevel(level)


# Apply the console downscaling (e.g., show WARNING+ in terminal; keep INFO in file)
_lower_console_handler_level(logger, settings.LOG_CONSOLE_LEVEL)


@observe(name="chat.turn")
def _observed_turn_invoke(
    chat_graph, state: ChatbotState, callbacks=None
) -> ChatbotState:
    """
    Execute a single chat turn under an observed span (if Langfuse is active).
    Also updates the trace with the user input and the model output.
    """
    lf = get_client()

    # Attach user input to the current trace (safe-guarded)
    try:
        if lf:
            lf.update_current_trace(
                input={"user_input": state.get("current_input", "")}
            )
    except Exception:
        # Never break the chat on observability issues
        pass

    # Invoke the graph with an optional Langfuse callback handler
    result = chat_graph.invoke(
        state, config={"callbacks": [callbacks]} if callbacks else {}
    )

    # Attach model output to the current trace (safe-guarded)
    try:
        if lf:
            lf.update_current_trace(output={"response": result.get("llm_response", "")})
    except Exception:
        pass

    return result


def initialize_application():
    """
    Build and compile the chat graph, and set up Langfuse tracing if enabled.
    Returns the compiled graph and the optional Langfuse client.
    """
    logger.info("Starting Chatbot initialization...")
    logger.info(f"Using LLM Model: {settings.gemini_model}")

    # Tracing setup (may return None if disabled or not available)
    langfuse_client = setup_langfuse_tracer()

    # Build the LangGraph once at startup
    chat_graph = build_chat_graph()
    logger.info("Initialization complete. Entering interactive loop.")
    return chat_graph, langfuse_client


def run_chat_loop(chat_graph, langfuse_client):
    """
    Run the interactive console loop. When Langfuse is enabled, wrap the whole
    session in a root span so every turn nests under it.
    """
    # Simple banner so users know the app context at a glance
    print("=" * 30)
    print(f"      {settings.APP_NAME.upper()} - VERSION {settings.APP_VERSION}")
    print("=" * 30)
    print(f"Powered by: Gemini Model ({settings.gemini_model}) and LangGraph.")
    print(
        "Observability:",
        "LangFuse Tracing ENABLED."
        if langfuse_client
        else "Standard Logging (LangFuse DISABLED).",
    )
    print("-" * 30)
    print("Welcome! Type 'exit' or 'quit' to end the session.")
    print("-" * 30)

    # Single Langfuse handler reused across invocations (recommended pattern)
    callback_handler = get_langfuse_callback_handler(
        langfuse_client, trace_name="chatbot_session_run"
    )

    # If Langfuse client is active, open a root span for the whole session
    lf_client = get_client() if langfuse_client else None
    session_id = f"session-{uuid4().hex[:8]}"

    if lf_client:
        # Root span groups all nested turns (cleaner trace in the UI)
        with lf_client.start_as_current_span(name="chat-session") as span:
            try:
                # Enrich the root trace with useful identifiers
                span.update_trace(
                    user_id="jorge.montes",  # adjust if you support multiple users
                    session_id=session_id,
                    tags=["local", "dev"],
                    metadata={"app_version": settings.APP_VERSION},
                )
            except Exception:
                pass

            _chat_loop_body(chat_graph, callback_handler)

    else:
        # No tracing: run the same loop with plain logging
        _chat_loop_body(chat_graph, callback_handler)

    # Ensure any buffered spans are sent before process exit
    if langfuse_client:
        try:
            langfuse_client.flush()
            logger.info("LangFuse traces flushed.")
        except Exception as e:
            logger.warning(f"LangFuse flush warning: {e}")


def _chat_loop_body(chat_graph, callback_handler):
    """
    Minimal console REPL: read user input, run the graph, print the model reply.
    """
    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            logger.info("Chat terminated by user.")
            break

        # Friendly exit commands
        if user_input.strip().lower() in {"exit", "quit"}:
            logger.info("Exiting chatbot.")
            break

        # Graph state for this turn; the graph will build upon `messages`
        initial_state: ChatbotState = {
            "messages": [],
            "current_input": user_input,
            "llm_response": "",
        }

        try:
            # If the callback handler exists, use the observed function
            if callback_handler:
                result = _observed_turn_invoke(
                    chat_graph, initial_state, callbacks=callback_handler
                )
            else:
                result = chat_graph.invoke(initial_state)

            final_response = result.get("llm_response") or "No response generated."
            print(f"Chatbot: {final_response}")

        except Exception as e:
            # Keep the session alive even if one turn fails
            logger.exception(f"Error durante la ejecución del grafo: {e}")
            print("Chatbot: An internal error prevented me from answering.")


if __name__ == "__main__":
    # Startup sequence: logs, graph, tracing, interactive loop
    logger.info("Application starting.")
    graph, langfuse = initialize_application()
    run_chat_loop(graph, langfuse)
