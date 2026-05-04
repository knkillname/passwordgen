"""Wordlist loading utilities with external-file overrides."""

from __future__ import annotations

from functools import cache
from importlib.resources import files
from pathlib import Path
from typing import Final

from secure_passwords.config.schema import WordlistsConfig

_EMBEDDED_MAP: Final[dict[str, str]] = {
    "en": "eff_large.txt",
    "es": "spanish.txt",
}


def available_dictionary_keys(config: WordlistsConfig) -> list[str]:
    """Return selectable dictionary keys for UI controls.

    Parameters
    ----------
    config : WordlistsConfig
        External path mapping.

    Returns
    -------
    list[str]
        Sorted language keys available from embedded and external dictionaries.
    """

    keys = set(_EMBEDDED_MAP.keys())
    keys.update(
        key.strip()
        for key, value in config.paths.items()
        if key.strip() and isinstance(value, str) and value.strip()
    )
    return sorted(keys)


class WordlistLoader:
    """Load words from configured paths or embedded package resources."""

    def load(self, language: str, config: WordlistsConfig) -> list[str]:
        """Load wordlist for language.

        Parameters
        ----------
        language : str
            Language key.
        config : WordlistsConfig
            External path mapping.

        Returns
        -------
        list[str]
            Loaded words.
        """

        external_path = config.paths.get(language, "")
        if external_path:
            path = Path(external_path)
            if path.exists() and path.is_file():
                return self._read_path(path)

        filename = _EMBEDDED_MAP.get(language, "")
        if not filename:
            return []

        resource = files("secure_passwords.wordlists").joinpath(filename)
        return self._read_text(resource.read_text(encoding="utf-8"))

    def clear_cache(self) -> None:
        """Clear read cache to force reload from disk/resources."""

        self._read_path.cache_clear()

    @staticmethod
    def _read_text(raw: str) -> list[str]:
        """Normalize line-delimited wordlist text.

        Parameters
        ----------
        raw : str
            Raw source text.

        Returns
        -------
        list[str]
            Normalized words.
        """

        words: list[str] = []
        for line in raw.splitlines():
            token = line.strip().lower()
            if not token:
                continue
            words.append(token)
        return words

    @staticmethod
    @cache
    def _read_path(path: Path) -> list[str]:
        """Read and cache words from a file path.

        Parameters
        ----------
        path : Path
            Source text file path.

        Returns
        -------
        list[str]
            Parsed words.
        """

        try:
            raw = path.read_text(encoding="utf-8")
        except OSError:
            return []
        return WordlistLoader._read_text(raw)
