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
    count : int
        The number of words to use.

    Methods
    -------
    generate_password()
        Generate a password.
    generate_many_passwords(count)
        Generate many passwords.
    """

    name = "XKCD method"
    description = "Select random words from a list."

    def __init__(self, word_list: Sequence[str], count: int = 4) -> None:
        """Initialize the password generator.

        Parameters
        ----------
        word_list : Sequence[str]
            The list of words to use.
        count : int, optional
            The number of words to use, by default 4
        """
        self.word_list = word_list
        self.count = count

    @property
    def word_list(self) -> Sequence[str]:
        """The list of words to use."""
        return self._word_list

    @word_list.setter
    def word_list(self, value: Sequence[str]) -> None:
        if not isinstance(value, Sequence):
            raise TypeError(f"Expected a sequence, got {type(value)}")
        if not value:
            raise ValueError("Expected a non-empty sequence")
        if not all(isinstance(word, str) for word in value):
            raise ValueError("Expected a sequence of strings")
        self._word_list = value

    @property
    def count(self) -> int:
        """The number of words to use."""
        return self._count

    @count.setter
    def count(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"Expected int, got {type(value)}")
        if value < 0:
            raise ValueError(f"Expected non-negative int, got {value}")
        self._count = value

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
        entropy_per_word = math.log2(len(self.word_list))
        entropy = entropy_per_word * self.count
        password = " ".join(random.choices(self.word_list, k=self.count))
        return Password(password, entropy)
