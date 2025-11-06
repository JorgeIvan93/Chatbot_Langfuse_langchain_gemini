"""
Sets up the application logger (console + rotating file) with optional noise reduction.
Keeps warnings under control and prevents third‑party libraries from flooding the console.
"""

import logging  # Python standard logging framework
import warnings  # Built‑in warnings control, routed into logging if desired
from logging.handlers import (RotatingFileHandler,)  # File handler with size‑based rotation
from pathlib import Path  # Cross‑platform filesystem paths

LOGGER_NAME = "AdvancedChatbotLogger"
LOG_LEVEL = logging.INFO

# Libraries that tend to be verbose in INFO/DEBUG.
# We set them to ERROR later when quiet_third_party=True.
NOISY_LOGGERS = (
    "google",
    "google.api_core",
    "grpc",
    "opentelemetry",
    "opentelemetry.sdk",
    "tenacity",
    "httpx",
    "urllib3",
    "langchain_core._api.deprecation",
)


def setup_logger(
    level: int | str = LOG_LEVEL,
    quiet_third_party: bool = True,
    silence_warnings: bool = True,
) -> logging.Logger:
    """
    Create (or return) the app logger with console and rotating-file handlers.

    - Console: human-friendly messages for interactive runs.
    - File:    persistent history at logs/app.log with rotation.
    - Warnings: optionally silenced or forwarded into logging.
    - Third‑party noise: optionally reduced to ERROR level.
    """
    # Route Python warnings through the logging system (so they can be filtered/formatted consistently)
    logging.captureWarnings(True)

    # Globally silence warnings if requested (use False in dev to see deprecations)
    if silence_warnings:
        warnings.filterwarnings("ignore")

    # Get or create the application logger
    app_logger = logging.getLogger(LOGGER_NAME)
    app_logger.setLevel(level)

    # Configure handlers only once to avoid duplicates on repeated imports
    if not app_logger.handlers:
        # Shared formatter for both console and file handlers
        fmt = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # --- Console handler: visible in terminal runs ---
        ch = logging.StreamHandler()  # writes to stderr by default
        ch.setFormatter(fmt)
        ch.setLevel(level)  # further adjusted at runtime if needed
        app_logger.addHandler(ch)

        # --- Rotating file handler: keeps history without growing unbounded ---
        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)  # ensure logs/ exists
        fh = RotatingFileHandler(
            log_dir / "app.log",
            maxBytes=5_000_000,  # ~5 MB per file
            backupCount=3,  # keep up to 3 old files
            encoding="utf-8",
        )
        fh.setFormatter(fmt)
        fh.setLevel(level)
        app_logger.addHandler(fh)

    # Reduce verbosity of noisy libraries if requested
    if quiet_third_party:
        for name in NOISY_LOGGERS:
            logging.getLogger(name).setLevel(logging.ERROR)

    # Safety note: do not log secrets (API keys, tokens, PII) at any level
    return app_logger


# Create the shared logger instance on import, so other modules can use:
#   from services.standard_logger import logger
logger = setup_logger()
