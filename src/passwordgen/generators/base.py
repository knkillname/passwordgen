"""Base classes for password generators.

This module contains the base classes for password generators. None of
which should be used directly. Instead, the classes in the
passwordgen.generators package should be used.

Classes
-------
IPasswordGenerator
    Interface for password generators.
PasswordGenerator
    Base class for password generators.
"""
import abc
from collections.abc import Iterable

from ..containers import Password


class IPasswordGenerator(metaclass=abc.ABCMeta):
    """Interface for password generators.

    This class is an interface for password generators. It defines
    the methods that must be implemented by all password generators.

    Attributes
    ----------
    name : str
        Name of the password generator.
    description : str
        Description of the password generator.

    Methods
    -------
    generate(length: int) -> Password
        Generate a password of the given length.
    generate_many(length: int, count: int) -> Iterable[Password]
        Generate multiple passwords of the given length.
    """

    @property
    @abc.abstractmethod
    def name(self):
        """Name of the password generator."""

    @property
    @abc.abstractmethod
    def description(self):
        """Description of the password generator."""

    @abc.abstractmethod
    def generate(self, length: int) -> Password:
        """Generate a password of the given length.

        Parameters
        ----------
        length : int
            The length of the password to generate.

        Returns
        -------
        Password
            The generated password.
        """

    @abc.abstractmethod
    def generate_many(self, length: int, count: int) -> Iterable[Password]:
        """Generate multiple passwords of the given length.

        Parameters
        ----------
        length : int
            The length of the passwords to generate.
        count : int
            The number of passwords to generate.

        Returns
        -------
        Iterable[Password]
            The generated passwords.
        """


class BasePasswordGenerator(IPasswordGenerator):
    """Base class for password generators.

    This class is a base class for password generators. It implements
    some of the methods that are common to all password generators.
    """

    @property
    def name(self):
        """Name of the password generator."""
        return self._name

    @property
    def description(self):
        """Description of the password generator."""
        return self._description

    def generate_many(self, length: int, count: int) -> Iterable[Password]:
        """Generate multiple passwords of the given length.

        Parameters
        ----------
        length : int
            The length of the passwords to generate.
        count : int
            The number of passwords to generate.

        Returns
        -------
        Iterable[Password]
            The generated passwords.
        """
        for _ in range(count):
            yield self.generate(length)
