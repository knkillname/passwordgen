"""Utility functions and data classes.

This module contains utility functions and data classes that are used
throughout the package.
"""
import dataclasses
import math
from collections.abc import Collection


@dataclasses.dataclass
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
    """

    years: int
    days: int
    hours: int
    minutes: int
    seconds: int

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


def entropy(probability: Collection[float] | Collection[int]) -> float:
    """Calculate the entropy of a set of probabilities.

    Arguments
    ---------
    probability : Collection[float] | Collection[int]
        The probabilities. The probabilities do not need to sum to 1 and
        can be integers. The probabilities will be normalized before
        calculating the entropy.

    Returns
    -------
    float
        The entropy of the probabilities.
    """
    # Normalize p so that it sums to 1.
    total = math.fsum(probability)
    probability = [p / total for p in probability]

    return -sum(p * math.log2(p) for p in probability)
