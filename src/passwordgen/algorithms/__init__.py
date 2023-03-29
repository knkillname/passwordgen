"""Password generators algorithms.

This package contains the algorithms used to generate passwords.

Classes
-------
RandomString
    Generate a password using a random string.
XKCDGenerator
    Generate a password using the XKCD method.
"""
from .abc import PasswordGeneratorBase
from .randomstring import RandomString
from .xkcd import XKCDGenerator
