"""Module for the XKCDPasswordGenerator class.

Classes
-------
XKCDPasswordGenerator
    Select random words from a list.
"""
import math
import random
from pathlib import Path
from typing import Sequence

from ..common.classes import Password
from .abc import PasswordGeneratorBase


class XKCDPasswordGenerator(PasswordGeneratorBase):
    """Select random words from a list.

    Attributes
    ----------
    name : str
        The name of the password generator.
    description : str
        The description of the password generator.
    word_list : Sequence[str]
        The list of words to use.
    word_count : int
        The number of words to use.
    separator: str
        The separator to use between words.

    Methods
    -------
    generate_password()
        Generate a password.
    generate_many_passwords(count)
        Generate many passwords.
    """

    name = "XKCD method"
    description = "Select random words from a list."

    def __init__(
        self, dictionary: Sequence[str], word_count: int = 4, separator: str = " "
    ) -> None:
        """Initialize the password generator.

        Parameters
        ----------
        word_list : Sequence[str]
            The list of words to use.
        word_count : int, optional
            The number of words to use, by default 4
        separator : str, optional
            The separator to use between words, by default " "
        """
        self.dictionary = dictionary
        self.word_count = word_count
        self.separator = separator

    @property
    def dictionary(self) -> Sequence[str]:
        """The list of words to use."""
        return self._dictionary

    @dictionary.setter
    def dictionary(self, value: Sequence[str]) -> None:
        if not isinstance(value, Sequence):
            raise TypeError(f"Expected a sequence, got {type(value)}")
        if not value:
            raise ValueError("Expected a non-empty sequence")
        if not all(isinstance(word, str) for word in value):
            raise TypeError("Expected a sequence of strings")
        self._dictionary = value

    @property
    def word_count(self) -> int:
        """The number of words to use."""
        return self._count

    @word_count.setter
    def word_count(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"Expected int, got {type(value)}")
        if value < 0:
            raise ValueError(f"Expected non-negative int, got {value}")
        self._count = value

    @property
    def separator(self) -> str:
        """The separator to use between words."""
        return self._separator

    @separator.setter
    def separator(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"Expected str, got {type(value)}")
        self._separator = value

    @classmethod
    def from_word_list_file(cls, path: Path | str) -> "XKCDPasswordGenerator":
        """Read a word list from a file.

        Parameters
        ----------
        path : Path | str
            The path to the file.
        """
        if isinstance(path, str):
            path = Path(path)
        elif not isinstance(path, Path):
            raise TypeError(f"Expected Path or str, got {type(path)}")
        with path.open("rt", encoding="utf-8") as file:
            lines = file.readlines()
        word_list = [word for line in lines if (word := line.strip())]
        return cls(word_list)

    def generate_password(self) -> Password:
        """Generate a password.

        Returns
        -------
        Password
            A password and its strength.
        """
        entropy_per_word = math.log2(len(self.dictionary))
        entropy = entropy_per_word * self.word_count
        password = self.separator.join(
            random.choices(self.dictionary, k=self.word_count)
        )
        return Password(password, entropy)
