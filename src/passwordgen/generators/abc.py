"""Base classes for password generators.

Password generators are used to generate passwords of a given strength
or length. The strength is measured in bits consumed by the random
number generator to create the password.

Classes
-------
PasswordGeneratorBase
    Base class for password generators.
"""
import abc
from collections.abc import Iterable

from ..common.classes import Password


class PasswordGeneratorBase(metaclass=abc.ABCMeta):
    """Base class for password generators.

    Attributes
    ----------
    name : str
        The name of the password generator.
    description : str
        The description of the password generator.

    Methods
    -------
    generate_password()
        Generate a password.
    generate_many_passwords(count)
        Generate many passwords.
    """

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """The name of the password generator."""

    @property
    @abc.abstractmethod
    def description(self) -> str:
        """The description of the password generator."""

    @abc.abstractmethod
    def generate_password(self) -> Password:
        """Generate a password.

        Returns
        -------
        Password
            A password and its strength.
        """

    def generate_many_passwords(self, count: int) -> Iterable[Password]:
        """Generate many passwords.

        Parameters
        ----------
        count : int
            The number of passwords to generate.

        Returns
        -------
        Iterable[Password]
            The passwords and their strength.
        """
        yield from (self.generate_password() for _ in range(count))
