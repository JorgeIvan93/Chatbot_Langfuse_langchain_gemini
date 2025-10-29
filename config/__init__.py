"""Expose Settings model and a singleton 'settings' to the rest of the app."""

from .config import (
    Settings,
    settings,
)  # Re-export Pydantic Settings and loaded instance

__all__ = ["Settings", "settings"]
