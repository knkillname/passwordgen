"""Test the random string password generator."""
import string
import unittest

from passwordgen.generators import RandomStringPasswordGenerator


class TestRandomStringPasswordGenerator(unittest.TestCase):
    """Test the random string password generator."""

    def test_instantiation(self) -> None:
        """Test instantiating the password generator."""
        generator = RandomStringPasswordGenerator()
        self.assertEqual(generator.length, 8)
        self.assertTrue(generator.use_uppercase)
        self.assertTrue(generator.use_lowercase)
        self.assertTrue(generator.use_digits)
        self.assertTrue(generator.use_punctuation)
        self.assertEqual(generator.other_characters, "")

        # Using any wrong argument type should rise an error
        with self.assertRaises(TypeError):
            RandomStringPasswordGenerator(length="8")  # type: ignore
        with self.assertRaises(TypeError):
            RandomStringPasswordGenerator(use_uppercase="True")  # type: ignore
        with self.assertRaises(TypeError):
            RandomStringPasswordGenerator(use_lowercase="True")  # type: ignore
        with self.assertRaises(TypeError):
            RandomStringPasswordGenerator(use_digits="True")  # type: ignore
        with self.assertRaises(TypeError):
            RandomStringPasswordGenerator(use_punctuation="True")  # type: ignore
        with self.assertRaises(TypeError):
            RandomStringPasswordGenerator(other_characters=1)  # type: ignore

        # Using a negative length should rise an error
        with self.assertRaises(ValueError):
            RandomStringPasswordGenerator(length=-1)

    def test_generate_password(self) -> None:
        """Test generating a password."""
        # Using the default options should generate a password of the
        # default length with the default characters
        generator = RandomStringPasswordGenerator()
        password = generator.generate_password()
        expected_charset = "".join(
            [
                string.ascii_uppercase,
                string.ascii_lowercase,
                string.digits,
                string.punctuation,
            ]
        )
        self.assertEqual(len(password.password), generator.length)
        self.assertLessEqual(set(password.password), set(expected_charset))

        # Using a different charset should generate a password with those
        # characters
        generator = RandomStringPasswordGenerator(
            length=13,
            use_uppercase=False,
            use_lowercase=False,
            use_digits=False,
            use_punctuation=False,
            other_characters="abc",
        )
        password = generator.generate_password()
        self.assertEqual(len(password.password), 13)
        self.assertTrue(all(char in "abc" for char in password.password))

        # Using a different length and charset should generate a password of
        # that length with those characters
        generator = RandomStringPasswordGenerator(
            length=16,
            use_uppercase=False,
            use_lowercase=False,
            use_digits=False,
            use_punctuation=False,
            other_characters="xyz",
        )
        password = generator.generate_password()
        self.assertEqual(len(password.password), 16)
        self.assertTrue(all(char in "xyz" for char in password.password))

        # A password using only digits
        generator = RandomStringPasswordGenerator(
            length=16,
            use_uppercase=False,
            use_lowercase=False,
            use_digits=True,
            use_punctuation=False,
            other_characters="",
        )
        password = generator.generate_password()
        self.assertEqual(len(password.password), 16)
        self.assertTrue(all(char in string.digits for char in password.password))

    def test_generate_many_passwords(self) -> None:
        """Test generating many passwords."""
        # Using the default options should generate a password of the
        # default length with the default characters
        generator = RandomStringPasswordGenerator()
        passwords = list(generator.generate_many_passwords(10))
        expected_charset = "".join(
            [
                string.ascii_uppercase,
                string.ascii_lowercase,
                string.digits,
                string.punctuation,
            ]
        )
        self.assertEqual(len(passwords), 10)
        for password in passwords:
            self.assertEqual(len(password.password), generator.length)
            self.assertLessEqual(set(password.password), set(expected_charset))

        # Using a different charset should generate a password with those
        # characters
        generator = RandomStringPasswordGenerator(
            length=13,
            use_uppercase=False,
            use_lowercase=False,
            use_digits=False,
            use_punctuation=False,
            other_characters="abc",
        )
        passwords = list(generator.generate_many_passwords(10))
        self.assertEqual(len(passwords), 10)
        for password in passwords:
            self.assertEqual(len(password.password), 13)
            self.assertTrue(all(char in "abc" for char in password.password))
