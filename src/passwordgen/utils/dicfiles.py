"""Module for dictionary files.

Dictionary files are used by the password generator to generate
passwords that are more secure. They contain a list of words in plain
text. The words are separated by newlines.

Classes
-------
DictionaryFileBase
    Base class for dictionary files.
HunspellDicFile
    A Hunspell dictionary file.
"""
import abc
import json
from pathlib import Path
from urllib import request

__all__ = ["DictionaryFileBase", "HunspellDicFile"]


class DictionaryFileBase(metaclass=abc.ABCMeta):
    """Base class for dictionary files.

    A dictionary file is a list of words in plain text. The words are
    separated by newlines.
    """

    @property
    @abc.abstractmethod
    def file_name(self) -> str:
        """The file name of the dictionary file."""

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
    def read_words(self) -> list[str]:
        """Read all the words from the dictionary file.

        Returns
        -------
        list[str]
            A list of words from the dictionary file.
        """


class HunspellDicFile:
    """A Hunspell dictionary file.

    Hunspell dictionary files are used by the password generator to
    generate passwords that are more secure.

    Properties
    ----------
    file_name : str
        The file name of the dictionary file.
    language_name : str
        The name of the language of the dictionary file.
    language_code : str
        The language code of the dictionary file.
    encoding : str
        The encoding of the dictionary file.
    url : str | None
        The download URL of the dictionary file.

    Methods
    -------
    download(download_dir: str | Path, overwrite: bool = False)
        Download the dictionary file to the given directory.
    extract_word(line: str) -> str | None
        Extract a word from a line of the dictionary file.
    read_words() -> list[str]
        Read the words from the dictionary file.
    """

    def __init__(
        self,
        file_name: str,
        language_name: str,
        language_code: str,
        encoding: str = "utf8",
        url: str | None = None,
    ):
        """Initialize a Hunspell dictionary file.

        Hunspell dictionary files are used by the password generator to
        generate passwords that are more secure.

        Parameters
        ----------
        file_name : str
            The file name of the dictionary file.
        language_name : str
            The name of the language of the dictionary file.
        language_code : str
            The language code of the dictionary file.
        encoding : str, optional
            The encoding of the dictionary file, by default "utf8"
        url : str | None, optional
            The download URL of the dictionary file, by default None
        """
        self.file_name = file_name
        self.language_name = language_name
        self.language_code = language_code
        self.encoding = encoding
        self.url = url

    # Properties:
    @property
    def file_name(self) -> str:
        """The file name of the dictionary file."""
        return self._file_name

    @file_name.setter
    def file_name(self, file_name: str):
        if not isinstance(file_name, str):
            raise TypeError(f"Expected str, got {type(file_name)}")
        if not file_name.endswith(".dic"):
            raise ValueError(f"Expected file name to end with .dic, got {file_name}")
        self._file_name = file_name

    @property
    def language_name(self) -> str:
        """The name of the language of the dictionary file."""
        return self._language_name

    @language_name.setter
    def language_name(self, language_name: str):
        if not isinstance(language_name, str):
            raise TypeError(f"Expected str, got {type(language_name)}")
        self._language_name = language_name

    @property
    def language_code(self) -> str:
        """The language code of the dictionary file."""
        return self._language_code

    @language_code.setter
    def language_code(self, language_code: str):
        if not isinstance(language_code, str):
            raise TypeError(f"Expected str, got {type(language_code)}")
        self._language_code = language_code

    @property
    def encoding(self) -> str:
        """The encoding of the dictionary file."""
        return self._encoding

    @encoding.setter
    def encoding(self, encoding: str):
        if not isinstance(encoding, str):
            raise TypeError(f"Expected str, got {type(encoding)}")
        self._encoding = encoding

    @property
    def url(self) -> str | None:
        """The download URL of the dictionary file."""
        return self._url

    @url.setter
    def url(self, url: str | None):
        if url is not None and not isinstance(url, str):
            raise TypeError(f"Expected str, got {type(url)}")
        self._url = url

    # Methods:

    def download(self, download_dir: str | Path, overwrite: bool = False):
        """Download the dictionary file.

        Attempts to download the dictionary file to the specified
        directory. If the file already exists, an error is raised unless
        the user specifies that the file should be overwritten.

        Parameters
        ----------
        download_dir : str | Path
            The directory to download the file to.
        overwrite : bool, optional
            Whether to overwrite the file if it already exists, by
            default False.

        Raises
        ------
        ValueError
            If no download URL is specified.
        TypeError
            If the download URL or path is not a string.
        FileExistsError
            If the file already exists and the user does not want to
            overwrite it.
        """
        # Check download URL and types:
        if self.url is None:
            raise ValueError("No download URL specified")
        if not isinstance(self.url, str):
            raise TypeError(f"Expected str, got {type(self.url)}")
        if not isinstance(download_dir, (str, Path)):
            raise TypeError(f"Expected str or Path, got {type(download_dir)}")

        # Check if the download directory is a directory:
        download_dir = Path(download_dir)
        download_dir.mkdir(parents=True, exist_ok=True)
        if not download_dir.is_dir():
            raise NotADirectoryError(f"Not a directory: {download_dir}")

        # Check if the file already exists:
        file_path = download_dir / self.file_name
        if file_path and not overwrite:
            raise FileExistsError(f"File already exists: {file_path}")

        # Otherwise, download the file:
        request.urlretrieve(self.url, file_path)

    def extract_word(self, line: str) -> str:
        """Extract the word from a line in the dictionary file.

        Overload this method to implement custom word extraction.
        """
        return line.strip().split("/", maxsplit=1)[0]

    def read_words(self, dictionaries_dir: str | Path) -> list[str]:
        """Read the words from the dictionary file.

        Parameters
        ----------
        dictionaries_dir : str | Path
            The directory to read the dictionary file from.

        Returns
        -------
        list[str]
            The words from the dictionary file.

        Raises
        ------
        FileNotFoundError
            If the dictionary file does not exist.
        """
        # Check the dictionary file exists:
        file_path = Path(dictionaries_dir) / self.file_name
        if not file_path.is_file():
            raise FileNotFoundError(f"Dictionary file not found: {file_path}")

        # Read the words from the file:
        with file_path.open("r", encoding=self.encoding) as file:
            return [self.extract_word(line) for line in file]

    def __repr__(self) -> str:
        """Return the representation of the dictionary file."""
        return (
            f"{self.__class__.__name__}("
            f"file_name={self.file_name!r}, "
            f"language_name={self.language_name!r}, "
            f"language_code={self.language_code!r}, "
            f"download_url={self.url!r})"
        )


class HunspellDictionariesManager:
    """A manager for Hunspell dictionaries.

    This class manages Hunspell dictionaries, allowing the user to
    download and read words from the dictionaries.

    Parameters
    ----------
    dictionaries_dir : str | Path
        The directory containing the dictionary files.
    definitions_file : str | Path
        The file containing the definitions of the dictionary files.

    Attributes
    ----------
    dictionaries_dir : str | Path
        The directory containing the dictionary files.
    definitions_file : str | Path
        The file containing the definitions of the dictionary files.
    """

    def __init__(self, dictionaries_dir: str | Path, definitions_file: str | Path):
        """Initialise the Hunspell dictionaries manager.

        Parameters
        ----------
        dictionaries_dir : str | Path
            The directory containing the dictionary files.
        definitions_file : str | Path
            The file containing the definitions of the dictionary files.

        Raises
        ------
        TypeError
            If the dictionaries directory or definitions file is not a
            string or path.
        """
        if not isinstance(dictionaries_dir, (str, Path)):
            raise TypeError(f"Expected str or Path, got {type(dictionaries_dir)}")
        if not isinstance(definitions_file, (str, Path)):
            raise TypeError(f"Expected str or Path, got {type(definitions_file)}")
        self.dictionaries_dir = dictionaries_dir
        self._definitions_file = definitions_file
        self._definitions: dict[str, dict[str, str]] = {}

        self._load_definitions()

    # Properties:
    @property
    def dictionaries_dir(self) -> str | Path:
        """The directory containing the dictionary files."""
        return self._dictionaries_dir

    @dictionaries_dir.setter
    def dictionaries_dir(self, dictionaries_dir: str | Path):
        if not isinstance(dictionaries_dir, (str, Path)):
            raise TypeError(f"Expected str or Path, got {type(dictionaries_dir)}")
        self._dictionaries_dir = dictionaries_dir

    @property
    def definitions_file(self) -> str | Path:
        """The definitions file."""
        return self._definitions_file

    def _load_definitions(self):
        """Load the definitions from the definitions file."""
        with open(self.definitions_file, "r") as file:
            definitions_obj = json.load(file)
        self._definitions = {
            record["language_code"]: record
            for record in definitions_obj["dictionaries"]
        }

    def _load_dictionary(self, language_code: str) -> HunspellDicFile:
        """Load a dictionary file from the definitions file.

        Parameters
        ----------
        language_code : str
            The language code of the dictionary file to load.

        Returns
        -------
        HunspellDicFile
            The dictionary file.

        Raises
        ------
        KeyError
            If the language code is not found in the definitions file.
        """
        if language_code not in self._definitions:
            raise KeyError(f"Language code not found: {language_code}")
        return HunspellDicFile(**self._definitions[language_code])

    def load_words(self, language_code: str) -> list[str]:
        """Load the words from the dictionary file.

        Parameters
        ----------
        language_code : str
            The language code of the dictionary file to load.

        Returns
        -------
        list[str]
            The words from the dictionary file.

        Raises
        ------
        KeyError
            If the language code is not found in the definitions file.
        FileNotFoundError
            If the dictionary file does not exist.
        """
        return self._load_dictionary(language_code).read_words(self._dictionaries_dir)
