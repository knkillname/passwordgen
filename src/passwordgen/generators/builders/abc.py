"""Abstract base class for password generator builders.

Classes
-------
GeneratorBuilder
    Abstract base class for password generator builders.
"""

import abc

from ...generators.abc import PasswordGeneratorBase


class PasswordGeneratorBuilder(metaclass=abc.ABCMeta):
    """Abstract base class for password generator builders."""

    @abc.abstractmethod
    def build(self) -> PasswordGeneratorBase:
        """Create a password generator."""

    @abc.abstractmethod
    def reset(self) -> None:
        """Reset the builder."""
