"""Unit tests for bracketed generator."""

from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from passwordgen.config.schema import WordlistsConfig
from passwordgen.generators.bracketed import (
    BracketedConfig,
    BracketedGenerator,
)
from passwordgen.wordlists import WordlistLoader

#: Characters that can appear in symbol groups.
_PUNCTUATION = set("!@#$%^&*?")


class TestBracketedGenerator(unittest.TestCase):
    """Validate bracketed generator structure."""

    def setUp(self) -> None:
        self.generator = BracketedGenerator(WordlistLoader(), WordlistsConfig(paths={}))

    def test_name_property(self) -> None:
        """name returns the algorithm display name."""

        self.assertEqual(self.generator.name, "Paréntesis")

    def test_wrong_config_type_raises(self) -> None:
        """Passing wrong config type raises TypeError."""

        with self.assertRaises(TypeError):
            self.generator.generate(object())  # type: ignore[arg-type]

    def test_output_structure_has_two_words_and_symbols(self) -> None:
        """Generated password contains symbols between two words and brackets."""

        cfg = BracketedConfig(
            symbols_between=4,
            language="en",
            use_digits=True,
            use_punctuation=True,
        )
        password = self.generator.generate(cfg)

        # Must contain at least 4 symbols/digits from the between group.
        digit_count = sum(1 for ch in password if ch.isdigit())
        punct_count = sum(1 for ch in password if ch in _PUNCTUATION)
        self.assertGreaterEqual(
            digit_count + punct_count,
            4,
            f"Expected >=4 symbols/digits, got {digit_count + punct_count} "
            f"in '{password}'",
        )

        # Must contain at least two word-like chunks (letters).
        letter_chunks = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+", password)
        self.assertGreaterEqual(
            len(letter_chunks),
            2,
            f"Expected >=2 word chunks in '{password}'",
        )

    def test_output_contains_bracket_pair(self) -> None:
        """Generated password wraps the second word in brackets."""

        cfg = BracketedConfig(
            symbols_between=3,
            language="en",
            use_digits=False,
            use_punctuation=True,
        )
        password = self.generator.generate(cfg)

        # After the symbol group, an opener should appear before a word,
        # then a closer at or near the end.
        # Pattern: word symbols OPENER word CLOSER (end)
        pattern = re.compile(
            r"[A-Za-zÀ-ÖØ-öø-ÿ]+"  # first word
            r"[^A-Za-zÀ-ÖØ-öø-ÿ]+"  # symbols
            r"(.)"  # opener (capture)
            r"[A-Za-zÀ-ÖØ-öø-ÿ]+"  # second word
            r"(.)$"  # closer (capture) at end
        )
        match = pattern.search(password)
        self.assertIsNotNone(
            match, f"Password '{password}' did not match bracketed pattern"
        )

    def test_symbols_between_zero_raises(self) -> None:
        """symbols_between must be >= 1."""

        cfg = BracketedConfig(
            symbols_between=0,
            language="en",
            use_digits=True,
            use_punctuation=False,
        )
        with self.assertRaises(ValueError):
            self.generator.generate(cfg)

    def test_both_flags_false_raises(self) -> None:
        """At least one of use_digits/use_punctuation must be enabled."""

        cfg = BracketedConfig(
            symbols_between=4,
            language="en",
            use_digits=False,
            use_punctuation=False,
        )
        with self.assertRaises(ValueError):
            self.generator.generate(cfg)

    def test_unknown_language_raises(self) -> None:
        """Unknown language key with no words raises ValueError."""

        cfg = BracketedConfig(
            symbols_between=2,
            language="xx",
            use_digits=True,
            use_punctuation=False,
        )
        with self.assertRaises(ValueError):
            self.generator.generate(cfg)

    def test_random_capitalization_is_applied_per_word(self) -> None:
        """Bracketed output randomizes first-letter capitalization."""

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "custom.txt"
            path.write_text("hola\nmundo\n", encoding="utf-8")
            self.generator.set_wordlists_config(
                WordlistsConfig(paths={"es": str(path)})
            )

            cfg = BracketedConfig(
                symbols_between=1,
                language="es",
                use_digits=True,
                use_punctuation=False,
            )
            with patch(
                "passwordgen.generators.bracketed.secrets.randbelow",
                side_effect=[1, 0],
            ):
                password = self.generator.generate(cfg)

            words = [
                chunk for chunk in re.split(r"[^A-Za-zÀ-ÖØ-öø-ÿ]+", password) if chunk
            ]
            self.assertEqual(words, ["Hola", "mundo"])
