"""Configuration management for the application."""

from secure_passwords.config.manager import ConfigManager
from secure_passwords.config.schema import AppConfig

__all__ = ["AppConfig", "ConfigManager"]
