"""EasyRandomPasswordGeneratorBuilder class.

This module contains the EasyRandomBuilder class, which is used to build
EasyRandomPasswordGenerator instances.

Classes
-------
EasyRandomBuilder
    Build an EasyRandomPasswordGenerator.
"""
from pathlib import Path

from ..easyrandom import EasyRandomPasswordGenerator
from .abc import DictionaryPasswordGeneratorBuilderBase


class EasyRandomPasswordGeneratorBuilder(DictionaryPasswordGeneratorBuilderBase):
    """Build an EasyRandomPasswordGenerator.

    This builder allows you to create an EasyRandomPasswordGenerator
    with a custom dictionary and settings. It has the same attributes
    and methods as the DictionaryBuilderBase class, but it also has the
    following:

    Methods
    -------
    build()
        Build the password generator.
    with_length(length)
        Set the length of the passwords to generate.
    add_filler_characters(chars)
        Add filler characters from a string to the filler character list.
    reset()
        Reset the builder to its default state.
    """

    def __init__(self, data_dir: str | Path | None = None) -> None:
        """Initialize the builder.

        Parameters
        ----------
        data_dir : str | Path, optional
            The directory to search for word lists in, by default
            the included word lists directory.

        Raises
        ------
        TypeError
            If data_dir is not a str or Path.
        FileNotFoundError
            If the data directory does not exist.
        """
        super().__init__(data_dir)
        self._length = 16
        self._filler_chars: list[str] | None = None

    def with_length(self, length: int) -> "EasyRandomPasswordGeneratorBuilder":
        """Set the length of the passwords to generate."""
        if not isinstance(length, int):
            raise TypeError(f"Expected int, got {type(length)}")
        self._length = length
        return self

    def add_filler_characters(self, chars: str) -> "EasyRandomPasswordGeneratorBuilder":
        """Add filler characters from a string.

        Parameters
        ----------
        chars : str
            The characters to add to the filler character list.

        Raises
        ------
        TypeError
            If chars is not a str.
        """
        if not isinstance(chars, str):
            raise TypeError(f"Expected str, got {type(chars)}")
        if self._filler_chars is None:
            self._filler_chars = list(chars)
        else:
            self._filler_chars.extend(
                char for char in chars if char not in self._filler_chars
            )
        return self

    def build(self) -> EasyRandomPasswordGenerator:
        """Build the password generator."""
        if self._filler_chars is None:
            return EasyRandomPasswordGenerator(
                length=self._length, dictionary=self.get_dictionary()
            )
        return EasyRandomPasswordGenerator(
            length=self._length,
            dictionary=self.get_dictionary(),
            filler_characters="".join(self._filler_chars),
        )

    def reset(self) -> None:
        """Reset the builder."""
        self._length = 16
        self._filler_chars = None
