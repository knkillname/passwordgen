"""Unit tests for application entry point."""

from __future__ import annotations

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from passwordgen.cli import CommandLineApp
from passwordgen.config.schema import (
    AlternatingDefaults,
    AppConfig,
    SymbolsDefaults,
    WordlistsConfig,
    WordsDefaults,
)


class TestMainEntryPoint(unittest.TestCase):
    """Validate CLI and GUI entry-point behavior."""

    @patch("passwordgen.cli.run_app")
    def test_gui_flag_runs_gui(self, run_app_mock) -> None:
        """--gui should launch GUI and return success."""

        exit_code = CommandLineApp.main("--gui")

        self.assertEqual(exit_code, 0)
        run_app_mock.assert_called_once_with()

    @patch("passwordgen.cli.RandomSymbolsGenerator")
    @patch("passwordgen.cli.ConfigManager")
    def test_cli_mode_prints_passwords(
        self, manager_cls_mock, generator_cls_mock
    ) -> None:
        """Default mode should print generated passwords to stdout."""

        manager = manager_cls_mock.return_value
        manager.load.return_value = AppConfig(
            batch_size=2,
            symbols=SymbolsDefaults(length=8),
        )

        generator = generator_cls_mock.return_value
        generator.generate.side_effect = ["firstpass", "secondpass"]

        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = CommandLineApp.main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(output.getvalue().splitlines(), ["firstpass", "secondpass"])

    @patch("passwordgen.cli.RandomSymbolsGenerator")
    @patch("passwordgen.cli.ConfigManager")
    def test_symbols_subparser_overrides_length_and_count(
        self, manager_cls_mock, generator_cls_mock
    ) -> None:
        """symbols subparser arguments should override defaults."""

        manager = manager_cls_mock.return_value
        manager.load.return_value = AppConfig(
            batch_size=5,
            symbols=SymbolsDefaults(length=20),
        )

        generator = generator_cls_mock.return_value
        generator.generate.return_value = "okpass"

        with redirect_stdout(io.StringIO()):
            exit_code = CommandLineApp.main("symbols", "--count", "3", "--length", "14")

        self.assertEqual(exit_code, 0)
        self.assertEqual(generator.generate.call_count, 3)
        generated_config = generator.generate.call_args_list[0].args[0]
        self.assertEqual(generated_config.length, 14)

    @patch("passwordgen.cli.RandomSymbolsGenerator")
    @patch("passwordgen.cli.ConfigManager")
    def test_default_cli_uses_symbols_subparser(
        self, manager_cls_mock, generator_cls_mock
    ) -> None:
        """No subcommand should default to symbols generation."""

        manager = manager_cls_mock.return_value
        manager.load.return_value = AppConfig(
            batch_size=1,
            symbols=SymbolsDefaults(length=10),
        )

        generator = generator_cls_mock.return_value
        generator.generate.return_value = "defaultpass"

        with redirect_stdout(io.StringIO()):
            exit_code = CommandLineApp.main("--length", "12")

        self.assertEqual(exit_code, 0)
        generated_config = generator.generate.call_args.args[0]
        self.assertEqual(generated_config.length, 12)

    @patch("passwordgen.cli.RandomWordsGenerator")
    @patch("passwordgen.cli.ConfigManager")
    def test_words_subparser_uses_words_generator(
        self, manager_cls_mock, words_generator_cls_mock
    ) -> None:
        """words subparser should route generation to RandomWordsGenerator."""

        manager = manager_cls_mock.return_value
        manager.load.return_value = AppConfig(
            batch_size=2,
            words=WordsDefaults(word_count=4, separator="-", language="en"),
            wordlists=WordlistsConfig(paths={}),
        )

        words_generator = words_generator_cls_mock.return_value
        words_generator.generate.side_effect = ["alpha-beta", "gamma-delta"]

        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = CommandLineApp.main("words", "--count", "2", "--word-count", "3")

        self.assertEqual(exit_code, 0)
        self.assertEqual(words_generator.generate.call_count, 2)
        words_config = words_generator.generate.call_args_list[0].args[0]
        self.assertEqual(words_config.word_count, 3)
        self.assertEqual(output.getvalue().splitlines(), ["alpha-beta", "gamma-delta"])

    @patch("passwordgen.cli.AlternatingGenerator")
    @patch("passwordgen.cli.ConfigManager")
    def test_alternating_subparser_uses_alternating_generator(
        self, manager_cls_mock, alternating_generator_cls_mock
    ) -> None:
        """alternating subparser should route generation correctly."""

        manager = manager_cls_mock.return_value
        manager.load.return_value = AppConfig(
            batch_size=1,
            alternating=AlternatingDefaults(
                word_count=3,
                symbols_per_group=2,
                language="en",
                use_digits=True,
            ),
            wordlists=WordlistsConfig(paths={}),
        )

        alternating_generator = alternating_generator_cls_mock.return_value
        alternating_generator.generate.return_value = "word!!Word"

        with redirect_stdout(io.StringIO()):
            exit_code = CommandLineApp.main(
                "alternating",
                "--word-count",
                "4",
                "--symbols-per-group",
                "3",
                "--no-digits",
            )

        self.assertEqual(exit_code, 0)
        alternating_config = alternating_generator.generate.call_args.args[0]
        self.assertEqual(alternating_config.word_count, 4)
        self.assertEqual(alternating_config.symbols_per_group, 3)
        self.assertFalse(alternating_config.use_digits)

    def test_invalid_argument_returns_parser_error_code(self) -> None:
        """Unknown arguments should return argparse error code 2."""

        exit_code = CommandLineApp.main("--not-a-real-option")

        self.assertEqual(exit_code, 2)

    def test_top_level_help_lists_available_algorithms(self) -> None:
        """Global --help should show all algorithm subcommands."""

        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = CommandLineApp.main("--help")

        help_text = output.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("symbols", help_text)
        self.assertIn("words", help_text)
        self.assertIn("alternating", help_text)

    @patch("passwordgen.cli._", side_effect=lambda message: f"TR::{message}")
    def test_cli_help_uses_translation_function(self, _translate_mock) -> None:
        """Parser help text should flow through i18n translation function."""

        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = CommandLineApp.main("--help")

        self.assertEqual(exit_code, 0)
        self.assertIn(
            "TR::Generate secure passwords in CLI mode or launch the GUI.",
            output.getvalue(),
        )
