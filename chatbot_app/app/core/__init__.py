"""Expose Settings model and a singleton 'settings' to the rest of the app."""

from .config import Settings as Settings 
from .config import settings as settings 

__all__ = ["Settings", "settings"]