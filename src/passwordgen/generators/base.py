"""Core abstractions for password generation algorithms."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeAlias

PasswordConfig: TypeAlias = object


class PasswordGenerator(ABC):
    """Abstract interface for all password generators."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return user-visible algorithm name.

        Returns
        -------
        str
            Human-readable algorithm name.
        """

    @abstractmethod
    def generate(self, config: PasswordConfig) -> str:
        """Generate one secure password.

        Parameters
        ----------
        config : PasswordConfig
            Algorithm-specific configuration object.

        Returns
        -------
        str
            Newly generated password.
        """
