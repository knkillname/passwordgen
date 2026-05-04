"""Alternating words-and-symbols password generator."""

from __future__ import annotations

import secrets
import string
from dataclasses import dataclass

from passwordgen.config.schema import WordlistsConfig
from passwordgen.generators.base import PasswordConfig, PasswordGenerator
from passwordgen.wordlists import WordlistLoader


@dataclass(slots=True)
class AlternatingConfig:
    """Configuration for alternating generation.

    Attributes
    ----------
    word_count : int
        Number of words in final password.
    symbols_per_group : int
        Number of symbols inserted between adjacent words.
    language : str
        Language key used for source dictionary.
    use_digits : bool
        Include digits in symbol groups.
    """

    word_count: int
    symbols_per_group: int
    language: str
    use_digits: bool


class AlternatingGenerator(PasswordGenerator):
    """Generate passwords alternating words and random symbol chunks."""

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

        return "Palabras alternadas"

    def set_wordlists_config(self, config: WordlistsConfig) -> None:
        """Update wordlist path mapping.

        Parameters
        ----------
        config : WordlistsConfig
            New mapping of language to source path.
        """

        self._wordlists_config = config

    def generate(self, config: PasswordConfig) -> str:
        """Generate one alternating password.

        Parameters
        ----------
        config : PasswordConfig
            Expected to be `AlternatingConfig`.

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

        if not isinstance(config, AlternatingConfig):
            raise TypeError("Expected AlternatingConfig")
        if config.word_count < 2:
            raise ValueError("word_count must be >= 2")
        if config.symbols_per_group < 1:
            raise ValueError("symbols_per_group must be >= 1")

        words = self._loader.load(config.language, self._wordlists_config)
        if not words:
            raise ValueError("No words available for selected language")

        selected_words = [
            self._randomize_first_letter(secrets.choice(words))
            for _ in range(config.word_count)
        ]
        groups = [
            self._random_symbol_group(config.symbols_per_group, config.use_digits)
            for _ in range(config.word_count - 1)
        ]

        chunks: list[str] = [selected_words[0]]
        for group, word in zip(groups, selected_words[1:], strict=True):
            chunks.append(group)
            chunks.append(word)
        return "".join(chunks)

    @staticmethod
    def _random_symbol_group(length: int, use_digits: bool) -> str:
        """Generate a random symbol chunk.

        Parameters
        ----------
        length : int
            Target group length.
        use_digits : bool
            Include digits in group symbols.

        Returns
        -------
        str
            Generated symbol group.
        """

        charset = "!@#$%^&*?" + (string.digits if use_digits else "")
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
            Word with optional first-letter capitalization.
        """

        if not word:
            return word
        if secrets.randbelow(2) == 0:
            return word
        return word[0].upper() + word[1:]
