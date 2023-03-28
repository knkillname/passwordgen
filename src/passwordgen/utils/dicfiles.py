from urllib import request


class DicFile:
    def __init__(
        self,
        file_name: str,
        language_name: str,
        language_code: str,
        encoding: str = "utf8",
        download_url: str | None = None,
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
        download_url : str | None, optional
            The download URL of the dictionary file, by default None
        """
        self.file_name = file_name
        self.language_name = language_name
        self.language_code = language_code
        self.encoding = encoding
        self.download_url = download_url

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
    def download_url(self) -> str | None:
        """The download URL of the dictionary file."""
        return self._download_url

    @download_url.setter
    def download_url(self, download_url: str | None):
        if download_url is not None and not isinstance(download_url, str):
            raise TypeError(f"Expected str, got {type(download_url)}")
        self._download_url = download_url

    # Methods:

    def download(self, path: str):
        """Download the dictionary file.

        Parameters
        ----------
        path : str
            The path to download the dictionary file to.
        """
        if self.download_url is None:
            raise ValueError("No download URL specified")
        request.urlretrieve(self.download_url, path)

    def __repr__(self) -> str:
        """Return the representation of the dictionary file."""
        return (
            f"{self.__class__.__name__}("
            f"file_name={self.file_name!r}, "
            f"language_name={self.language_name!r}, "
            f"language_code={self.language_code!r}, "
            f"download_url={self.download_url!r})"
        )
