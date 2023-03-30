"""Abstract base classes for dictionary files and dictionary shelves.

A dictionary file is a list of words in plain text. The words are
separated by newlines. A dictionary shelf is a collection of dictionary
files.

Classes
-------
DictionaryFileBase
    Base class for dictionary files.
DictionaryShelfBase
    Base class for dictionary shelves.
"""
import abc
from pathlib import Path
from typing import Sequence, TypedDict


class DictionaryFileDict(TypedDict):
    """Parameters for a dictionary file.

    Parameters
    ----------
    file_path : str
        The path of the dictionary file.
    language_name : str
        The name of the language of the dictionary file.
    language_code : str
        The language code of the dictionary file.
    encoding : str
        The encoding of the dictionary file.
    url : str | None
        The download URL of the dictionary file.
    """

    file_path: str
    language_name: str
    language_code: str
    encoding: str
    url: str | None


class DictionaryShelfDict(TypedDict):
    """Parameters for a dictionary shelf.

    A dictionary shelf is a collection of dictionary files.

    Parameters
    ----------
    dictionaries : list[DictionaryFileDict]
        A list of dictionary files.
    """

    dictionaries: list[DictionaryFileDict]


class DictionaryFileBase(metaclass=abc.ABCMeta):
    """Base class for dictionary files.

    A dictionary file is a list of words in plain text. The words are
    separated by newlines.
    """

    @property
    @abc.abstractmethod
    def file_path(self) -> Path:
        """The path of the dictionary file."""

    @property
    @abc.abstractmethod
    def language_name(self) -> str:
        """The name of the language of the dictionary file."""

    @property
    @abc.abstractmethod
    def language_code(self) -> str:
        """The language code of the dictionary file."""

    @property
    @abc.abstractmethod
    def encoding(self) -> str:
        """The encoding of the dictionary file."""

    @property
    @abc.abstractmethod
    def url(self) -> str | None:
        """The download URL of the dictionary file."""

    @abc.abstractmethod
    def extract_word(self, line: str) -> str | None:
        """Extract a word from a line of the dictionary file.

        Implementations of this method should extract a word from a
        line of the dictionary file. The word should be returned as a
        string. If the line does not contain a word, None should be
        returned.

        Parameters
        ----------
        line : str
            A line of the dictionary file.

        Returns
        -------
        str | None
            The word extracted from the line, or None if the line does
            not contain a word.
        """

    @abc.abstractmethod
    def load_words(self) -> list[str]:
        """Load all the words from the dictionary file.

        Returns
        -------
        list[str]
            A list of words from the dictionary file.
        """

    @abc.abstractmethod
    def download(self, overwrite: bool = False) -> None:
        """Download the dictionary file.

        Parameters
        ----------
        overwrite : bool, optional
            Whether to overwrite the dictionary file if it is already
            present, by default False.

        Raises
        ------
        DownloadError
            If the dictionary file could not be downloaded.
        FileExistsError
            If the dictionary file is already present and overwrite is
            False.
        """


class DictionaryShelfBase(metaclass=abc.ABCMeta):
    """Base class for dictionary shelves.

    A dictionary shelf is a collection of dictionary files.

    Attributes
    ----------
    shelf_directory : Path
        The directory of the dictionary shelf. All dictionaries will be
        downloaded to and read from this directory.
    dictionaries : Sequence[DictionaryFileBase]
        A sequence of dictionary files in the dictionary shelf.

    Methods
    -------
    get_dictionary(language_code)
        Get a dictionary file from the dictionary shelf.
    from_json(json_path)
        Create a dictionary shelf from a JSON file.
    to_json(json_path, overwrite=False)
        Save the dictionary shelf to a JSON file.
    load_words(language_code, download=True)
        Load all the words from a dictionary file.
    """

    @property
    @abc.abstractmethod
    def shelf_directory(self) -> Path:
        """The directory of the dictionary shelf."""

    @property
    @abc.abstractmethod
    def dictionaries(self) -> Sequence[DictionaryFileBase]:
        """A sequence of dictionary files in the dictionary shelf."""

    @abc.abstractmethod
    def get_dictionary(self, language_code: str) -> DictionaryFileBase:
        """Get a dictionary file from the dictionary shelf.

        Parameters
        ----------
        language_code : str
            The language code of the dictionary file.

        Returns
        -------
        DictionaryFileBase
            The dictionary file with the given language code.

        Raises
        ------
        KeyError
            If the dictionary shelf does not contain a dictionary file
            with the given language code.
        """

    @classmethod
    @abc.abstractmethod
    def from_json(
        cls, json_path: str | Path, shelf_directory: Path
    ) -> "DictionaryShelfBase":
        """Create a dictionary shelf from a JSON file.

        Parameters
        ----------
        json_path : str | Path
            The path of the JSON file.
        shelf_directory : Path
            The directory of the dictionary shelf.

        Returns
        -------
        DictionaryShelfBase
            The dictionary shelf created from the JSON file.

        Raises
        ------
        FileNotFoundError
            If the JSON file could not be found.
        ValueError
            If the JSON file could not be parsed.
        """

    @abc.abstractmethod
    def to_json(self, json_path: str | Path, overwrite=False) -> None:
        """Save the dictionary shelf to a JSON file.

        Parameters
        ----------
        json_path : str | Path
            The path of the JSON file.
        overwrite : bool, optional
            Whether to overwrite the JSON file if it is already
            present, by default False.

        Raises
        ------
        FileExistsError
            If the JSON file is already present and overwrite is False.
        """

    @abc.abstractmethod
    def load_words(self, language_code: str, download: bool = True) -> list[str]:
        """Load all the words from a dictionary file.

        Parameters
        ----------
        language_code : str
            The language code of the dictionary file.
        download : bool, optional
            Whether to download the dictionary file if it is not
            already present, by default True.

        Returns
        -------
        list[str]
            A list of words from the dictionary file.

        Raises
        ------
        KeyError
            If the dictionary shelf does not contain a dictionary file
            with the given language code.
        DownloadError
            If the dictionary file could not be downloaded.
        ValueError
            If no url is specified for the dictionary file.
        """
