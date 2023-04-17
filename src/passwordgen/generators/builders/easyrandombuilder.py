import string
from pathlib import Path
from typing import Optional, TypedDict
from .abc import PasswordGeneratorBuilder
from ..easyrandom import EasyRandomPasswordGenerator
from ...common.util import get_resource_path

_DEFAULT_DATA_DIR = get_resource_path("wordlists")


class EasyRandomBuilder(PasswordGeneratorBuilder):
    # FIXME: Docstring is incorrect.
    """Build an EasyRandomPasswordGenerator.

    Methods
    -------
    build()
        Build the password generator.
    with_length(length)
        Set the length of the passwords to generate.
    add_words_from_file(file_name)
        Add words from a file to the dictionary.
    add_words_from_string(words)
        Add words from a string to the dictionary.
    add_words_from_list(words)
        Add words from a list to the dictionary.
    add_filler_chars_from_string(chars)
        Add filler characters from a string to the filler character list.
    add_filler_chars_from_list(chars)
        Add filler characters from a list to the filler character list.
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
        self._filler_chars: Optional[list[str]] = None
        self._data_dir = Path(data_dir)
        if not self._data_dir.is_dir():
            raise FileNotFoundError(f"Data directory does not exist: {data_dir}")

    def with_length(self, length: int) -> "EasyRandomBuilder":
        """Set the length of the passwords to generate."""
        if not isinstance(length, int):
            raise TypeError(f"Expected int, got {type(length)}")
        self._length = length
        return self

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
        self._dictionary.extend(
            stripped for line in lines if (stripped := line.strip())
        )
        return self

    def with_filler_chars(self, chars: str) -> "EasyRandomBuilder":
        """Set the characters to use as filler.

        Parameters
        ----------
        chars : str
            The characters to use as filler.
        """
        if not isinstance(chars, str):
            raise TypeError(f"Expected str, got {type(chars)}")
        self._filler_chars = list(chars)
        return self

    def with_default_filler_chars(self) -> "EasyRandomBuilder":
        """Use the default filler characters."""
        self._filler_chars = None
        return self

    def with_punctuation_filler_chars(self) -> "EasyRandomBuilder":
        """Add punctuation characters to the filler characters."""
        if self._filler_chars is None:
            self._filler_chars = list(string.punctuation)
        else:
            self._filler_chars.extend(string.punctuation)
        return self

    def with_digits_filler_chars(self) -> "EasyRandomBuilder":
        """Add digits to the filler characters."""
        if self._filler_chars is None:
            self._filler_chars = list(string.digits)
        else:
            self._filler_chars.extend(string.digits)
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
