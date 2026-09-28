"""Compatibility entry point for hosting platforms that run ``uvicorn main:app``."""

from backend.main import app

__all__ = ["app"]
