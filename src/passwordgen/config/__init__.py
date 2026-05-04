"""Configuration management for the application."""

from passwordgen.config.manager import ConfigManager
from passwordgen.config.schema import AppConfig

__all__ = ["AppConfig", "ConfigManager"]
