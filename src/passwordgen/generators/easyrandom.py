"""Easy to memorize password generator.

Classes
-------
EasyRandomPasswordGenerator
    Generate a password that is easy to memorize.
"""

import itertools
import math
from collections.abc import Sequence
from random import SystemRandom

from ..common import Password
from .abc import PasswordGeneratorBase


class EasyRandomPasswordGenerator(PasswordGeneratorBase):
    """Easy to memorize password generator.

    This generator generates passwords that are easy to memorize by
    mixing words from a dictionary with numbers and special characters.

    Properties
    ----------
    length : int
        The length of the generated password.
    dictionary : list[str]
        The list of words to use for generating passwords.
    filler_characters : str
        The characters to use for filling in the gaps between words.
    max_filler_ratio : float
        The maximum ratio of filler characters to words. Must be between
        0 and 1, where 0 means no filler characters will be allowed in
        the resulting password and 1 means that the password can be
        filled with filler characters. Defaults to 1/3.

    Methods
    -------
    generate()
        Generate a password.
    generate_many(n)
        Generate many passwords.
    """

    # pylint: disable=too-many-instance-attributes
    # We need a lot of attributes for this class because it has
    # properties, and we need to store the values of the properties
    # somewhere.

    description = "Easy to memorize password generator"
    name = "Easy random"

    def __init__(
        self,
        length: int = 16,
        *,
        dictionary: Sequence[str],
        filler_characters: str = "!@#$%^&*()[]{}_+-=0123456789",
        max_filler_ratio: float = 1 / 3,
    ):
        """Initialize the generator.

        Parameters
        ----------
        length : int, optional
            The length of the generated password, by default 16
        dictionary : Sequence[str], keyword-only
            The list of words to use for generating passwords.
        filler_characters : str, optional, keyword-only
            The characters to use for filling in the gaps between words,
            by default "!@#$%^&*()[]{}_+-=0123456789". Must not be
            empty.

        Raises
        ------
        TypeError
            If length is not an integer.
        ValueError
            If length is less than 1.
        TypeError
            If dictionary is not a list of strings.
        ValueError
            If dictionary is empty.
        TypeError
            If filler_characters is not a string.
        ValueError
            If filler_characters is empty.
        """
        self._length: int
        self._dictionary: Sequence[str]
        self._filler_characters: str
        self._max_filler_ratio: float

        self.length = length
        self.dictionary = dictionary
        self.filler_characters = filler_characters
        self.max_filler_ratio = max_filler_ratio

    @property
    def length(self) -> int:
        """The length of the generated password."""
        return self._length

    @length.setter
    def length(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Length must be an integer")
        if value < 1:
            raise ValueError("Length must be greater than 0")
        self._length = value

    @property
    def dictionary(self) -> Sequence[str]:
        """The list of words to use for generating passwords."""
        return self._dictionary

    @dictionary.setter
    def dictionary(self, value: Sequence[str]) -> None:
        if not isinstance(value, Sequence):
            raise TypeError("Dictionary must be a sequence")
        if isinstance(value, str):
            raise TypeError("Dictionary cannot be a single str.")
        if not all(isinstance(word, str) for word in value):
            raise TypeError("Dictionary must be a sequence of strings")
        if not value:
            raise ValueError("Dictionary must not be empty")
        self._dictionary = value

    @property
    def filler_characters(self) -> str:
        """The characters to use for filling in the gaps between words."""
        return self._filler_characters

    @filler_characters.setter
    def filler_characters(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Filler characters must be a string")
        if not value:
            raise ValueError("Filler characters must not be empty")
        self._filler_characters = value

    @property
    def max_filler_ratio(self) -> float:
        """The maximum ratio of filler characters to words."""
        return self._max_filler_ratio

    @max_filler_ratio.setter
    def max_filler_ratio(self, value: float) -> None:
        if not isinstance(value, float):
            raise TypeError("Max filler ratio must be a float")
        if not 0 <= value <= 1:
            raise ValueError("Max filler ratio must be between 0 and 1")
        self._max_filler_ratio = value

    def generate_password(self) -> Password:
        """Generate a password.

        Returns
        -------
        Password
            The generated password.
        """
        random = SystemRandom()
        # Remove words that are too long
        dictionary = [word for word in self.dictionary if len(word) < self.length]
        fillers = list(self.filler_characters)

        # Select words until the password is long enough:
        selected_words: list[str] = []
        length = 0
        while True:
            word = random.choice(dictionary)
            if length + len(word) >= self.length:
                break
            selected_words.append(word)
            length += len(word) + 1  # +1 for at least 1 filler character

        # Add at least one filler character between each word and at the
        # end:
        buckets: list[list[str]] = [
            [random.choice(fillers)] for _ in range(len(selected_words))
        ]

        # Add the remaining filler characters to the buckets until the
        # password is long enough:
        while length < self.length:
            bucket = random.choice(buckets)
            bucket.append(random.choice(fillers))
            length += 1

        # Create the password string by mixing the words and the buckets:
        joints = ("".join(bucket) for bucket in buckets)
        password = "".join(itertools.chain(*zip(selected_words, joints)))

        # Compute the password strength:
        entropy = self._compute_entropy(dictionary, fillers, selected_words, buckets)

        return Password(password, entropy)

    def _compute_entropy(self, dictionary, fillers, selected_words, buckets):
        word_entropy = math.log2(len(dictionary))
        filler_entropy = math.log2(len(fillers))
        words_length = sum(len(word) for word in selected_words)
        extra_filler_positions = self.length - words_length - len(selected_words)
        arrangements = math.comb(
            len(buckets) - 1, extra_filler_positions + len(buckets) - 1
        )
        return (
            len(selected_words) * word_entropy
            + (self.length - words_length) * filler_entropy
            + (math.log2(arrangements) if arrangements > 0 else 0)
        )
