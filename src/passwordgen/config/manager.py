"""JSON configuration manager for secure password generator."""

from __future__ import annotations

import json
import os
from dataclasses import replace
from pathlib import Path
from typing import Any

from secure_passwords.config.schema import (
    AlternatingDefaults,
    AppConfig,
    SymbolsDefaults,
    WordlistsConfig,
    WordsDefaults,
)

_SYMBOL_KEYS = (
    "length",
    "use_upper",
    "use_digits",
    "use_punctuation",
    "custom_charset",
)
_WORD_KEYS = ("word_count", "separator", "language")
_ALT_KEYS = ("word_count", "symbols_per_group", "language", "use_digits")


class ConfigManager:
    """Load and persist runtime configuration overrides.

    Parameters
    ----------
    config_path : Path | None, optional
        Custom path to the JSON file. If omitted, the manager resolves to
        XDG config location (`$XDG_CONFIG_HOME/secure_passwords/config.json`) or
        `~/.config/secure_passwords/config.json`.
    """

    def __init__(self, config_path: Path | None = None) -> None:
        self._config_path = config_path or self.default_config_path()

    @staticmethod
    def default_config_path() -> Path:
        """Return the default JSON config path.

        Returns
        -------
        Path
            Absolute path for the configuration file.
        """

        base_dir = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
        return base_dir / "secure_passwords" / "config.json"

    @property
    def config_path(self) -> Path:
        """Return the manager target path.

        Returns
        -------
        Path
            Path where JSON overrides are persisted.
        """

        return self._config_path

    def load(self) -> AppConfig:
        """Load configuration and merge it with defaults.

        Returns
        -------
        AppConfig
            Fully-populated configuration object.
        """

        defaults = AppConfig()
        if not self._config_path.exists():
            return defaults

        raw = self._read_json_file(self._config_path)
        return self._merge(defaults, raw)

    def save(self, config: AppConfig) -> None:
        """Persist only override values to JSON.

        Parameters
        ----------
        config : AppConfig
            Effective configuration to be persisted.
        """

        defaults = AppConfig().to_dict()
        merged = config.to_dict()
        payload = self._diff(merged, defaults)

        self._config_path.parent.mkdir(parents=True, exist_ok=True)
        self._config_path.write_text(
            json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def reset(self) -> AppConfig:
        """Delete persisted overrides and return defaults.

        Returns
        -------
        AppConfig
            Default configuration after reset.
        """

        if self._config_path.exists():
            self._config_path.unlink()
        return AppConfig()

    @staticmethod
    def _read_json_file(path: Path) -> dict[str, Any]:
        """Read JSON object from disk.

        Parameters
        ----------
        path : Path
            Path to JSON file.

        Returns
        -------
        dict[str, Any]
            Parsed object; invalid JSON returns empty mapping.
        """

        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
        except OSError, json.JSONDecodeError:
            return {}
        if isinstance(loaded, dict):
            return loaded
        return {}

    def _merge(self, defaults: AppConfig, raw: dict[str, Any]) -> AppConfig:
        """Merge raw partial JSON data into defaults.

        Parameters
        ----------
        defaults : AppConfig
            Default values.
        raw : dict[str, Any]
            JSON overrides loaded from file.

        Returns
        -------
        AppConfig
            Effective configuration.
        """

        symbols_raw = self._section(raw, "symbols")
        words_raw = self._section(raw, "words")
        alternating_raw = self._section(raw, "alternating")

        symbols = replace(defaults.symbols, **self._pick(symbols_raw, _SYMBOL_KEYS))
        words = replace(defaults.words, **self._pick(words_raw, _WORD_KEYS))
        alternating = replace(
            defaults.alternating,
            **self._pick(alternating_raw, _ALT_KEYS),
        )

        paths = self._wordlist_paths(raw)
        theme = raw.get("theme", defaults.theme)
        batch_size = raw.get("batch_size", defaults.batch_size)

        return AppConfig(
            symbols=SymbolsDefaults(
                length=max(4, int(symbols.length)),
                use_upper=bool(symbols.use_upper),
                use_digits=bool(symbols.use_digits),
                use_punctuation=bool(symbols.use_punctuation),
                custom_charset=str(symbols.custom_charset),
            ),
            words=WordsDefaults(
                word_count=max(2, int(words.word_count)),
                separator=str(words.separator),
                language=str(words.language),
            ),
            alternating=AlternatingDefaults(
                word_count=max(2, int(alternating.word_count)),
                symbols_per_group=max(1, int(alternating.symbols_per_group)),
                language=str(alternating.language),
                use_digits=bool(alternating.use_digits),
            ),
            wordlists=WordlistsConfig(paths=paths),
            theme=str(theme),
            batch_size=max(1, int(batch_size)),
            crack_attempts_per_second=max(
                1,
                int(
                    raw.get(
                        "crack_attempts_per_second", defaults.crack_attempts_per_second
                    )
                ),
            ),
        )

    @staticmethod
    def _section(raw: dict[str, Any], key: str) -> dict[str, Any]:
        """Return a nested section if it is a dictionary.

        Parameters
        ----------
        raw : dict[str, Any]
            Raw configuration mapping.
        key : str
            Section key.

        Returns
        -------
        dict[str, Any]
            Section mapping or empty dict if not present.
        """

        value = raw.get(key, {})
        return value if isinstance(value, dict) else {}

    @staticmethod
    def _pick(source: dict[str, Any], keys: tuple[str, ...]) -> dict[str, Any]:
        """Pick only allowed keys from source mapping.

        Parameters
        ----------
        source : dict[str, Any]
            Source mapping.
        keys : tuple[str, ...]
            Accepted key names.

        Returns
        -------
        dict[str, Any]
            Filtered mapping.
        """

        return {key: source[key] for key in keys if key in source}

    def _wordlist_paths(self, raw: dict[str, Any]) -> dict[str, str]:
        """Extract validated wordlist path overrides.

        Parameters
        ----------
        raw : dict[str, Any]
            Raw configuration mapping.

        Returns
        -------
        dict[str, str]
            Valid language-path pairs.
        """

        wordlists_raw = self._section(raw, "wordlists")
        paths_raw = wordlists_raw.get("paths", {})
        if not isinstance(paths_raw, dict):
            return {}

        output: dict[str, str] = {}
        for key, value in paths_raw.items():
            if isinstance(key, str) and isinstance(value, str):
                output[key] = value
        return output

    @staticmethod
    def _diff(current: dict[str, Any], defaults: dict[str, Any]) -> dict[str, Any]:
        """Compute a recursive override-only diff.

        Parameters
        ----------
        current : dict[str, Any]
            Current values.
        defaults : dict[str, Any]
            Default values.

        Returns
        -------
        dict[str, Any]
            Mapping with only values that differ from defaults.
        """

        output: dict[str, Any] = {}
        for key, value in current.items():
            if key not in defaults:
                output[key] = value
                continue

            default_value = defaults[key]
            if isinstance(value, dict) and isinstance(default_value, dict):
                nested = ConfigManager._diff(value, default_value)
                if nested:
                    output[key] = nested
            elif value != default_value:
                output[key] = value

        return output
