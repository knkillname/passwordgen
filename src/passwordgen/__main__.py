"""Command line interface for the password generator.

This module contains the main entry point for the password generator
program.

Classes
-------
PasswordGen
    The main class for the password generator program.
"""
import argparse

from .generators.builders.easyrandombuilder import EasyRandomBuilder
from .generators.builders.xkcdbuilder import XKCDGeneratorBuilder
from .generators.randomstring import RandomStringPasswordGenerator
from .generators.xkcd import XKCDPasswordGenerator


class PasswordGen:
    """The main class for the password generator program."""

    def __init__(self):
        """Initialize the program."""
        self.parser = self.create_parser()

    def main(self) -> None:
        """Run the program.

        Raises
        ------
        ValueError
            If the generator is unknown.
        """
        args = self.parser.parse_args()
        if args.generator == "random":
            self.use_random(args)
        elif args.generator == "xkcd":
            self.use_xkcd(args)
        elif args.generator == "easy":
            self.use_easy_random(args)
        else:
            raise ValueError(f"Unknown generator: {args.generator}")

    def use_random(self, args: argparse.Namespace) -> None:
        """Use the random string password generator.

        Parameters
        ----------
        args : argparse.Namespace
            The arguments.
        """
        generator = RandomStringPasswordGenerator(
            length=args.length,
            use_uppercase=args.use_uppercase,
            use_lowercase=args.use_lowercase,
            use_digits=args.use_digits,
            use_punctuation=args.use_punctuation,
            other_characters=args.other_characters,
        )
        for password in generator.generate_many_passwords(count=args.count):
            print(password)

    def use_xkcd(self, args: argparse.Namespace) -> None:
        """Use the XKCD password generator.

        Parameters
        ----------
        args : argparse.Namespace
            The arguments.
        """
        builder = XKCDGeneratorBuilder()
        builder.add_words_from_file(args.word_list)
        builder.with_count(args.word_count)
        builder.with_separator(args.separator)
        generator = builder.build()
        for password in generator.generate_many_passwords(count=args.count):
            print(password)

    def use_easy_random(self, args: argparse.Namespace) -> None:
        """Use the easy random password generator.

        Parameters
        ----------
        args : argparse.Namespace
            The arguments.
        """
        builder = EasyRandomBuilder()
        builder.add_words_from_file(args.word_list)
        builder.with_length(args.length)
        builder.add_filler_chars(args.filler_chars)
        generator = builder.build()
        for password in generator.generate_many_passwords(count=args.count):
            print(password)

    def create_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser for the program.

        Returns
        -------
        argparse.ArgumentParser
            The argument parser.
        """
        parser = argparse.ArgumentParser()
        # Add subparser for password generators
        subparsers = parser.add_subparsers(
            title="Password generator", dest="generator", required=True
        )

        # Add subparser for random string password generator
        self._add_random_subparser(subparsers)

        # Add subparser for XKCD password generator
        self._add_xkcd_subparser(subparsers)

        # Add subparser for easy random password generator
        self._add_easy_random_subparser(subparsers)

        return parser

    def _add_xkcd_subparser(self, subparsers: argparse._SubParsersAction):
        """Add a subparser for the XKCD password generator.

        Parameters
        ----------
        subparsers : argparse._SubParsersAction
            The subparsers to add the subparser to.
        """
        xkcd_parser = subparsers.add_parser(
            "xkcd", help=XKCDPasswordGenerator.description
        )
        xkcd_parser.add_argument(
            "-c",
            "--count",
            type=int,
            default=10,
            help="The number of passwords to generate (default: 10)",
        )
        # Mimic the arguments from XKCDPasswordGenerator
        xkcd_parser.add_argument(
            "-w",
            "--word-list",
            dest="word_list",
            default="en_GB",
            help="The word list to use (default: en_GB)",
        )
        xkcd_parser.add_argument(
            "-n",
            "--word-count",
            dest="word_count",
            type=int,
            default=4,
            help="The number of words to use (default: 4)",
        )
        xkcd_parser.add_argument(
            "-s",
            "--separator",
            default=" ",
            help="The separator to use between words (default: ' ')",
        )

    def _add_random_subparser(self, subparsers):
        """Add a subparser for the random string password generator.

        Parameters
        ----------
        subparsers : argparse._SubParsersAction
            The subparsers to add the subparser to.
        """
        random_parser = subparsers.add_parser(
            "random", help=RandomStringPasswordGenerator.description
        )
        random_parser.add_argument(
            "-c",
            "--count",
            type=int,
            default=10,
            help="The number of passwords to generate (default: 10)",
        )
        # Mimic the arguments from RandomStringPasswordGenerator
        random_parser.add_argument(
            "-l",
            "--length",
            type=int,
            default=16,
            help="The length of the password (default: 16)",
        )
        random_parser.add_argument(
            "--no-uppercase",
            action="store_false",
            dest="use_uppercase",
            help="Do not use uppercase letters in the password",
        )
        random_parser.add_argument(
            "--no-lowercase",
            action="store_false",
            dest="use_lowercase",
            help="Do not use lowercase letters in the password",
        )
        random_parser.add_argument(
            "--no-digits",
            action="store_false",
            dest="use_digits",
            help="Do not use digits in the password",
        )
        random_parser.add_argument(
            "--no-punctuation",
            action="store_false",
            dest="use_punctuation",
            help="Do not use punctuation characters in the password",
        )
        random_parser.add_argument(
            "--other",
            dest="other_characters",
            default="",
            help="Characters to include in the password",
        )

    def _add_easy_random_subparser(self, subparsers):
        """Add a subparser for the easy random string password generator.

        Parameters
        ----------
        subparsers : argparse._SubParsersAction
            The subparsers to add the subparser to.
        """
        easy_random_parser = subparsers.add_parser(
            "easy", help=RandomStringPasswordGenerator.description
        )
        easy_random_parser.add_argument(
            "-c",
            "--count",
            type=int,
            default=10,
            help="The number of passwords to generate (default: 10)",
        )
        # Mimic the arguments from RandomStringPasswordGenerator
        easy_random_parser.add_argument(
            "-l",
            "--length",
            type=int,
            default=16,
            help="The length of the password (default: 16)",
        )
        easy_random_parser.add_argument(
            "-w",
            "--word-list",
            dest="word_list",
            default="en_GB",
            help="The word list to use (default: en_GB)",
        )
        easy_random_parser.add_argument(
            "--filler",
            default="!#$%&/=?-+*<>@~0123456789",
            dest="filler_chars",
            help=(
                "Characters to use to fill the password "
                "(default: !#$%&/=?-+*<>@~0123456789)"
            ),
        )


if __name__ == "__main__":
    application = PasswordGen()
    application.main()
