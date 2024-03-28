"""Abstract base class for password generator builders.

Classes
-------
GeneratorBuilder
    Abstract base class for password generator builders.
"""

import abc
from pathlib import Path
from typing import Iterable, Self

from passwordgen.common import util

from ...generators.abc import PasswordGeneratorBase

_DEFAULT_DATA_DIR = util.get_resource_path("dictionaries")


class PasswordGeneratorBuilder(metaclass=abc.ABCMeta):
    """Abstract base class for password generator builders."""

    @abc.abstractmethod
    def build(self) -> PasswordGeneratorBase:
        """Create a password generator."""

    @abc.abstractmethod
    def reset(self) -> None:
        """Reset the builder."""


class DictionaryPasswordGeneratorBuilderBase(
    PasswordGeneratorBuilder, metaclass=abc.ABCMeta
):
    """Base class for dictionary-based password generator builders.

    Attributes
    ----------
    data_dir : Path
        The directory to search for dictionaries in.
    Methods
    -------
    parse_word(line)
        Parse a word from a line of text.
    add_words_from_file(path)
        Add words from a file to the dictionary.
    add_words_from_iterable(words, filter_empty=True)
        Add words from an iterable to the dictionary.
    """

    def __init__(self, dictionaries_dir: str | Path | None = None) -> None:
        """Initialize the builder.

        Parameters
        ----------
        dictionaries_dir : str | Path, optional
            The directory to search for dictionaries in, by default
            the included word lists directory.

        Raises
        ------
        TypeError
            If dictionaries_dir is not a str or Path.
        FileNotFoundError
            If the data directory does not exist.
        """
        if dictionaries_dir is None:
            dictionaries_dir = _DEFAULT_DATA_DIR
        self._dictionaries_dir: Path
        self.dictionaries_dir = Path(dictionaries_dir)

        # We use a dict because they preserve the order of insertion of
        # the items whilst avoiding duplicates in an efficient manner.
        self._dictionary: dict[str, None] = {}

    @property
    def dictionaries_dir(self) -> Path:
        """The directory to search for dictionaries in."""
        return self._dictionaries_dir

    @dictionaries_dir.setter
    def dictionaries_dir(self, dictionaries_dir: Path) -> None:
        """Set the directory to search for dictionaries in.

        Parameters
        ----------
        dictionaries_dir : Path
            The directory to search for dictionaries in.

        Raises
        ------
        TypeError
            If dictionaries_dir is not a str or Path.
        FileNotFoundError
            If the data directory does not exist.
        """
        if not isinstance(dictionaries_dir, Path):
            raise TypeError(f"Expected Path, got {type(dictionaries_dir)}")
        if not dictionaries_dir.exists() or not dictionaries_dir.is_dir():
            raise FileNotFoundError(
                f"Data directory does not exist: {dictionaries_dir}"
            )
        self._dictionaries_dir = dictionaries_dir

    def get_available_dictionaries(self) -> list[str]:
        """Get the names of the available dictionaries.

        Returns
        -------
        list[str]
            The names of the available dictionaries.
        """
        return [
            path.stem
            for path in self._dictionaries_dir.iterdir()
            if path.is_file() and path.suffix == ".txt"
        ]

    def get_dictionary(self) -> list[str]:
        """Get the dictionary.

        Returns
        -------
        list[str]
            The dictionary.
        """
        return list(self._dictionary)

    def parse_word(self, line: str) -> str | None:
        """Parse a word from a line of text.

        Override this method to change how words are parsed. By default,
        the line is stripped and if the result is empty, None is
        returned.

        Parameters
        ----------
        line : str
            The line to parse.

        Returns
        -------
        str | None
            The parsed word, or None if the line should be ignored.
        """
        return stripped if (stripped := line.strip()) else None

    def add_words_from_file(
        self, path: str | Path
    ) -> "DictionaryPasswordGeneratorBuilderBase":
        """Add words from a file to the dictionary.

        If the path does not exists and it is a relative path, then
        the path will be searched for in the package data directory.
        Also, if the path contains no extension, ".txt" will be appended
        to the path.

        Parameters
        ----------
        path : str | Path
            The path to the file to add words from.
        Raises
        ------
        FileNotFoundError
            If the file does not exist.
        """
        path = Path(path)
        if not path.exists():
            path = self._dictionaries_dir / path
        if path.suffix == "":
            path = path.with_suffix(".txt")
        if not path.exists():
            raise FileNotFoundError(f"File does not exist: {path}")
        with path.open("rt", encoding="utf-8") as file:
            lines = file.readlines()
        self.add_words_from_iterable(
            (parsed for line in lines if (parsed := self.parse_word(line)) is not None),
            filter_empty=False,
        )
        return self

    def add_words_from_iterable(
        self, words: Iterable[str], filter_empty: bool = True
    ) -> Self:
        """Add words from an iterable to the dictionary.

        Parameters
        ----------
        words : Iterable[str]
            The words to add to the dictionary.
        filter_empty : bool, optional
            Whether to filter out empty strings, by default True.

        Raises
        ------
        TypeError
            If words is not an iterable or if any of the words is not a
            string.
        """
        if not isinstance(words, Iterable):
            raise TypeError(f"Expected Iterable, got {type(words)}")
        if filter_empty:
            words = (word for word in words if word)
        words = list(words)
        for word in words:
            if not isinstance(word, str):
                raise TypeError(f"Expected str, got {type(word)}")
        self._dictionary.update((word, None) for word in words)
        return self

    def reset(self) -> None:
        """Reset the dictionary to its default state."""
        self._dictionary = {}
