"""Common types used by the passwordgen package."""
import collections
from typing import NamedTuple

from . import util

__all__ = ["Password", "Duration"]


class Duration:
    """A duration of time."""

    def __init__(
        self,
        years: int | float = 0,
        days: int | float = 0,
        hours: int | float = 0,
        minutes: int | float = 0,
        seconds: int | float = 0,
    ):
        years, days, hours, minutes, seconds = util.normalize_time(
            years, days, hours, minutes, seconds
        )

        self._years = years
        self._days = days
        self._hours = hours
        self._minutes = minutes
        self._seconds = seconds

    @property
    def years(self) -> int:
        """Get the number of years."""
        return self._years

    @property
    def days(self) -> int:
        """Get the number of days."""
        return self._days

    @property
    def hours(self) -> int:
        """Get the number of hours."""
        return self._hours

    @property
    def minutes(self) -> int:
        """Get the number of minutes."""
        return self._minutes

    @property
    def seconds(self) -> int:
        """Get the number of seconds."""
        return self._seconds

    def total_seconds(self) -> float:
        """Get the total number of seconds."""
        return (
            self.years * 365.2422 * 24 * 60 * 60
            + self.days * 24 * 60 * 60
            + self.hours * 60 * 60
            + self.minutes * 60
            + self.seconds
        )

    def describe(self) -> str:
        """Describe the duration in plain english.

        Duration is described in the largest unit possible. For example,
        1 year is described as "1 year" and 1 day is described as "1
        day". 1 minute is described as "1 minute" and 1 second is
        described as "1 second". Less than a second is described as
        "Less than a second".
        """
        if self.years >= 1000000:
            millions_of_years = self.years // 1000000
            return "{n} million years".format(n=millions_of_years)
        elif self.years >= 1000:
            thousands_of_years = self.years // 1000
            return "{n} thousand years".format(n=thousands_of_years)
        elif self.years > 1:
            return "{n} years".format(n=self.years)
        elif self.years == 1:
            return "1 year"
        elif self.days > 1:
            return "{n} days".format(n=self.days)
        elif self.days == 1:
            return "1 day"
        elif self.hours > 1:
            return "{n} hours".format(n=self.hours)
        elif self.hours == 1:
            return "1 hour"
        elif self.minutes > 1:
            return "{n} minutes".format(n=self.minutes)
        elif self.minutes == 1:
            return "1 minute"
        elif self.seconds > 1:
            return "{n} seconds".format(n=self.seconds)
        elif self.seconds == 1:
            return "1 second"
        else:
            return "Less than a second"


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

    Methods
    -------
    entropy()
        Calculate the entropy of the password.
    time_to_crack(guesses_per_second, brute_force=False)
        Calculate the time to crack the password.
    """

    password: str
    strength: float

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

    def time_to_crack(self, guesses_per_second: int, brute_force=False) -> Duration:
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
            guesses = int(2 ** self.entropy())
        else:
            guesses = int(2 ** (self.strength - 1))
        seconds = guesses // guesses_per_second
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        years, days = divmod(days, 365)
        return Duration(years, days, hours, minutes, seconds)
