from __future__ import annotations

import unittest

from trazabilidad.session import SessionDuration


class SessionDurationTests(unittest.TestCase):
    def test_calculates_minutes_and_hours_across_offsets(self) -> None:
        duration = SessionDuration.from_iso(
            "2026-06-28T21:00:00-05:00",
            "2026-06-28T23:30:00-05:00",
        )
        self.assertEqual(duration.seconds, 9000)
        self.assertEqual(duration.minutes, 150)
        self.assertEqual(duration.hours, 2.5)

    def test_rejects_naive_timestamps(self) -> None:
        with self.assertRaises(ValueError):
            SessionDuration.from_iso(
                "2026-06-28T21:00:00",
                "2026-06-28T22:00:00",
            )

    def test_rejects_negative_duration(self) -> None:
        with self.assertRaises(ValueError):
            SessionDuration.from_iso(
                "2026-06-28T22:00:00-05:00",
                "2026-06-28T21:00:00-05:00",
            )
