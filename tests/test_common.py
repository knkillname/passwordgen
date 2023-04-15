import unittest
from unittest import mock

from passwordgen.common import CrackMethodEnum, Password


class TestPassword(unittest.TestCase):
    def test_password(self):
        # Test instantiating a password.
        password = Password("password", 42)
        self.assertEqual(password.password, "password")
        self.assertEqual(password.strength, 42)

        # Test the entropy calculation.
        # The entropy of the word "password" should be the same as the
        # entropy of the probability distribution [1, 1, 2, 1, 1, 1, 1]
        with mock.patch("passwordgen.common.util.entropy") as mock_entropy:
            password.entropy()
            mock_entropy.assert_called_once_with([1, 1, 2, 1, 1, 1, 1])

        # Test the time to crack calculation by brute force on a
        # password with no entropy.
        crack_time = Password("aaaa", 0).time_to_crack(1, CrackMethodEnum.BRUTE_FORCE)
        self.assertEqual(crack_time.total_seconds(), 0.0)

        # Test the time to crack calculation by brute force on a
        # password with 1 bit of entropy per character and 4 characters.
        crack_time = Password("abab", 0).time_to_crack(1, CrackMethodEnum.BRUTE_FORCE)
        self.assertEqual(crack_time.total_seconds(), 8.0)


if __name__ == "__main__":
    unittest.main()
