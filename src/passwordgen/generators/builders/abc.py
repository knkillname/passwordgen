"""Abstract base class for password generator builders.

Classes
-------
GeneratorBuilder
    Abstract base class for password generator builders.
"""

import abc


class GeneratorBuilder(metaclass=abc.ABCMeta):
    """Abstract base class for password generator builders."""

    @abc.abstractmethod
    def create_generator(self):
        """Create a password generator."""
        raise NotImplementedError
