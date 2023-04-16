"""Common functions used by the password generator."""
import math
from collections.abc import Iterable
from pathlib import Path
from typing import SupportsFloat, cast

__all__ = ["entropy", "get_resource_path", "normalize_time"]


def entropy(probability: Iterable[SupportsFloat]) -> float:
    """Calculate the entropy of a set of probabilities.

    Arguments
    ---------
    probability : Iterable[SupportsFloat]
        The probabilities. The probabilities do not need to sum to 1 and
        can be integers; they will be normalized before calculating the entropy.
    Returns
    -------
    float
        The entropy of the probabilities.
    Raises
    ------
    TypeError
        If the probabilities are not an iterable.
    ValueError
        If the probabilities are negative or all zero.
    """
    # Check arguments.
    if not isinstance(probability, Iterable):
        raise TypeError(f"Expected a iterable, got {type(probability)}")
    probability = cast(list[float], [float(p) for p in probability])
    if any(p < 0 for p in probability) or all(p == 0.0 for p in probability):
        raise ValueError("Probabilities must be non-negative and not all zero")

    # Normalize p so that it sums to 1.
    total = math.fsum(probability)
    probability = [p / total for p in probability]
    assert isinstance(probability, list)
    return -math.fsum(p * math.log2(p) for p in probability)


def get_resource_path(path: str) -> Path:
    """Get the path to a resource file or subdirectory.

    Parameters
    ----------
    path : str
        The path to the resource file or subdirectory, relative to the
        root of the repository. The path should use Unix-style path
        separators; i.e. forward slashes.

    Returns
    -------
    Path
        The path to the resource file or subdirectory.
    """
    return Path(__file__).parent.parent / "data" / path


def normalize_time(
    years: int | float,
    days: int | float,
    hours: int | float,
    minutes: int | float,
    seconds: int | float,
) -> tuple[int, int, int, int, int]:
    """Normalize a time.

    Arguments
    ---------
    years : int | float
        The number of years.
    days : int | float
        The number of days.
    hours : int | float
        The number of hours.
    minutes : int | float
        The number of minutes.
    seconds : int | float
        The number of seconds.

    Returns
    -------
    tuple[int, int, int, int, int]
        The normalised time.
    """
    # Propagate year fractions to days.
    years, aux = divmod(years, 1)
    days += aux * 365.2422

    # Propagate day fractions to hours.
    days, aux = divmod(days, 1)
    hours += aux * 24

    # Propagate hour fractions to minutes.
    hours, aux = divmod(hours, 1)
    minutes += aux * 60

    # Propagate minute fractions to seconds.
    minutes, aux = divmod(minutes, 1)
    seconds += aux * 60

    # Normalize seconds.
    aux, seconds = divmod(seconds, 60)
    minutes += aux

    # Normalize minutes.
    aux, minutes = divmod(minutes, 60)
    hours += aux

    # Normalize hours.
    aux, hours = divmod(hours, 24)
    days += aux

    # Normalize days.
    aux, days = divmod(days, 365.2422)
    years += aux

    # Convert to integers and return.
    return int(years), int(days), int(hours), int(minutes), int(seconds)
