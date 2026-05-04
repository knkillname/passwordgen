"""Unit tests for strength evaluator."""

from __future__ import annotations

import math
import unittest

from passwordgen.gui.results_frame import _format_crack_time
from passwordgen.strength import PasswordStrengthEvaluator, StrengthLevel


class TestStrengthEvaluator(unittest.TestCase):
    """Validate scoring and classification."""

    def setUp(self) -> None:
        self.evaluator = PasswordStrengthEvaluator()

    def test_empty_password_is_very_weak(self) -> None:
        """Empty input yields minimum score."""

        result = self.evaluator.evaluate("")
        self.assertEqual(result.level, StrengthLevel.VERY_WEAK)
        self.assertEqual(result.score, 0)

    def test_complex_password_is_high(self) -> None:
        """Complex long password reaches strong categories."""

        result = self.evaluator.evaluate("Aa9!Bb8@Cc7#Dd6$")
        self.assertIn(result.level, {StrengthLevel.STRONG, StrengthLevel.VERY_STRONG})

    def test_feedback_present_for_weak_password(self) -> None:
        """Weak password returns improvement hints."""

        result = self.evaluator.evaluate("abc")
        self.assertGreater(len(result.feedback), 0)

    def test_entropy_bits_empty_password(self) -> None:
        """Empty password yields zero entropy."""

        result = self.evaluator.evaluate("")
        self.assertEqual(result.entropy_bits, 0.0)

    def test_entropy_bits_positive_for_nonempty(self) -> None:
        """Non-empty password produces positive entropy."""

        result = self.evaluator.evaluate("abc123")
        self.assertGreater(result.entropy_bits, 0.0)

    def test_entropy_bits_grows_with_length(self) -> None:
        """Longer password of same character class has higher entropy."""

        short = self.evaluator.evaluate("abc")
        long_ = self.evaluator.evaluate("abcdefghij")
        self.assertGreater(long_.entropy_bits, short.entropy_bits)

    def test_crack_seconds_grows_with_entropy(self) -> None:
        """Higher entropy password takes more seconds to crack."""

        weak = self.evaluator.evaluate("ab")
        strong = self.evaluator.evaluate("Aa9!Bb8@Cc7#Dd6$")
        self.assertGreater(strong.crack_seconds(1000), weak.crack_seconds(1000))

    def test_crack_seconds_scales_with_speed(self) -> None:
        """Faster attacker reduces estimated crack time proportionally."""

        result = self.evaluator.evaluate("hello123")
        slow = result.crack_seconds(1000)
        fast = result.crack_seconds(1_000_000)
        self.assertAlmostEqual(slow / fast, 1000.0, places=5)

    def test_crack_seconds_zero_speed_returns_inf(self) -> None:
        """Zero attempts per second returns infinity."""

        result = self.evaluator.evaluate("hello")
        self.assertEqual(result.crack_seconds(0), float("inf"))

    def test_label_returns_string(self) -> None:
        """label() returns a non-empty string for every level."""

        result = self.evaluator.evaluate("hello")
        label = result.label()
        self.assertIsInstance(label, str)
        self.assertTrue(len(label) > 0)

    def test_evaluate_many_returns_list(self) -> None:
        """evaluate_many returns one result per input password."""

        results = self.evaluator.evaluate_many(["hello", "Aa9!Bb8@Cc7#Dd6$"])
        self.assertEqual(len(results), 2)


class TestFormatCrackTime(unittest.TestCase):
    """Validate human-readable crack time formatting."""

    def _assert_locale_value(self, actual: str, spanish: str, english: str) -> None:
        """Allow locale-dependent expected text in assertions."""

        self.assertIn(actual, {spanish, english})

    def test_seconds(self) -> None:
        """Small values display as seconds."""

        self._assert_locale_value(_format_crack_time(45), "45 segundos", "45 seconds")

    def test_minutes(self) -> None:
        """Values around a few minutes display minutes."""

        self._assert_locale_value(_format_crack_time(180), "3 minutos", "3 minutes")

    def test_hours(self) -> None:
        """Values around several hours display hours."""

        self._assert_locale_value(_format_crack_time(3 * 3600), "3 horas", "3 hours")

    def test_days(self) -> None:
        """Values around several days display days."""

        self._assert_locale_value(_format_crack_time(5 * 86400), "5 dias", "5 days")

    def test_weeks(self) -> None:
        """Values around several weeks display weeks."""

        self._assert_locale_value(
            _format_crack_time(3 * 7 * 86400),
            "3 semanas",
            "3 weeks",
        )

    def test_months(self) -> None:
        """Values around several months display months."""

        self._assert_locale_value(_format_crack_time(92 * 86400), "3 meses", "3 months")

    def test_years(self) -> None:
        """Values spanning years display years."""

        self._assert_locale_value(
            _format_crack_time(2 * 365 * 86400), "2 anos", "2 years"
        )

    def test_centuries(self) -> None:
        """Values spanning centuries display centuries."""

        self._assert_locale_value(
            _format_crack_time(120 * 365 * 86400), "1 siglo", "1 century"
        )

    def test_more_than_one_century_uses_plain_siglos(self) -> None:
        """Durations over one century omit the numeric count."""

        self._assert_locale_value(
            _format_crack_time(250 * 365 * 86400), "siglos", "centuries"
        )

    def test_largest_unit_only(self) -> None:
        """Formatter reports only the largest magnitude unit."""

        self._assert_locale_value(
            _format_crack_time((3 * 86400) + (2 * 3600) + 300),
            "3 dias",
            "3 days",
        )

    def test_infinity_returns_siglos(self) -> None:
        """Effectively infinite time returns 'siglos'."""

        self._assert_locale_value(
            _format_crack_time(float("inf")), "siglos", "centuries"
        )
        self._assert_locale_value(
            _format_crack_time(2.0**math.inf), "siglos", "centuries"
        )
