from __future__ import annotations

from datetime import date, datetime
import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from trazabilidad.weekly_report import (
    Activity,
    _grouped_hours,
    load_weekly_activities,
    period_bounds,
    week_bounds,
    work_type,
    write_weekly_pdf,
)


def _page(
    title: str,
    day: str,
    status: str = "Resuelto",
    category: str = "Operativo",
    module: str = "STO",
) -> dict:
    return {
        "properties": {
            "Titulo": {"type": "title", "title": [{"plain_text": title}]},
            "Date Reported": {"type": "date", "date": {"start": day}},
            "Status": {"type": "status", "status": {"name": status}},
            "Category": {"type": "select", "select": {"name": category}},
            "Modulo": {"type": "select", "select": {"name": module}},
            "Horas": {"type": "number", "number": 2.5},
        }
    }


class FakeClient:
    def __init__(self) -> None:
        self.last_filter: dict | None = None

    def retrieve_data_source(self, data_source_id: str) -> dict:
        return {
            "properties": {
                "Titulo": {"type": "title"},
                "Date Reported": {"type": "date"},
                "Status": {"type": "status"},
                "Category": {"type": "select"},
                "Modulo": {"type": "select"},
                "Descripcion": {"type": "rich_text"},
                "Horas": {"type": "number"},
            }
        }

    def query_data_source(self, data_source_id: str, **kwargs) -> list[dict]:
        self.last_filter = kwargs.get("query_filter")
        return [
            _page("Actividad", "2026-06-29T10:00:00-05:00"),
            _page("Fuera", "2026-06-22"),
            _page("Notion personal", "2026-06-30", category="Personal"),
            _page("Web personal", "2026-07-01", module="Personal"),
        ]


class WeeklyReportTests(unittest.TestCase):
    def test_week_bounds_use_monday_and_sunday(self) -> None:
        self.assertEqual(
            week_bounds(date(2026, 7, 1)),
            (date(2026, 6, 29), date(2026, 7, 5)),
        )

    def test_period_bounds_daily_is_single_day(self) -> None:
        self.assertEqual(
            period_bounds(date(2026, 7, 1), "diario"),
            (date(2026, 7, 1), date(2026, 7, 1)),
        )

    def test_loads_only_activities_inside_period(self) -> None:
        client = FakeClient()
        activities = load_weekly_activities(
            client,
            data_source_id="source",
            start=date(2026, 6, 29),
            end=date(2026, 7, 5),
        )
        self.assertEqual(len(activities), 3)
        self.assertEqual(activities[0].title, "Actividad")
        self.assertEqual(activities[0].hours, 2.5)
        self.assertIsInstance(activities[0].reported_on, date)
        self.assertNotIsInstance(activities[0].reported_on, datetime)
        self.assertIsNotNone(client.last_filter)

    def test_work_scope_excludes_personal_category(self) -> None:
        activities = load_weekly_activities(
            FakeClient(),
            data_source_id="source",
            start=date(2026, 6, 29),
            end=date(2026, 7, 5),
            scope="trabajo",
        )
        self.assertEqual([item.title for item in activities], ["Actividad"])

    def test_personal_scope_keeps_only_personal(self) -> None:
        activities = load_weekly_activities(
            FakeClient(),
            data_source_id="source",
            start=date(2026, 6, 29),
            end=date(2026, 7, 5),
            scope="personal",
        )
        self.assertEqual(
            [item.title for item in activities], ["Notion personal", "Web personal"]
        )

    def test_work_type_classification(self) -> None:
        meeting = Activity("Reunión: equipo", date(2026, 6, 29), "Resuelto", "MA-IA", "", 1)
        code = Activity("Fix", date(2026, 6, 29), "Cerrado", "MA-IA", "", 1)
        explicit = Activity("Refactor", date(2026, 6, 29), "Resuelto", "Desarrollo", "", 1)
        manual = Activity("Actas", date(2026, 6, 29), "Resuelto", "Operativo", "", 1)
        self.assertEqual(work_type(meeting), "Reuniones")
        self.assertEqual(work_type(code), "Desarrollo")
        self.assertEqual(work_type(explicit), "Desarrollo")
        self.assertEqual(work_type(manual), "Gestión")

    def test_grouped_hours_collapses_minor_entries(self) -> None:
        grouped = _grouped_hours(
            {"Reuniones": 14.0, "MA-IA": 6.0, "A": 0.5, "B": 0.4, "C": 0.3}
        )
        self.assertEqual(grouped[0], ("Reuniones", 14.0))
        self.assertEqual(grouped[1], ("MA-IA", 6.0))
        self.assertEqual(grouped[-1][0], "Otros")
        self.assertAlmostEqual(grouped[-1][1], 1.2)

    @unittest.skipUnless(importlib.util.find_spec("reportlab"), "requiere reportlab")
    def test_writes_pdf(self) -> None:
        activity = Activity(
            "Actividad",
            date(2026, 6, 29),
            "Resuelto",
            "Operativo",
            "STO",
            2.5,
        )
        with TemporaryDirectory() as directory:
            output = Path(directory) / "report.pdf"
            write_weekly_pdf(
                output,
                [activity],
                start=date(2026, 6, 29),
                end=date(2026, 7, 5),
                author="Andrés Ortega",
            )
            self.assertTrue(output.read_bytes().startswith(b"%PDF"))

    @unittest.skipUnless(importlib.util.find_spec("reportlab"), "requiere reportlab")
    def test_writes_daily_pdf(self) -> None:
        activity = Activity(
            "Actividad",
            date(2026, 7, 3),
            "Cerrado",
            "MA-IA",
            "STO",
            1.5,
        )
        with TemporaryDirectory() as directory:
            output = Path(directory) / "report.pdf"
            write_weekly_pdf(
                output,
                [activity],
                start=date(2026, 7, 3),
                end=date(2026, 7, 3),
                author="Andrés Ortega",
                period="diario",
            )
            self.assertTrue(output.read_bytes().startswith(b"%PDF"))


if __name__ == "__main__":
    unittest.main()
