"""Configuration schema for secure password generator.

The JSON configuration acts as an override source only. Missing fields are
resolved from defaults defined in this module.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class SymbolsDefaults:
    """Default parameters for symbol-based passwords.

    Attributes
    ----------
    length : int
        Length for generated passwords.
    use_upper : bool
        Whether uppercase letters are allowed.
    use_digits : bool
        Whether digits are allowed.
    use_punctuation : bool
        Whether punctuation symbols are allowed.
    custom_charset : str
        Optional custom character set that replaces built-in groups if not empty.
    """

    length: int = 20
    use_upper: bool = True
    use_digits: bool = True
    use_punctuation: bool = True
    custom_charset: str = ""


@dataclass(slots=True)
class WordsDefaults:
    """Default parameters for random-word passwords.

    Attributes
    ----------
    word_count : int
        Number of words to compose a password.
    separator : str
        Separator placed between words.
    language : str
        Language key for the wordlist.
    """

    word_count: int = 4
    separator: str = "-"
    language: str = "en"


@dataclass(slots=True)
class AlternatingDefaults:
    """Default parameters for alternating word-symbol passwords.

    Attributes
    ----------
    word_count : int
        Number of words in the generated password.
    symbols_per_group : int
        Number of random symbols inserted between each word.
    language : str
        Language key for the wordlist.
    use_digits : bool
        Whether symbol groups can include digits.
    """

    word_count: int = 3
    symbols_per_group: int = 3
    language: str = "en"
    use_digits: bool = True


@dataclass(slots=True)
class WordlistsConfig:
    """Mapping of language keys to custom wordlist files.

    Attributes
    ----------
    paths : dict[str, str]
        Language-to-file-path mapping. Empty values mean fallback to embedded
        package wordlists.
    """

    paths: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class AppConfig:
    """Top-level application configuration.

    Attributes
    ----------
    symbols : SymbolsDefaults
        Defaults for symbol generator parameters.
    words : WordsDefaults
        Defaults for words generator parameters.
    alternating : AlternatingDefaults
        Defaults for alternating generator parameters.
    wordlists : WordlistsConfig
        Wordlist source mapping by language key.
    theme : str
        TTK theme name used by the UI.
    batch_size : int
        Number of passwords generated in one operation.
    crack_attempts_per_second : int
        Assumed attacker speed for crack-time estimation.
    """

    symbols: SymbolsDefaults = field(default_factory=SymbolsDefaults)
    words: WordsDefaults = field(default_factory=WordsDefaults)
    alternating: AlternatingDefaults = field(default_factory=AlternatingDefaults)
    wordlists: WordlistsConfig = field(default_factory=WordlistsConfig)
    theme: str = "clam"
    batch_size: int = 5
    crack_attempts_per_second: int = 1000

    def to_dict(self) -> dict[str, Any]:
        """Serialize configuration into JSON-friendly dictionaries.

        Returns
        -------
        dict[str, Any]
            Serializable mapping that can be dumped as JSON.
        """

        return asdict(self)
