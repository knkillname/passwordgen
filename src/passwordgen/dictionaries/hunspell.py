"""Hunspell dictionary file and shelf classes.

A Hunspell dictionary file is a list of words in plain text. The words
are separated by newlines. The file may contain extra information
after the word separated by a slash. This class only loads the words
which then can be used to generate passwords.

A Hunspell dictionary shelf is a collection of Hunspell dictionary
files. The shelf can be used to load the words from all the files
which then can be used to generate passwords.

Classes
-------
HunspellDictionary
    A Hunspell dictionary file.
HunspellDictionaryShelf
    A Hunspell dictionary shelf.
"""
import json
import shutil
import tempfile
import warnings
from collections.abc import Sequence
from pathlib import Path
from urllib import request

from .abc import DictionaryFileBase, DictionaryShelfBase, DictionaryShelfDict

__all__ = ["HunspellDictionary", "HunspellDictionaryShelf"]


class HunspellDictionary(DictionaryFileBase):
    """A Hunspell dictionary file.

    Hunspell dictionary files contain a list of words separated by
    newlines with some extra information. This class only loads the
    words which then can be used to generate passwords.

    Parameters
    ----------
    file_path : str | Path
        The path of the dictionary file.
    language_name : str
        The name of the language of the dictionary file.
    language_code : str
        The language code of the dictionary file.
    encoding : str, optional
        The encoding of the dictionary file, by default "utf8"
    url : str | None, optional
        The download URL of the dictionary file, by default None.

    Attributes
    ----------
    file_path : Path
        The file path of the dictionary file.
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
    download(overwrite=False)
        Download the dictionary file.
    extract_word(line)
        Extract the word from a line of the dictionary file. Override
        this method to change the behavior.
    load_words()
        Load the words from the dictionary file.
    """

    def __init__(
        self,
        file_path: str | Path,
        language_name: str,
        language_code: str,
        encoding: str = "utf8",
        url: str | None = None,
    ):
        """Initialize a Hunspell dictionary file.

        Hunspell dictionary files contain a list of words separated by
        newlines with some extra information. This class only loads the
        words which then can be used to generate passwords.

        Parameters
        ----------
        file_path : str | Path
            The path of the dictionary file.
        language_name : str
            The name of the language of the dictionary file.
        language_code : str
            The language code of the dictionary file.
        encoding : str, optional
            The encoding of the dictionary file, by default "utf8"
        url : str | None, optional
            The download URL of the dictionary file, by default None.
        """
        self.file_path = Path(file_path)
        self.language_name = language_name
        self.language_code = language_code
        self.encoding = encoding
        self.url = url

    # Properties:
    @property
    def file_path(self) -> Path:
        """The file path of the dictionary file."""
        return self._file_path

    @file_path.setter
    def file_path(self, file_path: Path):
        if not isinstance(file_path, Path):
            raise TypeError(f"Expected Path, got {type(file_path)}")
        self._file_path = Path(file_path)

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

    def download(self, overwrite: bool = False):
        """Download the dictionary file.

        Attempts to download the dictionary file to the specified
        directory. If the file already exists, an error is raised unless
        the user specifies that the file should be overwritten.

        Parameters
        ----------
        overwrite : bool, optional
            Whether to overwrite the file if it already exists, by
            default False.

        Raises
        ------
        ValueError
            If no download URL is specified.
        FileExistsError
            If the file already exists and overwrite is False.
        """
        # Check download URL and types:
        if self.url is None:
            raise ValueError("No download URL specified")
        if not isinstance(overwrite, bool):
            raise TypeError(f"Expected bool, got {type(overwrite)}")

        # Check if the file already exists:
        if self.file_path.exists() and not overwrite:
            raise FileExistsError(f"File already exists: {self.file_path}")

        # Otherwise, download the file:
        request.urlretrieve(self.url, self.file_path)

    def extract_word(self, line: str) -> str | None:
        """Extract the word from a line in the dictionary file.

        Parameters
        ----------
        line : str
            The line from the dictionary file.
        """
        return line.strip().split("/", maxsplit=1)[0] or None

    def load_words(self) -> list[str]:
        """Load the words from the dictionary file.

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
        if not self.file_path.is_file():
            raise FileNotFoundError(f"Dictionary file not found: {self.file_path}")

        # Read the words from the file:
        with self.file_path.open("r", encoding=self.encoding) as file:
            first_line = file.readline()
            aux = (self.extract_word(line) for line in file)
            result = [word for word in aux if word is not None]

        try:
            expected_len = int(first_line)
        except ValueError:
            raise ValueError(
                f"Expected first line to be an integer, got {first_line!r}"
            )

        if len(result) != int(expected_len):
            warnings.warn(
                f"Expected {expected_len} words in file {self.file_path}, "
                f"got {len(result)}"
            )

        return result

    def __repr__(self) -> str:
        """Return the representation of the dictionary file."""
        return (
            f"{self.__class__.__name__}("
            f"file_name={self.file_path!r}, "
            f"language_name={self.language_name!r}, "
            f"language_code={self.language_code!r}, "
            f"download_url={self.url!r})"
        )


class HunspellDictionaryShelf(DictionaryShelfBase):
    """A shelf of Hunspell dictionaries.

    This class is used to store and manage Hunspell dictionaries. It
    provides methods to load the dictionaries from the shelf, and to
    load the words from the dictionaries.

    Attributes
    ----------
    dictionaries : Sequence[HunspellDictionary]
        The dictionaries in the shelf.
    shelf_directory : Path
        The path of the shelf directory.

    Methods
    -------
    get_dictionary(language_code)
        Get a dictionary from the shelf by language code.
    load_words(language_code)
        Load the words from a dictionary in the shelf.
    from_json(json_file)
        Create a dictionary shelf from a JSON file.
    to_json(json_file)
        Save the dictionary shelf to a JSON file.
    """

    def __init__(
        self,
        dictionaries: Sequence[HunspellDictionary] | None,
        shelf_directory: Path | None,
    ) -> None:
        """Initialize a Hunspell dictionary shelf.

        Parameters
        ----------
        dictionaries : Sequence[HunspellDictionary]
            The dictionaries to add to the shelf.
        shelf_directory : Path
            The path of the shelf file.
        """
        if dictionaries is None:
            dictionaries = []
        self.dictionaries = dictionaries

        self._is_temporary = False
        if shelf_directory is None:
            shelf_directory = Path(tempfile.mkdtemp())
            self._is_temporary = True
        self.shelf_directory = shelf_directory

    def __del__(self):
        """Finalize the dictionary shelf.

        This method is called when the object is about to be destroyed.
        Deletes the shelf directory if it was created by the class.
        """
        if self._is_temporary:
            shutil.rmtree(self.shelf_directory, ignore_errors=True)

    @property
    def dictionaries(self) -> Sequence[HunspellDictionary]:
        """The dictionaries in the shelf."""
        return self._dictionaries

    @dictionaries.setter
    def dictionaries(self, dictionaries: Sequence[HunspellDictionary]):
        if not isinstance(dictionaries, Sequence):
            raise TypeError(f"Expected Sequence, got {type(dictionaries)}")
        if not all(isinstance(d, HunspellDictionary) for d in dictionaries):
            raise TypeError("Expected all elements to be HunspellDictionary")
        self._dictionaries = dictionaries

    @property
    def shelf_directory(self) -> Path:
        """The directory of the shelf file."""
        return self._shelf_directory

    @shelf_directory.setter
    def shelf_directory(self, shelf_directory: Path):
        if not isinstance(shelf_directory, Path):
            raise TypeError(f"Expected Path, got {type(shelf_directory)}")
        self._shelf_directory = shelf_directory

    @classmethod
    def from_json(
        cls, json_path: str | Path, shelf_directory: Path
    ) -> "HunspellDictionaryShelf":
        """Load a Hunspell dictionary shelf from a JSON file.

        Parameters
        ----------
        json_path : str | Path
            The path of the JSON file.
        shelf_directory : Path
            The path of the shelf directory.

        Returns
        -------
        HunspellDictionaryShelf
            The Hunspell dictionary shelf.
        """
        with open(json_path, "r") as file:
            data: DictionaryShelfDict = json.load(file)
        dictionaries = [HunspellDictionary(**d) for d in data["dictionaries"]]
        shelf_directory = Path(shelf_directory)
        return cls(dictionaries, shelf_directory)

    def to_json(self, json_path: str | Path, overwrite: bool = False):
        """Save the Hunspell dictionary shelf to a JSON file.

        Parameters
        ----------
        json_path : str | Path
            The path of the JSON file.
        overwrite : bool, optional
            Whether to overwrite the file if it already exists, by
            default False.

        Raises
        ------
        FileExistsError
            If the file already exists and overwrite is False.
        """
        if not isinstance(json_path, Path):
            json_path = Path(json_path)
        if json_path.exists() and not overwrite:
            raise FileExistsError(f"File already exists: {json_path}")

        data: DictionaryShelfDict = {
            "dictionaries": [
                {
                    "file_path": dic_file.file_path.name,
                    "language_name": dic_file.language_name,
                    "language_code": dic_file.language_code,
                    "encoding": dic_file.encoding,
                    "url": dic_file.url,
                }
                for dic_file in self.dictionaries
            ]
        }
        with open(json_path, "w") as file:
            json.dump(data, file)

    def get_dictionary(self, language_code: str) -> DictionaryFileBase:
        """Get the dictionary file for the specified language code.

        Parameters
        ----------
        language_code : str
            The language code of the dictionary file to get.

        Returns
        -------
        DictionaryFileBase
            The dictionary file for the specified language code.
        """
        for dictionary in self.dictionaries:
            if dictionary.language_code == language_code:
                return dictionary
        raise ValueError(f"No dictionary found for language code {language_code!r}")

    def load_words(self, language_code: str, download: bool = True) -> list[str]:
        """Load the words from a specified dictionary.

        Parameters
        ----------
        language_code : str
            The language code of the dictionary file to load.
        download : bool, optional
            Whether to download the dictionary file if it does not exist,
            by default True.

        Returns
        -------
        list[str]
            The words from the dictionary file.

        Raises
        ------
        ValueError
            If no dictionary file exists for the specified language code.
        """
        dictionary = self.get_dictionary(language_code)
        if not dictionary.file_path.exists():
            if download:
                dictionary.download()
            else:
                raise FileNotFoundError(
                    f"Dictionary file not found: {dictionary.file_path}"
                )
        return dictionary.load_words()
