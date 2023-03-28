import unittest

from passwordgen.randomstring import RandomString


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

    def test_generate_password(self):
        # The length of the password should be
        # ceil(strength / entropy_per_character).
        # Since the default character set has 62 characters, the entropy
        # per character is 5.95 bits.
        password = RandomString().generate_password(42)
        self.assertEqual(len(password), 8)
        password = RandomString().generate_password(128)
        self.assertEqual(len(password), 22)

        # Generate a password with the default character set.
        password = RandomString().generate_password(42)
        self.assertTrue(password.isalnum())

        # Generate a password with a custom character set.
        password = RandomString(
            use_lowercase=False,
            use_uppercase=False,
            use_digits=False,
            use_punctuation=False,
            other_characters="abc",
        ).generate_password(128)
        self.assertTrue(password.isalpha())
        self.assertTrue(password.islower())
        self.assertTrue(password.isascii())
        self.assertLessEqual(set(password), set("abc"))
