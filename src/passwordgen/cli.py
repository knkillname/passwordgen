"""Command-line application for the secure password generator."""

from __future__ import annotations

import argparse
import sys

from passwordgen.config.manager import ConfigManager
from passwordgen.config.schema import AppConfig
from passwordgen.generators.alternating import AlternatingConfig, AlternatingGenerator
from passwordgen.generators.symbols import RandomSymbolsGenerator, SymbolsConfig
from passwordgen.generators.words import RandomWordsGenerator, WordsConfig
from passwordgen.gui.app import run_app
from passwordgen.i18n import _
from passwordgen.wordlists import WordlistLoader, available_dictionary_keys


class CommandLineApp:
    """Application service for CLI argument parsing and execution."""

    @classmethod
    def _build_parser(cls) -> argparse.ArgumentParser:
        """Build command-line argument parser."""

        parser = argparse.ArgumentParser(
            prog="passwordgen",
            description=_("Generate secure passwords in CLI mode or launch the GUI."),
        )
        parser.add_argument(
            "--gui",
            action="store_true",
            help=_("Launch the Tkinter GUI instead of running in CLI mode."),
        )

        subparsers = parser.add_subparsers(dest="algorithm")

        symbols_parser = subparsers.add_parser(
            "symbols",
            help=_("Generate random symbol-based passwords."),
        )
        symbols_parser.add_argument(
            "--count",
            type=int,
            default=None,
            help=_("Number of passwords to print."),
        )
        symbols_parser.add_argument(
            "--length",
            type=int,
            default=None,
            help=_("Password length."),
        )
        symbols_parser.add_argument(
            "--no-upper",
            action="store_true",
            help=_("Disable uppercase letters."),
        )
        symbols_parser.add_argument(
            "--no-digits",
            action="store_true",
            help=_("Disable digits."),
        )
        symbols_parser.add_argument(
            "--no-punctuation",
            action="store_true",
            help=_("Disable punctuation symbols."),
        )
        symbols_parser.add_argument(
            "--custom-charset",
            default="",
            help=_("Custom character set."),
        )

        words_parser = subparsers.add_parser(
            "words",
            help=_("Generate random-word passphrases."),
        )
        words_parser.add_argument(
            "--count",
            type=int,
            default=None,
            help=_("Number of passwords to print."),
        )
        words_parser.add_argument(
            "--word-count",
            type=int,
            default=None,
            help=_("Number of words in each passphrase."),
        )
        words_parser.add_argument(
            "--separator",
            default=None,
            help=_("Separator between words."),
        )
        words_parser.add_argument(
            "--language",
            default=None,
            help=_("Dictionary language key (for example: en, es)."),
        )

        alternating_parser = subparsers.add_parser(
            "alternating",
            help=_("Generate alternating words-and-symbols passwords."),
        )
        alternating_parser.add_argument(
            "--count",
            type=int,
            default=None,
            help=_("Number of passwords to print."),
        )
        alternating_parser.add_argument(
            "--word-count",
            type=int,
            default=None,
            help=_("Number of words in each password."),
        )
        alternating_parser.add_argument(
            "--symbols-per-group",
            type=int,
            default=None,
            help=_("Symbols inserted between words."),
        )
        alternating_parser.add_argument(
            "--language",
            default=None,
            help=_("Dictionary language key (for example: en, es)."),
        )
        alternating_parser.add_argument(
            "--no-digits",
            action="store_true",
            help=_("Disable digits in symbol groups."),
        )

        return parser

    @classmethod
    def _run_cli(cls, options: argparse.Namespace) -> int:
        """Run non-interactive CLI generation flow."""

        app_config = ConfigManager().load()
        algorithm = options.algorithm or "symbols"
        count = app_config.batch_size if options.count is None else options.count
        if count < 1:
            raise ValueError(_("count must be at least 1"))

        if algorithm == "symbols":
            cls._run_symbols_cli(options, app_config, count)
            return 0
        if algorithm == "words":
            cls._run_words_cli(options, app_config, count)
            return 0
        cls._run_alternating_cli(options, app_config, count)
        return 0

    @classmethod
    def _run_symbols_cli(
        cls, options: argparse.Namespace, app_config: AppConfig, count: int
    ) -> None:
        """Generate symbol-based passwords in CLI mode."""

        config = app_config.symbols
        length = config.length if options.length is None else options.length
        symbols_config = SymbolsConfig(
            length=length,
            use_upper=config.use_upper and not options.no_upper,
            use_digits=config.use_digits and not options.no_digits,
            use_punctuation=config.use_punctuation and not options.no_punctuation,
            custom_charset=str(options.custom_charset),
        )
        generator = RandomSymbolsGenerator()
        for _ in range(count):
            print(generator.generate(symbols_config))

    @classmethod
    def _run_words_cli(
        cls, options: argparse.Namespace, app_config: AppConfig, count: int
    ) -> None:
        """Generate word-based passphrases in CLI mode."""

        defaults = app_config.words
        language = defaults.language if options.language is None else options.language
        cls._validate_language(language, app_config)
        words_config = WordsConfig(
            word_count=(
                defaults.word_count if options.word_count is None else options.word_count
            ),
            separator=defaults.separator if options.separator is None else options.separator,
            language=language,
        )
        generator = RandomWordsGenerator(WordlistLoader(), app_config.wordlists)
        for _ in range(count):
            print(generator.generate(words_config))

    @classmethod
    def _run_alternating_cli(
        cls, options: argparse.Namespace, app_config: AppConfig, count: int
    ) -> None:
        """Generate alternating passwords in CLI mode."""

        defaults = app_config.alternating
        language = defaults.language if options.language is None else options.language
        cls._validate_language(language, app_config)
        alternating_config = AlternatingConfig(
            word_count=(
                defaults.word_count if options.word_count is None else options.word_count
            ),
            symbols_per_group=(
                defaults.symbols_per_group
                if options.symbols_per_group is None
                else options.symbols_per_group
            ),
            language=language,
            use_digits=defaults.use_digits and not options.no_digits,
        )
        generator = AlternatingGenerator(WordlistLoader(), app_config.wordlists)
        for _ in range(count):
            print(generator.generate(alternating_config))

    @classmethod
    def _validate_language(cls, language: str, app_config: AppConfig) -> None:
        """Validate language key against available dictionaries."""

        available_languages = set(available_dictionary_keys(app_config.wordlists))
        if language not in available_languages:
            raise ValueError(_("Unknown language: {language}").format(language=language))

    @classmethod
    def _normalize_args(cls, args: tuple[str, ...]) -> list[str]:
        """Convert legacy top-level CLI arguments into the `symbols` subcommand."""

        if not args:
            return ["symbols"]
        if args[0] in {"-h", "--help", "--gui", "symbols", "words", "alternating"}:
            return list(args)
        return ["symbols", *args]

    @classmethod
    def main(cls, *args: str) -> int:
        """Run CLI mode by default, or GUI mode when requested."""

        parser = cls._build_parser()

        try:
            options = parser.parse_args(cls._normalize_args(args))
        except SystemExit as exc:
            if isinstance(exc.code, int):
                return exc.code
            return 1

        if options.gui:
            run_app()
            return 0

        try:
            return cls._run_cli(options)
        except (OSError, TypeError, ValueError) as exc:
            print(str(exc), file=sys.stderr)
            return 1

    @classmethod
    def cli(cls) -> int:
        """Run CommandLineApp using the current process arguments."""

        return cls.main(*sys.argv[1:])


def cli() -> int:
    """Console-script wrapper that forwards process argv to CommandLineApp."""

    return CommandLineApp.cli()
