"""Containers for passwordgen."""
from typing import NamedTuple


class Password(NamedTuple):
    """Class to hold a password and its strength.

    Attributes
    ----------
    password : str
        The password string.
    strength : int
        The strength of the password measured in bits needed to
        generate it using the same algorithm.
    """

    password: str
    strength: int
