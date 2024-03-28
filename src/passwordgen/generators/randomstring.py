"""Module for the RandomStringPasswordGenerator class.

Classes
-------
RandomStringPasswordGenerator
    Generate a random string of characters.
"""

import math
import string
from random import SystemRandom

from ..common.classes import Password
from .abc import PasswordGeneratorBase


class RandomStringPasswordGenerator(PasswordGeneratorBase):
    """Generate a random string of characters.

    Attributes
    ----------
    name : str
        The name of the password generator.
    description : str
        The description of the password generator.
    length : int
        The length of the password.
    use_uppercase : bool
        Whether to use uppercase letters in the password.
    use_lowercase : bool
        Whether to use lowercase letters in the password.
    use_digits : bool
        Whether to use digits in the password.
    use_punctuation : bool
        Whether to use punctuation characters in the password.
    other_characters : str
        Characters to include in the password. These characters will be
        included in the password even if the corresponding use_* option
        is False.

    Methods
    -------
    generate_password()
        Generate a password.
    generate_many_passwords(count)
        Generate many passwords.
    """

    # pylint: disable=too-many-instance-attributes
    # We use private attributes to store the values of the public
    # attributes. This is to allow us to validate the values of the
    # public attributes when they are set.

    name = "Random String"
    description = "Generate a random string of characters."

    def __init__(
        self,
        length: int = 8,
        *,
        use_uppercase: bool = True,
        use_lowercase: bool = True,
        use_digits: bool = True,
        use_punctuation: bool = True,
        other_characters: str = "",
    ):
        """Initialize the password generator.

        Parameters
        ----------
        length : int, optional
            The length of the password, by default 8
        use_uppercase : bool, optional, keyword-only
            Whether to use uppercase letters in the password, by default
            True.
        use_lowercase : bool, optional, keyword-only
            Whether to use lowercase letters in the password, by default
            True.
        use_digits : bool, optional, keyword-only
            Whether to use digits in the password, by default True.
        use_punctuation : bool, optional, keyword-only
            Whether to use punctuation characters in the password, by
            default True.
        other_characters : str, optional, keyword-only
            Characters to include in the password, by default "". These
            characters will be included in the password even if the
            corresponding use_* option is False.

        Raises
        ------
        TypeError
            If any of the arguments are not of the correct type.
        ValueError
            If the length is negative.
        """
        self._charset: list[str]
        self._length: int
        self._use_uppercase: bool
        self._use_lowercase: bool
        self._use_digits: bool
        self._use_punctuation: bool
        self._other_characters: str
        self._random: SystemRandom

        self.length = length
        self.use_uppercase = use_uppercase
        self.use_lowercase = use_lowercase
        self.use_digits = use_digits
        self.use_punctuation = use_punctuation
        self.other_characters = other_characters
        self._random = SystemRandom()

    @property
    def length(self) -> int:
        """The length of the password."""
        return self._length

    @length.setter
    def length(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"Expected int, got {type(value)}")
        if value < 0:
            raise ValueError(f"Expected non-negative int, got {value}")
        self._length = value

    @property
    def use_uppercase(self) -> bool:
        """Whether to use uppercase letters in the password."""
        return self._use_uppercase

    @use_uppercase.setter
    def use_uppercase(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(f"Expected bool, got {type(value)}")
        self._use_uppercase = value

    @property
    def use_lowercase(self) -> bool:
        """Whether to use lowercase letters in the password."""
        return self._use_lowercase

    @use_lowercase.setter
    def use_lowercase(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(f"Expected bool, got {type(value)}")
        self._use_lowercase = value

    @property
    def use_digits(self) -> bool:
        """Whether to use digits in the password."""
        return self._use_digits

    @use_digits.setter
    def use_digits(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(f"Expected bool, got {type(value)}")
        self._use_digits = value

    @property
    def use_punctuation(self) -> bool:
        """Whether to use punctuation characters in the password."""
        return self._use_punctuation

    @use_punctuation.setter
    def use_punctuation(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(f"Expected bool, got {type(value)}")
        self._use_punctuation = value

    @property
    def other_characters(self) -> str:
        """Characters to include in the password."""
        return self._other_characters

    @other_characters.setter
    def other_characters(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"Expected str, got {type(value)}")
        self._other_characters = value

    def _update_charset(self) -> None:
        """Update the character set."""
        self._charset = []
        if self.use_uppercase:
            self._charset.extend(string.ascii_uppercase)
        if self.use_lowercase:
            self._charset.extend(string.ascii_lowercase)
        if self.use_digits:
            self._charset.extend(string.digits)
        if self.use_punctuation:
            self._charset.extend(string.punctuation)
        self._charset.extend(self.other_characters)

        # Remove duplicates
        self._charset = list(dict.fromkeys(self._charset))

    def generate_password(self) -> Password:
        """Generate a password.

        Returns
        -------
        Password
            A password and its strength.
        """
        self._update_charset()
        entropy_per_char = math.log2(len(self._charset))
        strength = self.length * entropy_per_char
        password = "".join(self._random.choices(self._charset, k=self.length))
        return Password(password, strength)
