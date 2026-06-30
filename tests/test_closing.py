from __future__ import annotations

import copy
import unittest

from trazabilidad.closing import (
    ACTIVITY_SCHEMA,
    PROJECT_SCHEMA,
    ClosePayloadError,
    CloseTargets,
    SessionCloseService,
    validate_close_payload,
)
from trazabilidad.notion_client import NotionConnectionError


def payload() -> dict:
    return {
        "session": {
            "name": "auto_Notification",
            "start": "2026-06-28T23:30:27-05:00",
            "end": "2026-06-28T23:58:54-05:00",
            "session_date": "2026-06-28",
            "duration_minutes": 28,
            "hours": 0.47,
            "challenge": "Migrar el proyecto",
            "resolved": True,
            "summary": "Migración y grafo inicial.",
            "version": "V1.0",
            "git_tag": "V1.0",
            "git_commit": "35f78b625e1fecb8cda0624dbf067344f0dd61f7",
            "status": "Done",
            "scope": "Laboral",
            "repository": "https://github.com/Vermell11/auto_Notification",
        },
        "activities": [
            {
                "title": "Migración inicial",
                "category": "Documentación",
                "reported_at": "2026-06-28",
                "hours": 0.47,
                "description": "Git, Obsidian y reglas.",
                "status": "Done",
            }
        ],
        "markdown": "# Cierre V1.0",
    }


class FakeClient:
    def __init__(self) -> None:
        self.projects: list[dict] = []
        self.activities: list[dict] = []
        self.create_calls = 0
        self.fail_after_project_create = False
        self.verified = False

    def verify_connection(self) -> dict:
        self.verified = True
        return {"id": "bot"}

    def retrieve_data_source(self, data_source_id: str) -> dict:
        schema = PROJECT_SCHEMA if data_source_id == "projects" else ACTIVITY_SCHEMA
        properties = {name: {"type": kind} for name, kind in schema.items()}
        if data_source_id == "projects":
            properties["Estado"]["status"] = {"options": [{"name": "Done"}]}
            properties["Ámbito"]["select"] = {
                "options": [{"name": "Laboral"}, {"name": "Personal"}]
            }
        else:
            properties["Category"]["select"] = {
                "options": [{"name": "Documentación"}]
            }
            properties["Status"]["status"] = {"options": [{"name": "Done"}]}
        return {"properties": properties}

    def query_data_source(self, data_source_id: str) -> list[dict]:
        return list(self.projects if data_source_id == "projects" else self.activities)

    def create_data_source_page(
        self, *, data_source_id: str, properties: dict, markdown: str | None = None
    ) -> dict:
        self.create_calls += 1
        pages = self.projects if data_source_id == "projects" else self.activities
        page = {
            "id": f"{data_source_id}-{len(pages) + 1}",
            "url": f"https://notion.test/{data_source_id}-{len(pages) + 1}",
            "properties": _as_response_properties(properties),
        }
        pages.append(page)
        if data_source_id == "projects" and self.fail_after_project_create:
            self.fail_after_project_create = False
            raise NotionConnectionError("respuesta incierta")
        return page


def _as_response_properties(properties: dict) -> dict:
    result = copy.deepcopy(properties)
    for value in result.values():
        for kind in ("title", "rich_text"):
            for item in value.get(kind, []):
                item["plain_text"] = item.get("text", {}).get("content", "")
    return result


class SessionCloseServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = FakeClient()
        self.service = SessionCloseService(
            self.client, CloseTargets("projects", "activities")
        )

    def test_rejects_short_commit_hash(self) -> None:
        invalid = payload()
        invalid["session"]["git_commit"] = "35f78b6"
        with self.assertRaisesRegex(ClosePayloadError, "SHA completo"):
            validate_close_payload(invalid)

    def test_rejects_verbose_notion_summary(self) -> None:
        invalid = payload()
        invalid["session"]["summary"] = "detalle " * 121
        with self.assertRaisesRegex(ClosePayloadError, "máximo de 120 palabras"):
            validate_close_payload(invalid)

    def test_rejects_verbose_activity_description(self) -> None:
        invalid = payload()
        invalid["activities"][0]["description"] = "detalle " * 81
        with self.assertRaisesRegex(ClosePayloadError, "máximo de 80 palabras"):
            validate_close_payload(invalid)

    def test_dry_run_validates_without_writing(self) -> None:
        result = self.service.execute(payload(), dry_run=True)
        self.assertTrue(self.client.verified)
        self.assertEqual(result.status, "dry_run")
        self.assertEqual(result.session_action, "would_create")
        self.assertEqual(result.activities_planned, 1)
        self.assertEqual(self.client.create_calls, 0)

    def test_creates_session_and_related_activity(self) -> None:
        result = self.service.execute(payload())
        self.assertEqual(result.session_action, "created")
        self.assertEqual(result.activities_created, 1)
        self.assertEqual(len(self.client.projects), 1)
        relation = self.client.activities[0]["properties"]["Proyecto"]["relation"]
        self.assertEqual(relation, [{"id": result.session_page_id}])

    def test_second_run_reuses_session_and_activity(self) -> None:
        first = self.service.execute(payload())
        second = self.service.execute(payload())
        self.assertEqual(first.session_page_id, second.session_page_id)
        self.assertEqual(second.session_action, "existing")
        self.assertEqual(second.activities_created, 0)
        self.assertEqual(second.activities_existing, 1)
        self.assertEqual(len(self.client.projects), 1)
        self.assertEqual(len(self.client.activities), 1)

    def test_reconciles_uncertain_session_creation(self) -> None:
        self.client.fail_after_project_create = True
        result = self.service.execute(payload())
        self.assertEqual(result.session_action, "created")
        self.assertEqual(len(self.client.projects), 1)
        self.assertEqual(result.activities_created, 1)

    def test_rejects_incompatible_schema(self) -> None:
        self.client.retrieve_data_source = lambda _: {"properties": {}}
        with self.assertRaisesRegex(ClosePayloadError, "Esquema incompatible"):
            self.service.execute(payload(), dry_run=True)

    def test_rejects_unknown_activity_category_during_preflight(self) -> None:
        invalid = payload()
        invalid["activities"][0]["category"] = "No existe"
        with self.assertRaisesRegex(ClosePayloadError, "Category no admite"):
            self.service.execute(invalid, dry_run=True)


if __name__ == "__main__":
    unittest.main()
