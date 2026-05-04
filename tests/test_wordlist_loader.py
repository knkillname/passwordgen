"""Unit tests for WordlistLoader and available_dictionary_keys."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from passwordgen.config.schema import WordlistsConfig
from passwordgen.wordlists import WordlistLoader, available_dictionary_keys


class TestWordlistLoader(unittest.TestCase):
    """Validate wordlist loading from embedded and external sources."""

    def setUp(self) -> None:
        self.loader = WordlistLoader()
        self.empty_config = WordlistsConfig(paths={})

    def test_embedded_en_loads_words(self) -> None:
        """Embedded English wordlist returns a non-empty list."""

        words = self.loader.load("en", self.empty_config)
        self.assertGreater(len(words), 0)

    def test_unknown_language_returns_empty(self) -> None:
        """Language with no embedded or external source returns empty list."""

        words = self.loader.load("xx", self.empty_config)
        self.assertEqual(words, [])

    def test_external_path_overrides_embedded(self) -> None:
        """Valid external file path is loaded instead of embedded list."""

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "custom.txt"
            path.write_text("alpha\nbeta\ngamma\n", encoding="utf-8")
            config = WordlistsConfig(paths={"en": str(path)})
            words = self.loader.load("en", config)
            self.assertEqual(sorted(words), ["alpha", "beta", "gamma"])

    def test_clear_cache_does_not_raise(self) -> None:
        """clear_cache() runs without errors."""

        self.loader.load("en", self.empty_config)
        self.loader.clear_cache()


class TestAvailableDictionaryKeys(unittest.TestCase):
    """Validate available_dictionary_keys helper."""

    def test_embedded_keys_always_present(self) -> None:
        """Embedded dictionaries en and es are always available."""

        config = WordlistsConfig(paths={})
        keys = available_dictionary_keys(config)
        self.assertIn("en", keys)
        self.assertIn("es", keys)

    def test_external_key_is_included(self) -> None:
        """An external path with a valid key is included in results."""

        config = WordlistsConfig(paths={"fr": "/path/to/fr.txt"})
        keys = available_dictionary_keys(config)
        self.assertIn("fr", keys)
        self.assertIn("en", keys)

    def test_result_is_sorted(self) -> None:
        """Returned keys are in sorted order."""

        config = WordlistsConfig(paths={"zh": "/path.txt"})
        keys = available_dictionary_keys(config)
        self.assertEqual(keys, sorted(keys))
