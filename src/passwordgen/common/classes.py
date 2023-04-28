"""Common types used by the passwordgen package."""
import collections
import enum
from typing import NamedTuple

from . import util

__all__ = ["Password", "Duration", "CrackMethodEnum"]


class CrackMethodEnum(int, enum.Enum):
    """An enumeration of the methods used to crack a password."""

    BEST = enum.auto()
    DICTIONARY = enum.auto()
    BRUTE_FORCE = enum.auto()


class Duration:
    """A duration of time.

    Attributes
    ----------
    years : int
        The number of years.
    days : int
        The number of days.
    hours : int
        The number of hours.
    minutes : int
        The number of minutes.
    seconds : int
        The number of seconds.

    Methods
    -------
    total_seconds()
        Get the total number of seconds.
    describe()
        Describe the duration in a human-readable format.
    """

    def __init__(
        self,
        *,
        years: int | float = 0,
        days: int | float = 0,
        hours: int | float = 0,
        minutes: int | float = 0,
        seconds: int | float = 0,
    ):
        """Initialize the duration.

        Parameters
        ----------
        years : int | float, optional
            The number of years, by default 0
        days : int | float, optional
            The number of days, by default 0
        hours : int | float, optional
            The number of hours, by default 0
        minutes : int | float, optional
            The number of minutes, by default 0
        seconds : int | float, optional
            The number of seconds, by default 0
        """
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

        Returns
        -------
        str
            The description of the duration.
        """
        # pylint: disable=too-many-return-statements
        # Since the number of return statements is proportional to the
        # number of possible units of time, it is not possible to reduce
        # the number of return statements (or branches) without reducing
        # the number of possible units of time.

        if self.years >= 1000000:
            millions_of_years = self.years // 1000000
            return f"{millions_of_years} million years"
        if self.years >= 1000:
            thousands_of_years = self.years // 1000
            return f"{thousands_of_years} thousand years"
        if self.years > 1:
            return f"{self.years} years"
        if self.years == 1:
            return "1 year"
        if self.days > 1:
            return f"{self.days} days"
        if self.days == 1:
            return "1 day"
        if self.hours > 1:
            return f"{self.hours} hours"
        if self.hours == 1:
            return "1 hour"
        if self.minutes > 1:
            return f"{self.minutes} minutes"
        if self.minutes == 1:
            return "1 minute"
        if self.seconds > 1:
            return f"{self.seconds} seconds"
        if self.seconds == 1:
            return "1 second"
        return "Less than a second"


class Password(NamedTuple):
    """A password and its strength.

    Attributes
    ----------
    password : str
        The password.
    strength : int
        The strength of the password measured by the number of bits
        that need to be consumed by a random number generator to
        recreate it using the same algorithm.

    Methods
    -------
    entropy()
        Calculate the entropy of the password. This is the number of
        bits of information that the password contains assuming that the
        symbols contained in the password are known but not the password
        generation algorithm.
    time_to_crack(guesses_per_second, brute_force=False, method=CrackMethodEnum.BEST)
        Calculate the time to crack the password.
    """

    password: str
    strength: float

    def entropy(self) -> float:
        """Calculate the entropy of the password.

        This is the number of bits of information that the password
        contains assuming that the symbols contained in the password are
        known but not the password generation algorithm.

        Returns
        -------
        float
            The entropy of the password.
        """
        weights = list(collections.Counter(self.password).values())
        character_entropy = util.entropy(weights)
        return len(self.password) * character_entropy

    def time_to_crack(
        self, guesses_per_second: int, method: CrackMethodEnum = CrackMethodEnum.BEST
    ) -> Duration:
        """Calculate the time to crack the password.

        Arguments
        ---------
        guesses_per_second : int
            The number of guesses that can be made per second.
        method : CrackMethodEnum, optional
            The method to estimate the number of guesses needed to crack
            the password, by default BEST.

        Returns
        -------
        Duration
            The time to crack the password.
        """
        guesses = self.guesses_to_crack(method)
        seconds = guesses // guesses_per_second
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        years, days = divmod(days, 365)
        return Duration(
            years=years, days=days, hours=hours, minutes=minutes, seconds=seconds
        )

    def bits_to_crack(self, method: CrackMethodEnum) -> float:
        """Get the number of bits needed to crack the password."""
        if method == CrackMethodEnum.BRUTE_FORCE:
            return self.entropy()
        if method == CrackMethodEnum.DICTIONARY:
            return self.strength
        return min(self.entropy(), self.strength)

    def guesses_to_crack(self, method: CrackMethodEnum) -> int:
        """Get the number of guesses needed to crack the password."""
        bits = self.bits_to_crack(method)
        return int(2 ** (bits - 1))

    def __str__(self) -> str:
        """Get the string representation of the password."""
        password = self.password
        strength = int(min(self.strength, self.entropy()))
        time = self.time_to_crack(1000).describe()
        return f"{password} (strength: {strength} bits or {time})"
