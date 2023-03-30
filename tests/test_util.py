import unittest

from passwordgen import util


class TestEntropy(unittest.TestCase):
    def test_wrong_parameters(self):
        # Test that the function raises a TypeError when wrong parameter
        # types are passed.
        with self.assertRaises(TypeError):
            util.entropy(1)
        with self.assertRaises(TypeError):
            util.entropy("1")
        with self.assertRaises(TypeError):
            util.entropy([None, None, None])

        # If probabilities are not positive, the function should raise a
        # ValueError.
        with self.assertRaises(ValueError):
            util.entropy([0.0, 1])

        with self.assertRaises(ValueError):
            util.entropy([0.0, 0.0, 0.0])

        with self.assertRaises(ValueError):
            util.entropy([-1, 1])

        with self.assertRaises(ValueError):
            util.entropy([-1, -1])

    def test_entropy(self):
        # Test that the function returns the correct entropy.
        self.assertAlmostEqual(util.entropy([1]), 0.0)
        self.assertAlmostEqual(util.entropy([1, 2]), 0.9182958340544896)
        self.assertAlmostEqual(util.entropy([1, 1]), 1.0)
        self.assertAlmostEqual(util.entropy([1, 2, 3]), 1.4591479170272448)
        self.assertAlmostEqual(util.entropy([1, 1, 1, 1]), 2.0)
