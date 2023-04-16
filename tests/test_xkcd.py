"""Test the XKCDPasswordGenerator class."""

import tempfile
import unittest

from passwordgen.generators import XKCDPasswordGenerator


class TestXKCDPasswordGenerator(unittest.TestCase):
    """Test the XKCDPasswordGenerator class."""

    def test_instantiation(self):
        """Test the instantiation of the XKCDPasswordGenerator class."""
        # Attempt to instantiate the class with any wrong type should
        # raise a TypeError.
        with self.assertRaises(TypeError):
            XKCDPasswordGenerator(word_list=123)
        with self.assertRaises(TypeError):
            XKCDPasswordGenerator(word_list=[123, "a"])
        with self.assertRaises(TypeError):
            XKCDPasswordGenerator(count="123", word_list=["a", "b"])
        with self.assertRaises(TypeError):
            XKCDPasswordGenerator(separator=123, word_list=["a", "b"])

        # Instantiation with an empty list of words should raise a ValueError.
        with self.assertRaises(ValueError):
            XKCDPasswordGenerator(word_list=[])

        # Instantiation with a negative count should raise a ValueError.
        with self.assertRaises(ValueError):
            XKCDPasswordGenerator(word_list=["a", "b"], count=-1)

    def test_from_word_list_file(self):
        """Test the from_word_list_file method."""
        # Create a temporary file with a word list.
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as file:
            file.write("foo\nbar\nbaz\nqux\n")
            file.seek(0)

            # Test the instantiation of the class from the word list file.
            generator = XKCDPasswordGenerator.from_word_list_file(file.name)
            self.assertEqual(generator.word_list, ["foo", "bar", "baz", "qux"])

        # Test the instantiation of the class from a non-existing file.
        with self.assertRaises(FileNotFoundError):
            XKCDPasswordGenerator.from_word_list_file("non-existing-file")

        # Test the instantiation of the class with a wrong argument type.
        with self.assertRaises(TypeError):
            XKCDPasswordGenerator.from_word_list_file(123)

    def test_generate_password(self):
        """Test the generation of passwords."""
        word_list = ["foo", "bar", "baz", "qux"]
        # Test the generation of a password with the default parameters.
        generator = XKCDPasswordGenerator(word_list=word_list, separator="\t", count=4)
        password = generator.generate_password()
        parts = password.password.split("\t")
        self.assertEqual(len(parts), 4)
        for i, part in enumerate(parts):
            with self.subTest(i=i):
                self.assertIn(part, word_list)
