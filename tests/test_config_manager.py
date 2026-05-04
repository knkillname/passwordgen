"""Unit tests for config manager."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from passwordgen.config.manager import ConfigManager


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

    def test_config_path_property(self) -> None:
        """config_path returns the path supplied at construction."""

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "cfg.json"
            manager = ConfigManager(path)
            self.assertEqual(manager.config_path, path)

    def test_reset_deletes_file_and_returns_defaults(self) -> None:
        """reset() removes persisted config and returns factory defaults."""

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "cfg.json"
            path.write_text('{"batch_size": 8}', encoding="utf-8")
            manager = ConfigManager(path)
            config = manager.reset()
            self.assertFalse(path.exists())
            self.assertEqual(config.batch_size, 5)

    def test_invalid_json_returns_defaults(self) -> None:
        """Malformed JSON falls back to default configuration."""

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "cfg.json"
            path.write_text("not valid json", encoding="utf-8")
            manager = ConfigManager(path)
            config = manager.load()
            self.assertEqual(config.symbols.length, 20)

    def test_non_dict_json_returns_defaults(self) -> None:
        """JSON array instead of object falls back to default configuration."""

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "cfg.json"
            path.write_text("[1, 2, 3]", encoding="utf-8")
            manager = ConfigManager(path)
            config = manager.load()
            self.assertEqual(config.symbols.length, 20)

    def test_xdg_config_home_env_is_respected(self) -> None:
        """XDG_CONFIG_HOME env var changes the default config path."""

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {"XDG_CONFIG_HOME": tmpdir}):
                default_path = ConfigManager.default_config_path()
                self.assertTrue(str(default_path).startswith(tmpdir))

    def test_save_nested_symbols_override(self) -> None:
        """Nested dict override (symbols.length) is persisted correctly."""

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "cfg.json"
            manager = ConfigManager(path)
            config = manager.load()
            config = replace(config, symbols=replace(config.symbols, length=32))
            manager.save(config)
            loaded = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(loaded, {"symbols": {"length": 32}})

    def test_wordlist_paths_loaded_from_json(self) -> None:
        """External wordlist paths in JSON are read into config."""

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "cfg.json"
            payload = {"wordlists": {"paths": {"es": "/path/to/es.txt"}}}
            path.write_text(json.dumps(payload), encoding="utf-8")
            manager = ConfigManager(path)
            config = manager.load()
            self.assertEqual(config.wordlists.paths.get("es"), "/path/to/es.txt")
