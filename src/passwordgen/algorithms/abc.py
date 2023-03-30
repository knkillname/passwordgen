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

from ..passwords import Password


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
    def generate_password(
        self, *, strength: int | None = None, length: int | None = None
    ) -> Password:
        """Generate a password of the given strength or length.

        If no arguments are given, a password of strength 42 is
        generated.

        Arguments
        ---------
        strength : int, optional
            The strength of the password measured in bits consumed by
            the random number generator to create it. The default is 42.
        length : int, optional
            The length of the password. The default is None.

        Raises
        ------
        ValueError
            If both strength and length are given.
        """

    def generate_many_passwords(
        self,
        count: int = 100,
        *,
        strength: int | None = None,
        length: int | None = None,
    ) -> list[Password]:
        """Generate a list of passwords of the given strength or length.

        Arguments
        ---------
        count : int
            The number of passwords to generate. The default is 100.
        strength : int, optional
            The strength of the passwords measured in bits consumed by
            the random number generator to create them. The default is
            42.
        length : int, optional
            The length of the passwords. The default is None.

        Returns
        -------
        list[str]
            The generated passwords.

        Raises
        ------
        ValueError
            If both strength and length are given.
        """
        kwargs = {}
        if strength is not None:
            kwargs["strength"] = strength
        if length is not None:
            kwargs["length"] = length
        return [self.generate_password(**kwargs) for _ in range(count)]
