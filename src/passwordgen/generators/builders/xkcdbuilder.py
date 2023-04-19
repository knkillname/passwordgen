"""A builder for the XKCD password generator.

Classes
-------
XKCDGeneratorBuilder
    A builder for the XKCD password generator.
"""
from pathlib import Path

from ..xkcd import XKCDPasswordGenerator
from .abc import DictionaryBuilderBase


class XKCDGeneratorBuilder(DictionaryBuilderBase):
    """A builder for the XKCD password generator.

    This builder allows you to create an XKCD password generator with
    a custom dictionary and settings. It has the same attributes and
    methods as the DictionaryBuilderBase class, but it also has the
    following:

    Methods
    -------
    with_word_count(count: int) -> XKCDGeneratorBuilder
        Set the number of words to use.
    with_separator(separator: str) -> XKCDGeneratorBuilder
        Set the separator to use between words.
    build() -> XKCDPasswordGenerator
        Build the generator.
    reset() -> None
        Reset the builder to its default state.
    """

    def __init__(self, data_dir: str | Path | None = None):
        """Initialize the factory.

        Parameters
        ----------
        data_dir : Path, optional
            The directory containing the word lists, by default the
            wordlists directory in the package data.

        Raises
        ------
        FileNotFoundError
            If the data directory does not exist.
        """
        super().__init__(data_dir)
        self._word_count: int
        self._separator: str
        self.reset()

    def with_word_count(self, word_count: int) -> "XKCDGeneratorBuilder":
        """Set the number of words to generate.

        Parameters
        ----------
        count : int
            The number of words to generate.
        """
        self._word_count = word_count
        return self

    def with_separator(self, separator: str) -> "XKCDGeneratorBuilder":
        """Set the separator to use between words.

        Parameters
        ----------
        separator : str
            The separator to use between words.
        """
        self._separator = separator
        return self

    def build(self) -> XKCDPasswordGenerator:
        """Create a password generator.

        Returns
        -------
        XKCDPasswordGenerator
            The password generator.
        """
        return XKCDPasswordGenerator(
            dictionary=self.get_dictionary(),
            word_count=self._word_count,
            separator=self._separator,
        )

    def reset(self) -> None:
        """Reset the builder to its default state."""
        super().reset()
        self._word_count = 4
        self._separator = " "
