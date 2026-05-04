"""Unit tests for config manager."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from secure_passwords.config.manager import ConfigManager


class TestConfigManager(unittest.TestCase):
    """Validate JSON loading/merging behavior."""

    def test_missing_file_returns_defaults(self) -> None:
        """No file should return in-memory defaults."""

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "cfg.json"
            manager = ConfigManager(path)
            config = manager.load()
            self.assertEqual(config.symbols.length, 20)
            self.assertEqual(config.words.language, "en")

    def test_partial_json_merges_with_defaults(self) -> None:
        """Partial values should override only specified fields."""

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "cfg.json"
            payload = {
                "symbols": {"length": 33},
                "words": {"language": "es"},
            }
            path.write_text(json.dumps(payload), encoding="utf-8")
            manager = ConfigManager(path)
            config = manager.load()

            self.assertEqual(config.symbols.length, 33)
            self.assertEqual(config.words.language, "es")
            self.assertEqual(config.words.word_count, 4)

    def test_save_persists_only_overrides(self) -> None:
        """Serialized JSON should omit default-equal fields."""

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "cfg.json"
            manager = ConfigManager(path)
            config = manager.load()
            config.batch_size = 8
            manager.save(config)

            loaded = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(loaded, {"batch_size": 8})
