"""Module to generate random password strings.

Classes
-------
RandomStringGenerator
    Class to generate random password strings.
"""
import math
from random import SystemRandom
import string
import unicodedata

from .base import BasePasswordGenerator
from ..containers import Password

_UNICODE_RANGE = range(0x00A0, 0x10FFFF + 1)


class RandomStringGenerator(BasePasswordGenerator):
    """Class to generate random password strings.

    This class generates random password strings. The characters used
    in the password can be configured using the properties of the
    class.

    Attributes
    ----------
    use_digits : bool
        Whether to use digits in the password.
    use_punctuation : bool
        Whether to use punctuation in the password.
    use_uppercase : bool
        Whether to use uppercase letters in the password.
    use_lowercase : bool
        Whether to use lowercase letters in the password.
    use_unicode : bool
        Whether to use Unicode characters in the password.
    """

    name = "Random String"
    description = "Generates a random string of characters and symbols."

    def __init__(
        self,
        use_digits: bool = True,
        use_punctuation: bool = False,
        use_uppercase: bool = True,
        use_lowercase: bool = True,
        use_unicode: bool = False,
    ):
        """Initialize the generator.

        Parameters
        ----------
        use_digits : bool, optional
            Whether to use digits in the password, by default True
        use_punctuation : bool, optional
            Whether to use punctuation in the password, by default False
        use_uppercase : bool, optional
            Whether to use uppercase letters in the password, by default True
        use_lowercase : bool, optional
            Whether to use lowercase letters in the password, by default True
        use_unicode : bool, optional
            Whether to use Unicode characters in the password, by default False
        """
        self._use_digits = bool(use_digits)
        self._use_punctuation = bool(use_punctuation)
        self._use_uppercase = bool(use_uppercase)
        self._use_lowercase = bool(use_lowercase)
        self._use_unicode = bool(use_unicode)
        self._random = SystemRandom()
        self._update_charset()

    @property
    def use_digits(self) -> bool:
        """Whether to use digits in the password."""
        return self._use_digits

    @use_digits.setter
    def use_digits(self, value: bool):
        self._use_digits = bool(value)
        self._update_charset()

    @property
    def use_punctuation(self) -> bool:
        """Whether to use punctuation in the password."""
        return self._use_punctuation

    @use_punctuation.setter
    def use_punctuation(self, value: bool):
        self._use_punctuation = bool(value)
        self._update_charset()

    @property
    def use_uppercase(self) -> bool:
        """Whether to use uppercase letters in the password."""
        return self._use_uppercase

    @use_uppercase.setter
    def use_uppercase(self, value: bool):
        self._use_uppercase = bool(value)
        self._update_charset()

    @property
    def use_lowercase(self) -> bool:
        """Whether to use lowercase letters in the password."""
        return self._use_lowercase

    @use_lowercase.setter
    def use_lowercase(self, value: bool):
        self._use_lowercase = bool(value)
        self._update_charset()

    def generate(self, length: int) -> Password:
        """Generate a password of the given length.

        Parameters
        ----------
        length : int
            The length of the password to generate.

        Returns
        -------
        Password
            The generated password.
        """
        choice = self._random.choice
        password_str = "".join(choice(self._charset) for _ in range(length))
        strength = int(length * math.log2(len(self._charset)))
        return Password(password_str, strength)

    def _update_charset(self):
        self._charset = []
        if self._use_digits:
            self._charset.extend(string.digits)
        if self._use_punctuation:
            self._charset.extend(string.punctuation)
        if self._use_uppercase:
            if not self._use_unicode:
                # ASCII uppercase letters
                self._charset.extend(string.ascii_uppercase)
            else:
                # Unicode uppercase letters
                self._charset.extend(
                    chr(c)
                    for c in _UNICODE_RANGE
                    if unicodedata.category(chr(c)) == "Lu"
                )

        if self._use_lowercase:
            if not self._use_unicode:
                # ASCII lowercase letters
                self._charset.extend(string.ascii_lowercase)
            else:
                # Unicode lowercase letters
                self._charset.extend(
                    chr(c)
                    for c in _UNICODE_RANGE
                    if unicodedata.category(chr(c)) == "Ll"
                )
