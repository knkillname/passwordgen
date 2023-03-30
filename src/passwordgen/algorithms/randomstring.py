"""Class for generating random strings of characters.

This module contains the RandomString class for generating random
strings of characters.

Classes
-------
RandomString
    Generate a random string of characters.
"""
import math
import string
from random import SystemRandom

from .abc import PasswordGeneratorBase


class RandomString(PasswordGeneratorBase):
    """Generate a random string of characters.

    This password generator generates a random string of characters
    from a set of characters that can be configured. The default
    character set is all ASCII letters and digits, but no punctuation.

    Attributes
    ----------
    use_uppercase : bool
        Whether to use uppercase letters.
    use_lowercase : bool
        Whether to use lowercase letters.
    use_digits : bool
        Whether to use digits.
    use_punctuation : bool
        Whether to use punctuation.
    other_characters : str
        Additional characters to use.

    Methods
    -------
    generate_password(strength: int) -> str
        Generate a password of the given strength.

    generate_many_passwords(strength: int, count: int) -> list[str]
        Generate a list of passwords of the given strength.
    """

    name = "Random String"
    description = "Generate a random string of characters."

    def __init__(
        self,
        use_uppercase: bool = True,
        use_lowercase: bool = True,
        use_digits: bool = True,
        use_punctuation: bool = False,
        other_characters: str = "",
    ):
        """Initialize the password generator.

        Arguments
        ---------
        use_uppercase : bool
            Whether to use uppercase letters.
        use_lowercase : bool
            Whether to use lowercase letters.
        use_digits : bool
            Whether to use digits.
        use_punctuation : bool
            Whether to use punctuation.
        other_characters : str
            Additional characters to use.

        Raises
        ------
        ValueError
            If no characters are selected.
        """
        self._random = SystemRandom()
        self._init_attributes_phase = True
        self.use_uppercase = use_uppercase
        self.use_lowercase = use_lowercase
        self.use_digits = use_digits
        self.use_punctuation = use_punctuation
        self.other_characters = other_characters
        self._init_attributes_phase = False
        self._update_character_set()

    def generate_password(
        self, *, strength: int | None = None, length: int | None = None
    ) -> str:
        """Generate a password of the given strength or length.

        Arguments
        ---------
        strength : int
            The strength of the password measured in bits consumed by
            the random number generator to create it. The default is 42.
        length : int
            The length of the password. The default is None.

        Returns
        -------
        str
            The generated password.

        Raises
        ------
        ValueError
            If both strength and length are given.
        """
        # Check that either strength or length is given.
        if strength is None and length is None:
            strength = 42
        elif strength is not None and length is not None:
            raise ValueError("Cannot specify both strength and length")

        # Calculate the length of the password if it is not given.
        if length is None:
            assert strength is not None
            length = math.ceil(strength / self._character_entropy)

        # Generate the password of the given length.
        return "".join(self._random.choices(self._character_set, k=length))

    @property
    def use_uppercase(self) -> bool:
        """Whether to use uppercase letters."""
        return self._use_uppercase

    @use_uppercase.setter
    def use_uppercase(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(f"Expected bool, got {type(value)}")
        self._use_uppercase = value
        self._update_character_set()

    @property
    def use_lowercase(self) -> bool:
        """Whether to use lowercase letters."""
        return self._use_lowercase

    @use_lowercase.setter
    def use_lowercase(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(f"Expected bool, got {type(value)}")
        self._use_lowercase = value
        self._update_character_set()

    @property
    def use_digits(self) -> bool:
        """Whether to use digits."""
        return self._use_digits

    @use_digits.setter
    def use_digits(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(f"Expected bool, got {type(value)}")
        self._use_digits = value
        self._update_character_set()

    @property
    def use_punctuation(self) -> bool:
        """Whether to use punctuation."""
        return self._use_punctuation

    @use_punctuation.setter
    def use_punctuation(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(f"Expected bool, got {type(value)}")
        self._use_punctuation = value
        self._update_character_set()

    @property
    def other_characters(self) -> str:
        """Additional characters to use."""
        return self._other_characters

    @other_characters.setter
    def other_characters(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"Expected str, got {type(value)}")
        self._other_characters = value
        self._update_character_set()

    def _update_character_set(self) -> None:
        """Update the character set and entropy per character."""
        if self._init_attributes_phase:
            return
        result: list[str] = []
        if self._use_uppercase:
            result += string.ascii_uppercase
        if self._use_lowercase:
            result += string.ascii_lowercase
        if self._use_digits:
            result += string.digits
        if self._use_punctuation:
            result += string.punctuation
        result += self._other_characters

        result = list(dict.fromkeys(result))  # Remove duplicates.

        if not result:
            raise ValueError("No characters to choose from.")

        self._character_set = result
        self._character_entropy = math.log2(len(self._character_set))
