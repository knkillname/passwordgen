"""Bracketed-word password generator.

Generates passwords with the pattern
``word1 + symbols + opener + word2 + closer``.

Examples
--------
``chamaco1528(Padalustro)``
``Trolebús98%5{Guijarro}``
"""

from __future__ import annotations

import secrets
import string
from dataclasses import dataclass

from passwordgen.config.schema import WordlistsConfig
from passwordgen.generators.base import PasswordConfig, PasswordGenerator
from passwordgen.wordlists import WordlistLoader

#: Bracket pairs randomly selected for each generated password.
#: Includes traditional paired symbols and self-paired delimiters.
_BRACKET_PAIRS: list[tuple[str, str]] = [
    ("(", ")"),
    ("[", "]"),
    ("{", "}"),
    ("<", ">"),
    ("¿", "?"),
    ("¡", "!"),
    # Self-paired symbols.
    ("$", "$"),
    ("#", "#"),
    ("@", "@"),
    ("%", "%"),
    ("&", "&"),
    ("*", "*"),
    ("+", "+"),
    ("=", "="),
    ("~", "~"),
    ("|", "|"),
    ("/", "/"),
    ("\\", "\\"),
    ("^", "^"),
]


@dataclass(slots=True)
class BracketedConfig:
    """Configuration for bracketed generation.

    Attributes
    ----------
    symbols_between : int
        Number of symbols inserted between first word and opening bracket.
    language : str
        Language key used for source dictionary.
    use_digits : bool
        Include digits in the symbol group.
    use_punctuation : bool
        Include punctuation in the symbol group.
    """

    symbols_between: int
    language: str
    use_digits: bool
    use_punctuation: bool


class BracketedGenerator(PasswordGenerator):
    """Generate passwords with a word, symbols, and a bracketed word."""

    def __init__(
        self, loader: WordlistLoader, wordlists_config: WordlistsConfig
    ) -> None:
        self._loader = loader
        self._wordlists_config = wordlists_config

    @property
    def name(self) -> str:
        """Return algorithm display name.

        Returns
        -------
        str
            Display name for this algorithm.
        """

        return "Paréntesis"

    def set_wordlists_config(self, config: WordlistsConfig) -> None:
        """Update wordlist path mapping.

        Parameters
        ----------
        config : WordlistsConfig
            New mapping of language to source path.
        """

        self._wordlists_config = config

    def generate(self, config: PasswordConfig) -> str:
        """Generate one bracketed password.

        Parameters
        ----------
        config : PasswordConfig
            Expected to be `BracketedConfig`.

        Returns
        -------
        str
            Generated password.

        Raises
        ------
        ValueError
            If configuration is invalid.
        TypeError
            If config type is invalid.
        """

        if not isinstance(config, BracketedConfig):
            raise TypeError("Expected BracketedConfig")
        if config.symbols_between < 1:
            raise ValueError("symbols_between must be >= 1")
        if not config.use_digits and not config.use_punctuation:
            raise ValueError(
                "At least one of use_digits or use_punctuation must be enabled"
            )

        words = self._loader.load(config.language, self._wordlists_config)
        if not words:
            raise ValueError("No words available for selected language")

        word1 = self._randomize_first_letter(secrets.choice(words))
        word2 = self._randomize_first_letter(secrets.choice(words))
        symbols = self._random_symbol_group(
            config.symbols_between, config.use_digits, config.use_punctuation
        )
        opener, closer = secrets.choice(_BRACKET_PAIRS)
        return f"{word1}{symbols}{opener}{word2}{closer}"

    @staticmethod
    def _random_symbol_group(
        length: int, use_digits: bool, use_punctuation: bool
    ) -> str:
        """Generate a random symbol chunk.

        Parameters
        ----------
        length : int
            Target group length.
        use_digits : bool
            Include digits in group symbols.
        use_punctuation : bool
            Include punctuation in group symbols.

        Returns
        -------
        str
            Generated symbol group.
        """

        charset = ""
        if use_digits:
            charset += string.digits
        if use_punctuation:
            charset += "!@#$%^&*?"
        return "".join(secrets.choice(charset) for _ in range(length))

    @staticmethod
    def _randomize_first_letter(word: str) -> str:
        """Randomly capitalize first letter of a word.

        Parameters
        ----------
        word : str
            Input word.

        Returns
        -------
        str
            Word with first letter randomly capitalized.
        """

        if not word:
            return word
        first = word[0].upper() if secrets.randbelow(2) else word[0].lower()
        return first + word[1:]
