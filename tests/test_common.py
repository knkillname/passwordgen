"""Test the common module."""
import unittest
from unittest import mock

from passwordgen.common import CrackMethodEnum, Duration, Password, util


class TestCommon(unittest.TestCase):
    """Test the common module."""

    def test_password(self):
        """Test the Password class."""
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

        # Test the time to crack calculation by a dictionary attack on a
        # password with no strength.
        crack_time = Password("aaaa", 0).time_to_crack(1, CrackMethodEnum.DICTIONARY)
        crack_time = Password("sequoia", 0).time_to_crack(1, CrackMethodEnum.BEST)

        # Test converting a password to a human-readable string.
        result = str(Password("sequoia", 42))
        self.assertIn("sequoia", result)

    def test_duration(self):
        """Test the Duration class."""
        # Test instantiating a duration.
        duration = Duration(years=1, days=2, hours=3, minutes=4, seconds=5)
        self.assertEqual(duration.years, 1)
        self.assertEqual(duration.days, 2)
        self.assertEqual(duration.hours, 3)
        self.assertEqual(duration.minutes, 4)
        self.assertEqual(duration.seconds, 5)

        # Test the total seconds calculation.
        duration = Duration(years=1, days=2, hours=3, minutes=4, seconds=5)
        self.assertAlmostEqual(duration.total_seconds(), 31740771.079999994)

        # Test the total seconds calculation with a duration of 0.
        duration = Duration(seconds=0)
        self.assertEqual(duration.total_seconds(), 0.0)

        # Test converting a duration to a human-readable string.
        self.assertEqual(Duration(years=2123456).describe(), "2 million years")
        self.assertEqual(Duration(years=123456).describe(), "123 thousand years")
        self.assertEqual(Duration(years=1, days=2).describe(), "1 year")
        self.assertEqual(Duration(years=2, days=30).describe(), "2 years")
        self.assertEqual(Duration(days=1, hours=10).describe(), "1 day")
        self.assertEqual(Duration(days=2, hours=10).describe(), "2 days")
        self.assertEqual(Duration(hours=1, minutes=10).describe(), "1 hour")
        self.assertEqual(Duration(hours=2, minutes=10).describe(), "2 hours")
        self.assertEqual(Duration(minutes=1, seconds=10).describe(), "1 minute")
        self.assertEqual(Duration(minutes=2, seconds=10).describe(), "2 minutes")
        self.assertEqual(Duration(seconds=1).describe(), "1 second")
        self.assertEqual(Duration(seconds=2).describe(), "2 seconds")
        self.assertEqual(Duration(seconds=0).describe(), "Less than a second")

    def test_entropy(self):
        """Test the entropy function."""
        # Test calculating the entropy of a probability distribution.
        self.assertEqual(util.entropy([1]), 0.0)
        self.assertEqual(util.entropy([1, 1]), 1)
        self.assertEqual(util.entropy([2, 1, 1]), 1.5)

        # Test type checking.
        with self.assertRaises(TypeError):
            util.entropy(1)

        # Test value checking.
        with self.assertRaises(ValueError):
            util.entropy([1, -1])

        with self.assertRaises(ValueError):
            util.entropy([0, 0, 0, 0])

    def test_get_resource_path(self):
        """Test the get_resource_path function."""
        # Test getting the path to a resource.
        path = util.get_resource_path("test.txt")
        self.assertEqual("test.txt", path.parts[-1])

    def test_normalize_time(self):
        """Test the normalize_time function."""
        # The util.normalize_time function is used in the Duration class
        # to normalize the number of seconds, minutes, hours, and days
        # in a duration.

        # Test normalizing a duration.
        duration = Duration(years=1, days=2, hours=3, minutes=4, seconds=5)
        self.assertEqual(duration.years, 1)
        self.assertEqual(duration.days, 2)
        self.assertEqual(duration.hours, 3)
        self.assertEqual(duration.minutes, 4)
        self.assertEqual(duration.seconds, 5)

        # Test normalizing a duration with more than 60 seconds.
        duration = Duration(seconds=61)
        self.assertEqual(duration.years, 0)
        self.assertEqual(duration.days, 0)
        self.assertEqual(duration.hours, 0)
        self.assertEqual(duration.minutes, 1)
        self.assertEqual(duration.seconds, 1)


if __name__ == "__main__":
    unittest.main()
