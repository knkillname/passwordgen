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

        Arguments
        ---------
        strength : int, optional
            The strength of the password measured in bits consumed by
            the random number generator to create it. The default is 42.
            If given, it must be non-negative.
        length : int, optional
            The length of the password. The default is None. If given,
            it must be non-negative.

        Returns
        -------
        str
            The generated password.

        Raises
        ------
        TypeError
            If strength or length is not an int.
        ValueError
            If both strength and length are given, or if the given
            value is negative.
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
        TypeError
            If count, strength or length is not an int.
        ValueError
            If both strength and length are given or if the given
            value is negative.
        """
        if not isinstance(count, int):
            raise TypeError(f"Expected int, got {type(count)}")

        kwargs = {}
        if strength is not None:
            kwargs["strength"] = strength
        if length is not None:
            kwargs["length"] = length
        return [self.generate_password(**kwargs) for _ in range(count)]
