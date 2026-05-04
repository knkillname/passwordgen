"""Unit tests for alternating generator."""

from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from passwordgen.config.schema import WordlistsConfig
from passwordgen.generators.alternating import (
    AlternatingConfig,
    AlternatingGenerator,
)
from passwordgen.wordlists import WordlistLoader


class TestAlternatingGenerator(unittest.TestCase):
    """Validate alternating generator structure."""

    def setUp(self) -> None:
        self.generator = AlternatingGenerator(
            WordlistLoader(), WordlistsConfig(paths={})
        )

    def test_output_contains_symbol_groups(self) -> None:
        """Generated output includes inserted symbol groups."""

        cfg = AlternatingConfig(
            word_count=3,
            symbols_per_group=2,
            language="en",
            use_digits=False,
        )
        password = self.generator.generate(cfg)
        punctuation = set("!@#$%^&*?")
        punct_count = sum(1 for ch in password if ch in punctuation)
        self.assertEqual(punct_count, 4)

    def test_invalid_group_length_raises(self) -> None:
        """symbols_per_group must be >= 1."""

        cfg = AlternatingConfig(
            word_count=3,
            symbols_per_group=0,
            language="en",
            use_digits=True,
        )
        with self.assertRaises(ValueError):
            self.generator.generate(cfg)

    def test_name_property(self) -> None:
        """name returns the algorithm display name."""

        self.assertEqual(self.generator.name, "Palabras alternadas")

    def test_wrong_config_type_raises(self) -> None:
        """Passing wrong config type raises TypeError."""

        with self.assertRaises(TypeError):
            self.generator.generate(object())  # type: ignore[arg-type]

    def test_invalid_word_count_raises(self) -> None:
        """word_count must be >= 2."""

        cfg = AlternatingConfig(
            word_count=1,
            symbols_per_group=1,
            language="en",
            use_digits=False,
        )
        with self.assertRaises(ValueError):
            self.generator.generate(cfg)

    def test_unknown_language_raises(self) -> None:
        """Unknown language key with no words raises ValueError."""

        cfg = AlternatingConfig(
            word_count=2,
            symbols_per_group=1,
            language="xx",
            use_digits=False,
        )
        with self.assertRaises(ValueError):
            self.generator.generate(cfg)

    def test_random_capitalization_is_applied_per_word(self) -> None:
        """Alternating output randomizes first-letter capitalization."""

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "custom.txt"
            path.write_text("hola\n", encoding="utf-8")
            self.generator.set_wordlists_config(
                WordlistsConfig(paths={"es": str(path)})
            )

            cfg = AlternatingConfig(
                word_count=3,
                symbols_per_group=1,
                language="es",
                use_digits=False,
            )
            with patch(
                "passwordgen.generators.alternating.secrets.randbelow",
                side_effect=[1, 0, 1],
            ):
                password = self.generator.generate(cfg)

            words = [
                chunk for chunk in re.split(r"[^A-Za-zÀ-ÖØ-öø-ÿ]+", password) if chunk
            ]
            self.assertEqual(words, ["Hola", "hola", "Hola"])
