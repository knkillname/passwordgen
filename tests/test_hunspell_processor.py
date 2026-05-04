"""Unit tests for Hunspell dictionary processor."""

from __future__ import annotations

import unittest

from secure_passwords.wordlists.downloader import HunspellProcessor


class TestHunspellProcessor(unittest.TestCase):
    """Validate extraction of words from `.dic` content."""

    def setUp(self) -> None:
        self.processor = HunspellProcessor()

    def test_process_extracts_and_normalizes_words(self) -> None:
        """Processor should remove affix codes and normalize case."""

        raw = "5\nCasa/AB\nperro\nniNo/XY\nA1\nzz\n"
        words = self.processor.process(raw)
        self.assertEqual(words, ["casa", "nino", "perro"])

    def test_process_filters_invalid_tokens(self) -> None:
        """Words outside length and character constraints are discarded."""

        raw = "4\naa\nabcdefghijkl\nhi!\nvalida\n"
        words = self.processor.process(raw)
        self.assertEqual(words, ["valida"])
