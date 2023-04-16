"""A builder for the XKCD password generator.

Classes
-------
XKCDGeneratorBuilder
    A builder for the XKCD password generator.
"""
from collections.abc import Sequence
from pathlib import Path

from ...common import util
from ..xkcd import XKCDPasswordGenerator
from .abc import GeneratorBuilder

_WORD_LISTS_DIR = util.get_resource_path("wordlists")


class XKCDGeneratorBuilder(GeneratorBuilder):
    """A builder for the XKCD password generator.

    This builder allows you to create an XKCD password generator with
    a custom word list and custom settings.

    Properties
    ----------
    data_dir : Path
        The directory containing the word lists.

    Methods
    -------
    get_available_word_lists_files() -> Sequence[str]
        Get the available word list files.
    clear_word_list() -> None
        Clear the word list.
    add_words_from_list(word_list: Sequence[str]) -> None
        Add words to the word list.
    add_words_from_file(path: str | Path) -> None
        Add words from a file to the word list.
    with_count(count: int) -> None
        Set the number of words to use.
    with_separator(separator: str) -> None
        Set the separator to use between words.
    create_generator() -> XKCDPasswordGenerator
        Create the generator.
    """

    def __init__(self, data_dir: str | Path = _WORD_LISTS_DIR):
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
        if isinstance(data_dir, str):
            data_dir = Path(data_dir)
        if not isinstance(data_dir, Path):
            raise TypeError(f"Expected a Path, got {type(data_dir)}")
        if not data_dir.exists() and not data_dir.is_dir():
            raise FileNotFoundError(f"Directory {data_dir} does not exist")
        self._data_dir = data_dir
        self._word_list: list[str] = []
        self._count = 4
        self._separator = " "

    @property
    def data_dir(self) -> Path:
        """Get the data directory.

        Returns
        -------
        Path
            The data directory.
        """
        return self._data_dir

    def get_available_word_lists_files(self) -> Sequence[str]:
        """Get the available word list files.

        Returns
        -------
        Sequence[str]
            The list of available word list files.
        """
        return [f.stem for f in self._data_dir.glob("*.txt")]

    def clear_word_list(self) -> None:
        """Clear the word list."""
        self._word_list = []

    def add_words_from_list(self, word_list: Sequence[str]) -> None:
        """Add words to the word list.

        Parameters
        ----------
        word_list : Sequence[str]
            The list of words to add.

        Raises
        ------
        TypeError
            If the word list is not a sequence, or if the word list is
            not a sequence of strings.
        """
        if not isinstance(word_list, Sequence):
            raise TypeError(f"Expected a sequence, got {type(word_list)}")
        if not all(isinstance(w, str) for w in word_list):
            raise TypeError("Expected a sequence of strings")
        self._word_list.extend(word_list)
        self._remove_duplicates()

    def _remove_duplicates(self) -> None:
        """Remove duplicate words from the word list."""
        self._word_list = list(dict.fromkeys(self._word_list))

    def add_words_from_file(self, path: str | Path) -> None:
        """Add words from a file to the word list.

        Parameters
        ----------
        path : str | Path
            The path to the file. If the path is a string, it is
            converted to a Path. If the path is a Path, it is used
            directly. If the path is a relative path, it is assumed to
            be relative to the data directory. If the path is a
            relative path with no extension, the extension .txt is
            appended.

        Raises
        ------
        TypeError
            If the path is not a string or a Path.
        FileNotFoundError
            If the file does not exist.
        """
        if isinstance(path, str):
            path = Path(path)
        if not isinstance(path, Path):
            raise TypeError(f"Expected str or path, got {type(path)}")
        if not path.exists() and not path.is_absolute() and len(path.parts) == 1:
            path = self._data_dir / path.with_suffix(".txt").name
        with path.open("rt", encoding="utf-8") as file:
            lines = file.readlines()
        words = [stripped for line in lines if (stripped := line.strip())]
        self.add_words_from_list(words)

    def with_count(self, word_count: int) -> None:
        """Set the number of words to generate.

        Parameters
        ----------
        count : int
            The number of words to generate.
        """
        self._count = word_count

    def with_separator(self, separator: str) -> None:
        """Set the separator to use between words.

        Parameters
        ----------
        separator : str
            The separator to use between words.
        """
        self._separator = separator

    def create_generator(self):
        """Create a password generator.

        Returns
        -------
        XKCDPasswordGenerator
            The password generator.
        """
        return XKCDPasswordGenerator(
            word_list=self._word_list, count=self._count, separator=self._separator
        )
