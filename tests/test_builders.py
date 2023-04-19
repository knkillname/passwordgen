"""Test the generator builders module."""

import tempfile
import unittest
from pathlib import Path

from passwordgen.common import util
from passwordgen.generators.builders import EasyRandomBuilder, XKCDGeneratorBuilder


class TestGeneratorBuilders(unittest.TestCase):
    """Test the generator builders module."""

    def test_xkcd_builder(self):
        """Test the XKCDGeneratorBuilder class."""
        # Instantiating a builder with a non-existent word list files
        # directory should result in a FileNotFoundError.
        with self.assertRaises(FileNotFoundError):
            builder = XKCDGeneratorBuilder(data_dir="non-existent")

        # Instantiating a builder with a bad type data directory should
        # result in a TypeError.
        with self.assertRaises(TypeError):
            builder = XKCDGeneratorBuilder(data_dir=123)

        # Adding words from a non sequence of strings should result in a TypeError.
        with self.assertRaises(TypeError):
            builder = XKCDGeneratorBuilder()
            builder.add_words_from_list(123)
        with self.assertRaises(TypeError):
            builder = XKCDGeneratorBuilder()
            builder.add_words_from_list(["this", 123])
        # Attempting to add words from a non file should result in a TypeError.
        with self.assertRaises(TypeError):
            builder = XKCDGeneratorBuilder()
            builder.add_words_from_file(123)

        # The default data directory should be the wordlists directory
        # in the package data.
        builder = XKCDGeneratorBuilder()
        self.assertEqual(builder.data_dir, util.get_resource_path("wordlists"))

        # Building a generator with a word list:
        builder = XKCDGeneratorBuilder()
        builder.add_words_from_list(["this", "is", "a", "test"])
        builder.with_count(2)
        builder.with_separator(",")
        generator = builder.build()
        self.assertEqual(generator.separator, ",")
        self.assertEqual(generator.count, 2)
        self.assertEqual(generator.word_list, ["this", "is", "a", "test"])
        # After clearing the word list, the generator should not be
        # buildable
        builder.clear_word_list()
        with self.assertRaises(ValueError):
            builder.build()

        # Building a generator with an included word list file:
        builder = XKCDGeneratorBuilder()
        builder.add_words_from_file("en_GB")
        generator = builder.build()
        # Get expected set of words from the file
        file_path = util.get_resource_path("wordlists/en_GB.txt")
        with file_path.open("r") as file:
            expected_words = {
                stripped for line in file.readlines() if (stripped := line.strip())
            }
        self.assertEqual(set(generator.word_list), expected_words)
        self.assertEqual(len(generator.word_list), len(expected_words))

        # Building a generator with a custom data directory:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a custom word list file
            file_path = Path(temp_dir) / "custom.txt"
            with file_path.open("w") as file:
                file.writelines(["this\n", "is\n", "a\n", "test\n"])
            # Create a builder with the custom data directory
            builder = XKCDGeneratorBuilder(data_dir=temp_dir)
            available_word_lists = builder.get_available_word_lists_files()
            self.assertEqual(available_word_lists, ["custom"])

        # Building a generator with no words should result in a
        # ValueError.
        with self.assertRaises(ValueError):
            builder = XKCDGeneratorBuilder()
            builder.build()

        # Building a generator after a reset should result in a ValueError.
        with self.assertRaises(ValueError):
            builder = XKCDGeneratorBuilder()
            builder.add_words_from_list(["this", "is", "a", "test"])
            builder.reset()
            builder.build()

    def test_easy_random_builder(self):
        """Test the EasyRandomBuilder class."""
        # Instantiating a builder with a bad type data directory should
        # result in a TypeError.
        with self.assertRaises(TypeError):
            builder = EasyRandomBuilder(data_dir=123)

        # The default data directory should be the wordlists directory
        # in the package data.
        builder = EasyRandomBuilder()
        self.assertEqual(builder.data_dir, util.get_resource_path("wordlists"))

        # Building a generator with a word list:
        builder = EasyRandomBuilder()
        builder.add_words_from_list(["this", "is", "a", "test"])
        builder.with_length(13)
        builder.add_filler_chars("1234")
        generator = builder.build()
        self.assertEqual(generator.filler_characters, "1234")
        self.assertEqual(generator.length, 13)
        self.assertEqual(generator.dictionary, ["this", "is", "a", "test"])
        # After a reset the generator should not be buildable since
        # the dictionary is empty.
        builder.reset()
        with self.assertRaises(ValueError):
            builder.build()

        # Building a generator with an included word list file:
        builder = EasyRandomBuilder()
        builder.add_words_from_file("en_GB")
        generator = builder.build()
        # Get expected set of words from the file
        file_path = util.get_resource_path("wordlists/en_GB.txt")
        with file_path.open("r") as file:
            expected_words = {
                stripped for line in file.readlines() if (stripped := line.strip())
            }
        self.assertEqual(set(generator.dictionary), expected_words)
        self.assertEqual(len(generator.dictionary), len(expected_words))

        # Building a generator with a custom data directory:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a custom word list file
            file_path = Path(temp_dir) / "custom.txt"
            with file_path.open("w") as file:
                file.writelines(["this\n", "is\n", "a\n", "test\n"])
            # Create a builder with the custom data directory
            builder = EasyRandomBuilder(data_dir=temp_dir)
            available_word_lists = builder.get_available_dictionaries()
            self.assertEqual(available_word_lists, ["custom"])

        # Building a generator with no words should result in a
        # ValueError.
        with self.assertRaises(ValueError):
            builder = EasyRandomBuilder()
            builder.build()
