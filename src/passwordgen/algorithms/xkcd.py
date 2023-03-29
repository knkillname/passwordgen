"""XKCD password generator.

This module contains the XKCD password generator.
The generator is described in the XKCD web comic 936:
https://xkcd.com/936/

Classes
-------
XKCDGenerator
    Generates passwords by combining words from a predefined list.
"""
import math
from random import SystemRandom

from .abc import PasswordGeneratorBase


class XKCDGenerator(PasswordGeneratorBase):
    """Generates passwords by combining words from a predefined list.

    The XKCD method generates easy to remember passwords by combining
    words from a predefined list. The words are selected in a random
    order and the first letter of each word is capitalized.
    The method is described in the XKCD web comic 936:
    https://xkcd.com/936/

    Attributes
    ----------
    word_list : list[str]
        The list of words used to generate passwords.

    Methods
    -------
    generate_password(strength: int) -> str
        Generate a password of the given strength.
    generate_many_passwords(strength: int, count: int) -> list[str]
        Generate a list of passwords of the given strength.
    """

    def __init__(self, word_list: list[str]) -> None:
        """Initialize the XKCD password generator.

        Parameters
        ----------
        word_list : list[str]
            A list of words to use when generating passwords.
        """
        self._word_list = word_list
        self._random = SystemRandom()

    @property
    def word_list(self) -> list[str]:
        """The list of words used to generate passwords."""
        return self._word_list

    @word_list.setter
    def word_list(self, word_list: list[str]) -> None:
        """Set the list of words used to generate passwords.

        Parameters
        ----------
        word_list : list[str]
            A list of words to use when generating passwords.
        """
        if not isinstance(word_list, list):
            raise TypeError(f"Expected list, got {type(word_list)}")
        if not all(isinstance(word, str) for word in word_list):
            raise TypeError(f"Expected list of str, got {type(word_list[0])}")
        self._word_list = word_list

    def generate_password(self, strength: int) -> str:
        """Generate a password of the given strength.

        Parameters
        ----------
        strength : int
            The strength of the password measured in bits consumed by
            the random number generator to create it.

        Returns
        -------
        str
            A password of the given strength.
        """
        if not isinstance(strength, int):
            raise TypeError(f"Expected int, got {type(strength)}")
        if strength < 0:
            raise ValueError(f"Expected strength to be positive, got {strength}")
        if strength == 0:
            return ""

        entropy_per_word = math.log2(len(self.word_list))
        word_count = math.ceil(strength / entropy_per_word)
        words = self._random.sample(self.word_list, word_count)
        return "".join(word.capitalize() for word in words)
