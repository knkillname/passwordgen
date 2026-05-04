"""Random-word password generator."""

from __future__ import annotations

import secrets
from dataclasses import dataclass

from secure_passwords.config.schema import WordlistsConfig
from secure_passwords.generators.base import PasswordConfig, PasswordGenerator
from secure_passwords.wordlists import WordlistLoader


@dataclass(slots=True)
class WordsConfig:
    """Configuration for word-based generation.

    Attributes
    ----------
    word_count : int
        Number of words to compose in each password.
    separator : str
        Separator between words.
    language : str
        Language key to resolve the source dictionary.
    """

    word_count: int
    separator: str
    language: str


class RandomWordsGenerator(PasswordGenerator):
    """Generate passphrases using random dictionary words."""

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

        return "Palabras aleatorias"

    def set_wordlists_config(self, config: WordlistsConfig) -> None:
        """Update wordlist path mapping.

        Parameters
        ----------
        config : WordlistsConfig
            New mapping of language to source path.
        """

        self._wordlists_config = config

    def generate(self, config: PasswordConfig) -> str:
        """Generate one passphrase.

        Parameters
        ----------
        config : PasswordConfig
            Expected to be `WordsConfig`.

        Returns
        -------
        str
            Generated passphrase.

        Raises
        ------
        ValueError
            If configuration is invalid.
        TypeError
            If config type is invalid.
        """

        if not isinstance(config, WordsConfig):
            raise TypeError("Expected WordsConfig")
        if config.word_count < 2:
            raise ValueError("word_count must be >= 2")

        words = self._loader.load(config.language, self._wordlists_config)
        if not words:
            raise ValueError("No words available for selected language")

        selected = [secrets.choice(words) for _ in range(config.word_count)]
        return config.separator.join(selected)
