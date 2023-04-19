"""EasyRandomBuilder class.

This module contains the EasyRandomBuilder class, which is used to build
EasyRandomPasswordGenerator instances.

Classes
-------
EasyRandomBuilder
    Build an EasyRandomPasswordGenerator.
"""
from collections.abc import Collection, Iterable
from pathlib import Path

from ...common.util import get_resource_path
from ..easyrandom import EasyRandomPasswordGenerator
from .abc import PasswordGeneratorBuilder

_DEFAULT_DATA_DIR = get_resource_path("wordlists")


class EasyRandomBuilder(PasswordGeneratorBuilder):
    """Build an EasyRandomPasswordGenerator.

    Methods
    -------
    build()
        Build the password generator.
    with_length(length)
        Set the length of the passwords to generate.
    add_words_from_file(file_name)
        Add words from a file to the dictionary.
    add_words_from_list(words)
        Add words from a list to the dictionary.
    add_filler_chars(chars)
        Add filler characters from a string to the filler character list.
    reset()
        Reset the builder to its default state.
    """

    def __init__(self, data_dir: str | Path = _DEFAULT_DATA_DIR) -> None:
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
        self._length = 16
        self._dictionary: list[str] = []
        self._filler_chars: list[str] | None = None
        self._data_dir = Path(data_dir)
        if not self._data_dir.is_dir():
            raise FileNotFoundError(f"Data directory does not exist: {data_dir}")

    @property
    def data_dir(self) -> Path:
        """The directory to search for word lists in."""
        return self._data_dir

    def with_length(self, length: int) -> "EasyRandomBuilder":
        """Set the length of the passwords to generate."""
        if not isinstance(length, int):
            raise TypeError(f"Expected int, got {type(length)}")
        self._length = length
        return self

    def get_available_dictionaries(self) -> list[str]:
        """Get a list of the available word lists."""
        return [file.stem for file in self._data_dir.iterdir() if file.suffix == ".txt"]

    def add_words_from_file(self, file_name: str | Path) -> "EasyRandomBuilder":
        """Add words from a file to the dictionary.

        Parameters
        ----------
        file_name : str | Path
            The file to read from. If the file is a relative path and
            no such file exists, it will be searched for in the data
            directory.

        Raises
        ------
        TypeError
            If file_name is not a str or Path.
        FileNotFoundError
            If the file does not exist.
        """
        if isinstance(file_name, str):
            file_name = Path(file_name)
        if not isinstance(file_name, Path):
            raise TypeError("file_name must be a str or Path")
        if not file_name.is_absolute() and not file_name.exists():
            file_name = self._data_dir / file_name.with_suffix(".txt")
        with file_name.open("rt", encoding="utf-8") as file:
            lines = file.readlines()
        self.add_words_from_list(
            stripped for line in lines if (stripped := line.strip())
        )
        return self

    def add_words_from_list(self, words: Iterable[str]) -> "EasyRandomBuilder":
        """Add words from a list to the dictionary.

        Parameters
        ----------
        words : Iterable[str]
            The words to add to the dictionary.

        Raises
        ------
        TypeError
            If words is not an Iterable[str].
        """
        if not isinstance(words, Iterable):
            raise TypeError(f"Expected Iterable[str], got {type(words)}")
        if not isinstance(words, Collection):
            words = list(words)
        if not all(isinstance(word, str) for word in words):
            raise TypeError(f"Expected Iterable[str], got {type(words)}")

        self._dictionary.extend(words)
        # Remove duplicates
        self._dictionary = list(dict.fromkeys(self._dictionary))
        return self

    def add_filler_chars(self, chars: str) -> "EasyRandomBuilder":
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
                length=self._length, dictionary=self._dictionary
            )
        return EasyRandomPasswordGenerator(
            length=self._length,
            dictionary=self._dictionary,
            filler_characters="".join(self._filler_chars),
        )

    def reset(self) -> None:
        """Reset the builder."""
        self._length = 16
        self._dictionary = []
        self._filler_chars = None
