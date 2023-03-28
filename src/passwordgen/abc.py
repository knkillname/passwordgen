"""Base classes for password generators.

Password generators are used to generate passwords of a given strength.
The strength is measured in bits consumed by the random number generator
to create the password. The length of the password is calculated from
the strength and the algorithm used to generate it.

Classes
-------
PasswordGeneratorBase
    Base class for password generators.
"""
import abc


class PasswordGeneratorBase(metaclass=abc.ABCMeta):
    """Base class for password generators.

    This class is used to define the interface for password generators.}
    It is not intended to be used directly.
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
    def generate_password(self, strength: int) -> str:
        """Generate a password of the given strength.

        Arguments
        ---------
        strength : int
            The strength of the password measured in bits consumed by
            the random number generator to create it.
        """

    def generate_many_passwords(self, strength: int, count: int) -> list[str]:
        """Generate a list of passwords of the given strength.

        Arguments
        ---------
        strength : int
            The strength of the password measured in bits consumed by
            the random number generator to create each.
        count : int
            The number of passwords to generate.
        """
        return [self.generate_password(strength) for _ in range(count)]
