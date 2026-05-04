"""Unit tests for random words generator."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from secure_passwords.config.schema import WordlistsConfig
from secure_passwords.generators.words import RandomWordsGenerator, WordsConfig
from secure_passwords.wordlists import WordlistLoader


class TestWordsGenerator(unittest.TestCase):
    """Validate passphrase generation behavior."""

    def setUp(self) -> None:
        self.loader = WordlistLoader()
        self.config = WordlistsConfig(paths={})
        self.generator = RandomWordsGenerator(self.loader, self.config)

    def test_generates_expected_word_count(self) -> None:
        """Generated passphrase contains configured amount of words."""

        cfg = WordsConfig(word_count=4, separator="-", language="en")
        password = self.generator.generate(cfg)
        self.assertEqual(len(password.split("-")), 4)

    def test_external_wordlist_is_used(self) -> None:
        """External file path overrides embedded list."""

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "custom.txt"
            path.write_text("uno\ndos\ntres\n", encoding="utf-8")
            self.generator.set_wordlists_config(
                WordlistsConfig(paths={"es": str(path)})
            )

            cfg = WordsConfig(word_count=3, separator="_", language="es")
            password = self.generator.generate(cfg)
            self.assertTrue(set(password.split("_")).issubset({"uno", "dos", "tres"}))

    def test_invalid_word_count_raises(self) -> None:
        """word_count must be >= 2."""

        cfg = WordsConfig(word_count=1, separator="-", language="en")
        with self.assertRaises(ValueError):
            self.generator.generate(cfg)
