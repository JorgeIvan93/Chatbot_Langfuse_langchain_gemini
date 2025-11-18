"""
Initializes and wires Langfuse tracing for the application.
Provides a safe setup (esp. on Python 3.14) and a LangChain callback handler if available.
"""

from __future__ import annotations 
import sys  # Python version check to guard 3.14 behavior
from typing import Optional
from services.standard_logger import logger# Application logger (console + rotating file)
from config import settings # Centralized configuration (keys, host/base_url, flags) via pydantic-settings


def _get_base_url() -> str:
    """
    Resolve the Langfuse base URL from settings with a sensible fallback.
    """
    # Prefer the explicit BASE_URL if present (recommended in SDK v3)
    base_url = settings.LANGFUSE_BASE_URL or ""
    if base_url:
        return base_url

    # Fallback to HOST (legacy style) or the default EU endpoint
    return settings.LANGFUSE_HOST or "https://cloud.langfuse.com"


def setup_langfuse_tracer():
    """
    Initialize the Langfuse client if possible; otherwise return None.

    Behavior notes:
    - Python 3.14 guard: by default, tracing is disabled unless ENABLE_LANGFUSE=True,
      to avoid import-time issues in environments where the SDK still touches v1 paths.
    - Deferred import: we import Langfuse inside the function so the app can still run
      even if the SDK is not installed or incompatible.
    """
    # Guard for Python 3.14: only enable if explicitly requested in settings
    if sys.version_info >= (3, 14) and not settings.ENABLE_LANGFUSE:
        logger.warning(
            "Langfuse deshabilitado en Python 3.14 por incompatibilidad del SDK "
            "(usa Pydantic v1 en rutas internas). Continuamos con logging estándar."
        )
        return None

    # Import lazily to avoid breaking the application if the SDK is missing/incompatible
    try:
        from langfuse import Langfuse  # type: ignore
    except Exception as e:
        logger.warning(f"Langfuse no importable ({e}). Tracing deshabilitado.")
        return None

    # Attempt to construct the client with the provided credentials and base URL
    try:
        pk = settings.LANGFUSE_PUBLIC_KEY
        sk = settings.LANGFUSE_SECRET_KEY
        if not (pk and sk):
            logger.warning("Claves Langfuse no configuradas. Tracing deshabilitado.")
            return None

        lf = Langfuse(
            public_key=pk,
            secret_key=sk,
            base_url=_get_base_url(),
            flush_at=10,  # batch size before automatic flush
            flush_interval=60,  # periodic flush interval (seconds)
        )

        # Optional connectivity check (logs the result; does not raise)
        try:
            ok = lf.auth_check()
            logger.info(f"Langfuse auth_check(): {ok}")
            if not ok:
                logger.warning(
                    "Langfuse no autenticó. Revisa claves/base_url/proyecto."
                )
        except Exception as e:
            logger.warning(f"Langfuse auth_check() lanzó excepción: {e}")

        logger.info("Langfuse inicializado correctamente.")
        return lf

    except Exception as e:
        # Any construction error is logged and tracing is disabled (non-fatal for the app)
        logger.error(f"No se pudo inicializar Langfuse: {e}")
        return None


def get_langfuse_callback_handler(langfuse_client, trace_name: Optional[str] = None):
    """
    Return the LangChain CallbackHandler for Langfuse if available; otherwise None.

    Supports:
    - v3:   `from langfuse.langchain import CallbackHandler`
    - v2:   `from langfuse.callback.langchain import LangchainCallbackHandler`
    """
    # If there is no client (disabled or failed import), we simply do not attach callbacks
    if not langfuse_client:
        return None

    # Try the v3 integration first
    try:
        from langfuse.langchain import CallbackHandler  # type: ignore

        return CallbackHandler()
    except Exception:
        # Fallback to v2 path if present
        try:
            from langfuse.callback.langchain import (  # type: ignore
                LangchainCallbackHandler as CallbackHandler,
            )

            return CallbackHandler()
        except Exception as e:
            logger.warning(f"No se pudo crear Langfuse CallbackHandler: {e}")
            return None
