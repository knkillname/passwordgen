"""Unit tests for random words generator."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from passwordgen.config.schema import WordlistsConfig
from passwordgen.generators.words import RandomWordsGenerator, WordsConfig
from passwordgen.wordlists import WordlistLoader


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

    def test_name_property(self) -> None:
        """name returns the algorithm display name."""

        self.assertEqual(self.generator.name, "Palabras aleatorias")

    def test_wrong_config_type_raises(self) -> None:
        """Passing wrong config type raises TypeError."""

        with self.assertRaises(TypeError):
            self.generator.generate(object())  # type: ignore[arg-type]

    def test_unknown_language_raises(self) -> None:
        """Unknown language key with no words raises ValueError."""

        cfg = WordsConfig(word_count=2, separator="-", language="xx")
        with self.assertRaises(ValueError):
            self.generator.generate(cfg)
