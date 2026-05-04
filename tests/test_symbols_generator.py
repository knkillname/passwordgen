"""Unit tests for symbol generator."""

from __future__ import annotations

import unittest

from passwordgen.generators.symbols import RandomSymbolsGenerator, SymbolsConfig


class TestSymbolsGenerator(unittest.TestCase):
    """Validate random symbols generator behavior."""

    def setUp(self) -> None:
        self.generator = RandomSymbolsGenerator()

    def test_generates_expected_length(self) -> None:
        """Generated password has configured length."""

        config = SymbolsConfig(
            length=24,
            use_upper=True,
            use_digits=True,
            use_punctuation=True,
        )
        password = self.generator.generate(config)
        self.assertEqual(len(password), 24)

    def test_uses_custom_charset(self) -> None:
        """Generator limits output to custom charset if provided."""

        config = SymbolsConfig(
            length=32,
            use_upper=False,
            use_digits=False,
            use_punctuation=False,
            custom_charset="ab",
        )
        password = self.generator.generate(config)
        self.assertTrue(set(password).issubset({"a", "b"}))

    def test_invalid_short_length_raises(self) -> None:
        """Length lower than 4 is rejected."""

        config = SymbolsConfig(
            length=3,
            use_upper=True,
            use_digits=True,
            use_punctuation=True,
        )
        with self.assertRaises(ValueError):
            self.generator.generate(config)

    def test_name_property(self) -> None:
        """name returns the algorithm display name."""

        self.assertEqual(self.generator.name, "Simbolos aleatorios")

    def test_wrong_config_type_raises(self) -> None:
        """Passing wrong config type raises TypeError."""

        with self.assertRaises(TypeError):
            self.generator.generate(object())  # type: ignore[arg-type]

    def test_lowercase_only_charset(self) -> None:
        """All flags off and no custom charset produces lowercase-only output."""

        config = SymbolsConfig(
            length=16,
            use_upper=False,
            use_digits=False,
            use_punctuation=False,
        )
        password = self.generator.generate(config)
        self.assertTrue(all(c.islower() for c in password))
