"""
Langfuse tracer setup for observability (Python SDK v3).
Handles safe initialization and returns global client instance.
"""

from __future__ import annotations
import sys
from app.services.standard_logger import logger
from app.core.config import settings


def _get_host() -> str:
    """
    Return Langfuse host or default cloud host.
    """
    return settings.langfuse_base_url or "https://cloud.langfuse.com"


def setup_langfuse_tracer():
    """
    Initialize Langfuse client safely (v3).
    Return Langfuse client or None if disabled or error.
    """
    if sys.version_info >= (3, 14) and not settings.enable_langfuse:
        logger.warning("Langfuse disabled on Python 3.14 unless explicitly enabled.")
        return None

    try:
        # v3 client and singleton accessor
        from langfuse import Langfuse, get_client
    except Exception as e:
        logger.warning(f"Langfuse not importable ({e}). Tracing disabled.")
        return None

    try:
        pk = settings.langfuse_public_key
        sk = settings.langfuse_secret_key
        if not (pk and sk):
            logger.warning("Langfuse keys missing. Tracing disabled.")
            return None

        # Initialize client; v3 uses 'host' parameter
        Langfuse(
            public_key=pk,
            secret_key=sk,
            host=_get_host(),
            debug=settings.langfuse_debug,
        )

        lf = get_client()

        try:
            ok = lf.auth_check()
            logger.info(f"Langfuse auth_check(): {ok}")
        except Exception as e:
            logger.warning(f"Langfuse auth_check() exception: {e}")

        logger.info("Langfuse initialized successfully.")
        return lf

    except Exception as e:
        logger.error(f"Failed to initialize Langfuse: {e}")
        return None


# Global Langfuse client instance (None if disabled)
langfuse_client = setup_langfuse_tracer()