"""Password strength evaluation utilities."""

from __future__ import annotations

import math
import string
from dataclasses import dataclass
from enum import IntEnum


class StrengthLevel(IntEnum):
    """Strength categories from weak to strong."""

    VERY_WEAK = 0
    WEAK = 1
    MEDIUM = 2
    STRONG = 3
    VERY_STRONG = 4


@dataclass(slots=True)
class StrengthResult:
    """Strength evaluation output.

    Attributes
    ----------
    level : StrengthLevel
        Categorized security level.
    score : int
        Normalized score in range [0, 100].
    entropy_bits : float
        Shannon entropy estimate in bits.
    feedback : list[str]
        Human-readable recommendations.
    """

    level: StrengthLevel
    score: int
    entropy_bits: float
    feedback: list[str]

    def label(self) -> str:
        """Return a user-friendly strength label.

        Returns
        -------
        str
            Readable label derived from enum level.
        """

        return self.level.name.replace("_", " ").title()

    def crack_seconds(self, attempts_per_second: int) -> float:
        """Estimate seconds to brute-force at given attack rate.

        Parameters
        ----------
        attempts_per_second : int
            Number of guesses per second the attacker can perform.

        Returns
        -------
        float
            Expected seconds to exhaust the search space.
        """

        if attempts_per_second <= 0:
            return float("inf")
        return float(2.0**self.entropy_bits) / attempts_per_second


class PasswordStrengthEvaluator:
    """Estimate password strength from entropy and composition heuristics."""

    def evaluate_many(self, passwords: list[str]) -> list[StrengthResult]:
        """Evaluate multiple passwords in one call.

        Parameters
        ----------
        passwords : list[str]
            Passwords to evaluate.

        Returns
        -------
        list[StrengthResult]
            Strength results preserving input order.
        """

        return [self.evaluate(password) for password in passwords]

    def evaluate(self, password: str) -> StrengthResult:
        """Evaluate a password.

        Parameters
        ----------
        password : str
            Password to evaluate.

        Returns
        -------
        StrengthResult
            Computed strength classification and suggestions.
        """

        if not password:
            return StrengthResult(
                level=StrengthLevel.VERY_WEAK,
                score=0,
                entropy_bits=0.0,
                feedback=["La contrasena esta vacia."],
            )

        pool_size = self._pool_size(password)
        entropy = len(password) * math.log2(max(2, pool_size))
        score = min(100, max(0, int(entropy * 1.6)))

        feedback: list[str] = []
        if len(password) < 12:
            feedback.append("Usa al menos 12 caracteres.")
        if password.lower() == password or password.upper() == password:
            feedback.append("Mezcla mayusculas y minusculas.")
        if not any(char.isdigit() for char in password):
            feedback.append("Incluye al menos un numero.")
        if not any(char in string.punctuation for char in password):
            feedback.append("Incluye simbolos para mayor entropia.")

        level = self._score_to_level(score)
        if not feedback:
            feedback.append("Contrasena robusta.")

        return StrengthResult(
            level=level, score=score, entropy_bits=entropy, feedback=feedback
        )

    @staticmethod
    def _pool_size(password: str) -> int:
        """Estimate effective character pool size.

        Parameters
        ----------
        password : str
            Password under analysis.

        Returns
        -------
        int
            Estimated search-space alphabet size.
        """

        pool = 0
        if any(char.islower() for char in password):
            pool += 26
        if any(char.isupper() for char in password):
            pool += 26
        if any(char.isdigit() for char in password):
            pool += 10
        if any(char in string.punctuation for char in password):
            pool += len(string.punctuation)
        if pool == 0:
            return 1
        return pool

    @staticmethod
    def _score_to_level(score: int) -> StrengthLevel:
        """Map score to a discrete strength level.

        Parameters
        ----------
        score : int
            Value in range [0, 100].

        Returns
        -------
        StrengthLevel
            Corresponding category.
        """

        if score < 25:
            return StrengthLevel.VERY_WEAK
        if score < 45:
            return StrengthLevel.WEAK
        if score < 65:
            return StrengthLevel.MEDIUM
        if score < 85:
            return StrengthLevel.STRONG
        return StrengthLevel.VERY_STRONG
