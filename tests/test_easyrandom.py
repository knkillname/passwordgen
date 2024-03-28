"""Test the EasyRandomPasswordGenerator class."""

import re
import unittest

from passwordgen.generators.easyrandom import EasyRandomPasswordGenerator


class TestEasyRandom(unittest.TestCase):
    """Test the EasyRandomPasswordGenerator class."""

    dictionary = ["this", "is", "a", "test"]

    def test_init(self) -> None:
        """Test initialization of the generator."""
        # Test default values
        generator = EasyRandomPasswordGenerator(dictionary=self.dictionary)
        self.assertEqual(generator.length, 16)
        self.assertEqual(generator.dictionary, self.dictionary)
        self.assertEqual(generator.filler_characters, "!@#$%^&*()[]{}_+-=0123456789")

        # Test custom values
        generator = EasyRandomPasswordGenerator(
            length=32,
            dictionary=self.dictionary,
            filler_characters="!',",
        )
        self.assertEqual(generator.length, 32)
        self.assertEqual(generator.dictionary, self.dictionary)
        self.assertEqual(generator.filler_characters, "!',")
        self.assertEqual(generator.max_filler_ratio, 1 / 3)

        # Attempt to initialize with an empty dictionary
        with self.assertRaises(ValueError):
            EasyRandomPasswordGenerator(dictionary=[])
        # Attempt to initialize with a string dictionary
        with self.assertRaises(TypeError):
            EasyRandomPasswordGenerator(dictionary="this is a test")
        # Attempt to initialize with a non-sequence dictionary
        with self.assertRaises(TypeError):
            EasyRandomPasswordGenerator(dictionary=123)  # type: ignore
        # Attempt to initialize with a dictionary with some non-string
        # values
        with self.assertRaises(TypeError):
            EasyRandomPasswordGenerator(dictionary=[123, "test"])  # type: ignore
        # Attempt to initialize with a non-string filler_characters
        with self.assertRaises(TypeError):
            EasyRandomPasswordGenerator(
                dictionary=self.dictionary, filler_characters=123  # type: ignore
            )
        # Attempt to initialize with an empty filler_characters
        with self.assertRaises(ValueError):
            EasyRandomPasswordGenerator(
                dictionary=self.dictionary, filler_characters=""
            )
        # Attempt to initialize with a non-integer length
        with self.assertRaises(TypeError):
            EasyRandomPasswordGenerator(
                dictionary=self.dictionary, length="16"  # type: ignore
            )
        # Attempt to initialize with a length less than 1
        with self.assertRaises(ValueError):
            EasyRandomPasswordGenerator(dictionary=self.dictionary, length=0)
        # Attempt to initialize with a max_filler_ratio outside the
        # range [0, 1]
        with self.assertRaises(ValueError):
            EasyRandomPasswordGenerator(
                dictionary=self.dictionary, max_filler_ratio=1.1
            )
        with self.assertRaises(ValueError):
            EasyRandomPasswordGenerator(
                dictionary=self.dictionary, max_filler_ratio=-0.1
            )
        # Attempt to initialize with a max_filler_ratio that is not a
        # float
        with self.assertRaises(TypeError):
            EasyRandomPasswordGenerator(
                dictionary=self.dictionary, max_filler_ratio="0.5"  # type: ignore
            )

    def test_generate_password(self) -> None:
        """ "Test the generate_password method."""

        # Test default values
        generator = EasyRandomPasswordGenerator(dictionary=self.dictionary, length=16)
        # Create a regex to group words and filler characters
        filler = re.escape(generator.filler_characters)
        regex = re.compile(rf"([a-zA-Z]+)([{filler}]+)")

        for i in range(100):
            with self.subTest(i=i):
                password = generator.generate_password()
                self.assertEqual(len(password.password), generator.length)
                self.assertRegex(password.password, regex)
                # Parse the password into groups of words and filler
                # characters
                groups = regex.findall(password.password)
                # Check that the groups match the full password
                self.assertEqual(
                    "".join(word + filler for word, filler in groups), password.password
                )
                words, fillers = zip(*groups)
                # Check that the words belong to the dictionary
                for word in words:
                    self.assertIn(word, generator.dictionary)
                # Check that the filler characters belong to the
                # filler_characters string
                for filler in fillers:
                    self.assertTrue(all(c in filler for c in filler))
