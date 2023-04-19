"""Test the generator builders module."""

import tempfile
import unittest
from pathlib import Path

from passwordgen.common import util
from passwordgen.generators.builders import (
    EasyRandomPasswordGeneratorBuilder,
    XKCDPasswordGeneratorBuilder,
)
from passwordgen.generators.builders.abc import DictionaryPasswordGeneratorBuilderBase


class TestDictionaryBuilderBase(unittest.TestCase):
    """Test the DictionaryBuilderBase class."""

    class DummyBuilder(DictionaryPasswordGeneratorBuilderBase):
        """A dummy builder for testing the base class."""

        def build(self):
            pass

        def reset(self):
            pass

    def test_init(self):
        """Test the instance initialization."""
        # Test that DictionaryBuilderBase cannot be instantiated
        # directly as it is an abstract base class.
        with self.assertRaises(TypeError):
            # pylint: disable=abstract-class-instantiated
            DictionaryPasswordGeneratorBuilderBase()

        # Test that the default dictionaries directory is used if none
        # is specified.
        builder = type(self).DummyBuilder()
        self.assertEqual(
            builder.dictionaries_dir, util.get_resource_path("dictionaries")
        )

        # Test that the specified dictionaries directory is used if one
        # is specified.
        with tempfile.TemporaryDirectory() as temp_dir:
            builder = type(self).DummyBuilder(temp_dir)
            self.assertEqual(builder.dictionaries_dir, Path(temp_dir))

        # Test that a FileNotFoundError is raised if the specified
        # data directory does not exist or is not a directory.
        with self.assertRaises(FileNotFoundError):
            type(self).DummyBuilder("non-existent")
        with tempfile.NamedTemporaryFile() as file:
            with self.assertRaises(FileNotFoundError):
                type(self).DummyBuilder(file.name)

        # Test that a TypeError is raised if the specified data
        # directory is not a string or Path.
        with self.assertRaises(TypeError):
            type(self).DummyBuilder(123)

        builder = type(self).DummyBuilder()
        with self.assertRaises(TypeError):
            builder.dictionaries_dir = 123

    def test_parse_word(self):
        """Test the default implementation of parse_word."""
        builder = type(self).DummyBuilder()
        self.assertEqual(builder.parse_word("test"), "test")
        self.assertEqual(builder.parse_word(" \ttest\r\n"), "test")
        self.assertIsNone(builder.parse_word(""))
        self.assertIsNone(builder.parse_word(" \t\r\n"))

    def test_get_available_dictionaries(self):
        """Test the get_available_dictionaries method."""
        # Create a temporary directory to test with.
        with tempfile.TemporaryDirectory() as temp_dir:
            dir_path = Path(temp_dir)
            # Create a dictionary file in the directory.
            (dir_path / "test.txt").touch()
            builder = type(self).DummyBuilder(dir_path)
            # The test dictionary should be found.
            self.assertIn("test", builder.get_available_dictionaries())

    def test_add_words_from_file(self):
        """Test the add_words_from_file method."""
        builder = type(self).DummyBuilder()
        # Create a temporary file to test with.
        with tempfile.NamedTemporaryFile("wt", suffix=".txt") as file:
            file.writelines(["this\n", "is\n", "a\n", "test\n"])
            file.seek(0)
            builder.add_words_from_file(file.name)
            self.assertEqual(builder.get_dictionary(), ["this", "is", "a", "test"])

        # Attempting to add words from a non-existent file should result
        # in a FileNotFoundError.
        with self.assertRaises(FileNotFoundError):
            builder.add_words_from_file("non-existent")

        # Attempting to add words from a non file should result in a
        # TypeError.
        with self.assertRaises(TypeError):
            builder.add_words_from_file(123)

    def test_add_words_from_iterable(self):
        """Test the add_words_from_iterable method."""
        builder = type(self).DummyBuilder()
        builder.add_words_from_iterable(["this", "is", "a", "test"], filter_empty=False)
        self.assertEqual(builder.get_dictionary(), ["this", "is", "a", "test"])

        # Test that empty strings are filtered when filter_empty is True.
        builder = type(self).DummyBuilder()
        builder.add_words_from_iterable(
            ["this", "is", "a", "test", "", " ", "\t"], filter_empty=True
        )
        self.assertEqual(
            builder.get_dictionary(), ["this", "is", "a", "test", " ", "\t"]
        )

        # Attempting to add words from a non iterable of strings should
        # result in a TypeError.
        with self.assertRaises(TypeError):
            builder.add_words_from_iterable(123)
        with self.assertRaises(TypeError):
            builder.add_words_from_iterable(["this", 123])


class TestXKCDGeneratorBuilder(unittest.TestCase):
    """Test the XKCDGeneratorBuilder class."""

    test_words = ["this", "is", "a", "test"]

    def test_with_word_count(self):
        """Test the with_word_count method."""
        builder = XKCDPasswordGeneratorBuilder()
        builder.add_words_from_iterable(self.test_words)
        result = builder.with_word_count(5)
        self.assertIs(result, builder)
        instance = builder.build()
        self.assertEqual(instance.word_count, 5)

    def test_with_separator(self):
        """Test the with_separator method."""
        builder = XKCDPasswordGeneratorBuilder()
        builder.add_words_from_iterable(self.test_words)
        result = builder.with_separator("X")
        self.assertIs(result, builder)
        instance = builder.build()
        self.assertEqual(instance.separator, "X")

    def test_build(self):
        """Test the build method."""
        instance = (
            XKCDPasswordGeneratorBuilder()
            .with_separator(",")
            .with_word_count(8)
            .add_words_from_iterable(["this", "is", "a", "test"])
            .build()
        )
        self.assertEqual(instance.word_count, 8)
        self.assertEqual(instance.separator, ",")
        self.assertEqual(instance.dictionary, ["this", "is", "a", "test"])


class TestEasyRandomBuilder(unittest.TestCase):
    """Test the EasyRandomBuilder class."""

    dictionary = ["this", "is", "a", "test"]

    def test_with_length(self):
        """Test the with_length method."""
        builder = EasyRandomPasswordGeneratorBuilder().add_words_from_iterable(
            self.dictionary
        )
        result = builder.with_length(10)
        self.assertIs(result, builder)
        instance = builder.build()
        self.assertEqual(instance.length, 10)

        # Attempting to set the length to a non integer should result in
        # a TypeError.
        with self.assertRaises(TypeError):
            builder.with_length("10")

    def test_add_filler_chars(self):
        """Test the add_filler_chars method."""
        builder = EasyRandomPasswordGeneratorBuilder().add_words_from_iterable(
            self.dictionary
        )
        result = builder.add_filler_characters("-01")
        self.assertIs(result, builder)
        instance = builder.build()
        self.assertEqual(instance.filler_characters, "-01")

        # Attempting to add filler characters that are not strings
        # should result in a TypeError.
        with self.assertRaises(TypeError):
            builder.add_filler_characters(123)

        # Adding characters two times should extend the list of filler
        # characters.
        builder = EasyRandomPasswordGeneratorBuilder().add_words_from_iterable(
            self.dictionary
        )
        builder.add_filler_characters("01").add_filler_characters("23")
        instance = builder.build()
        self.assertEqual(instance.filler_characters, "0123")

    def test_reset(self):
        """Test the reset method."""
        builder = EasyRandomPasswordGeneratorBuilder().add_words_from_iterable(
            self.dictionary
        )
        builder.add_filler_characters("01").with_length(10)
        builder.reset()
        builder.add_filler_characters("23").with_length(16)
        instance = builder.build()
        self.assertEqual(instance.filler_characters, "23")
        self.assertEqual(instance.length, 16)
