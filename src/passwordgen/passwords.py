"""Classes for passwords and durations of time."""
import collections
import functools
from typing import NamedTuple

from . import util


class Password(NamedTuple):
    """A password and its strength.

    Attributes
    ----------
    password : str
        The password.
    strength : int
        The strength of the password measured in the minimum number of
        bits that need to be consumed by a random number generator to
        create it.
    """

    password: str
    strength: float

    @functools.cached_property
    def entropy(self) -> float:
        """Calculate the entropy of the password.

        This is the number of bits of information that the password
        contains and can be used to calculate the time to crack the
        password with a brute force attack and no knowledge of the
        password generation algorithm.

        Returns
        -------
        float
            The entropy of the password.
        """
        weights = list(collections.Counter(self.password).values())
        return util.entropy(weights)

    def time_to_crack(
        self, guesses_per_second: int, brute_force=False
    ) -> util.Duration:
        """Calculate the time to crack the password.

        Arguments
        ---------
        guesses_per_second : int
            The number of guesses that can be made per second.
        brute_force : bool, optional
            If True, the time to crack the password with a brute force
            attack is calculated. If False, the time to crack the
            password with a dictionary attack is calculated. The
            default is False.

        Returns
        -------
        Duration
            The time to crack the password.
        """
        if brute_force:
            guesses = int(2**self.entropy)
        else:
            guesses = int(2 ** (self.strength - 1))
        seconds = guesses // guesses_per_second
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        years, days = divmod(days, 365)
        return util.Duration(years, days, hours, minutes, seconds)
