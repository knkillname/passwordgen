import unittest

from passwordgen.algorithms.randomstring import RandomString


class TestRandomString(unittest.TestCase):
    def test_instantiation(self):
        # Instantiation without any character set should fail.
        with self.assertRaises(ValueError):
            RandomString(
                use_lowercase=False,
                use_uppercase=False,
                use_digits=False,
                use_punctuation=False,
                other_characters="",
            )

        # Instantiation with wrong types should fail.
        with self.assertRaises(TypeError):
            RandomString(use_lowercase="True")
        with self.assertRaises(TypeError):
            RandomString(use_uppercase="True")
        with self.assertRaises(TypeError):
            RandomString(use_digits="True")
        with self.assertRaises(TypeError):
            RandomString(use_punctuation="True")
        with self.assertRaises(TypeError):
            RandomString(other_characters=123)

    def test_generate_password_by_strength(self):
        # The length of the password should be
        # ceil(strength / entropy_per_character).
        # Since the default character set has 62 characters, the entropy
        # per character is 5.95 bits.

        # Generate a password with the default strength which is 42.
        password = RandomString().generate_password()
        self.assertEqual(len(password.password), 8)

        # Generate a password with a custom strength.
        password = RandomString().generate_password(strength=42)
        self.assertEqual(len(password.password), 8)
        self.assertEqual(password.strength, 42)
        password = RandomString().generate_password(strength=128)
        self.assertEqual(len(password.password), 22)
        self.assertEqual(password.strength, 128)

        # Generate a password with the default character set.
        password = RandomString().generate_password(strength=42)
        self.assertTrue(password.password.isalnum())

        # Generate a password with a custom character set.
        password = RandomString(
            use_lowercase=False,
            use_uppercase=False,
            use_digits=False,
            use_punctuation=False,
            other_characters="abc",
        ).generate_password(strength=128)
        self.assertTrue(password.password.isalpha())
        self.assertTrue(password.password.islower())
        self.assertTrue(password.password.isascii())
        self.assertLessEqual(set(password.password), set("abc"))

    def test_generate_password_by_length(self):
        # Generate a password with the default character set.
        password = RandomString().generate_password(length=42)
        self.assertEqual(len(password.password), 42)
        self.assertTrue(password.password.isalnum())

        # Generate a password with a custom character set.
        password = RandomString(
            use_lowercase=False,
            use_uppercase=False,
            use_digits=False,
            use_punctuation=False,
            other_characters="abc",
        ).generate_password(length=128)
        self.assertEqual(len(password.password), 128)
        self.assertTrue(password.password.isalpha())
        self.assertTrue(password.password.islower())
        self.assertTrue(password.password.isascii())
        self.assertLessEqual(set(password.password), set("abc"))

    def test_generate_password_by_strength_and_length(self):
        # Specifying both strength and length should fail.
        with self.assertRaises(ValueError):
            RandomString().generate_password(strength=42, length=42)
