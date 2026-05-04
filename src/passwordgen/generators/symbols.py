"""Symbol-based password generator."""

from __future__ import annotations

import secrets
import string
from dataclasses import dataclass

from passwordgen.generators.base import PasswordConfig, PasswordGenerator


@dataclass(slots=True)
class SymbolsConfig:
    """Configuration for symbol-based generation.

    Attributes
    ----------
    length : int
        Output password length.
    use_upper : bool
        Include uppercase letters.
    use_digits : bool
        Include digits.
    use_punctuation : bool
        Include punctuation symbols.
    custom_charset : str
        Optional custom set replacing all generated groups.
    """

    length: int
    use_upper: bool
    use_digits: bool
    use_punctuation: bool
    custom_charset: str = ""


class RandomSymbolsGenerator(PasswordGenerator):
    """Generate cryptographically secure random-symbol passwords."""

    @property
    def name(self) -> str:
        """Return algorithm display name.

        Returns
        -------
        str
            Display name for this algorithm.
        """

        return "Simbolos aleatorios"

    def generate(self, config: PasswordConfig) -> str:
        """Generate one password from the selected character set.

        Parameters
        ----------
        config : PasswordConfig
            Expected to be `SymbolsConfig`.

        Returns
        -------
        str
            Generated password.

        Raises
        ------
        ValueError
            If no valid characters are available.
        TypeError
            If config type is invalid.
        """

        if not isinstance(config, SymbolsConfig):
            raise TypeError("Expected SymbolsConfig")

        charset = self._build_charset(config)
        if config.length < 4:
            raise ValueError("Length must be at least 4")

        return "".join(secrets.choice(charset) for _ in range(config.length))

    @staticmethod
    def _build_charset(config: SymbolsConfig) -> str:
        """Build effective character set.

        Parameters
        ----------
        config : SymbolsConfig
            Generator configuration.

        Returns
        -------
        str
            Character set used for random selection.
        """

        if config.custom_charset:
            return "".join(dict.fromkeys(config.custom_charset))

        parts = [string.ascii_lowercase]
        if config.use_upper:
            parts.append(string.ascii_uppercase)
        if config.use_digits:
            parts.append(string.digits)
        if config.use_punctuation:
            parts.append("!@#$%^&*()_+-=[]{}|;:,.<>?")
        return "".join(parts)
