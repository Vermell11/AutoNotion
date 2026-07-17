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
        "quality": {
            "offline_audit": "0 vulnerabilidades",
            "known_alerts": [],
            "online_validation": "no requerida",
        },
        "markdown": "# Cierre V1.0",
    }


class FakeClient:
    def __init__(self) -> None:
        self.projects: list[dict] = []
        self.activities: list[dict] = []
        self.create_calls = 0
        self.fail_after_project_create = False
        self.update_calls = 0
        self.append_calls = 0
        self.markdown: dict[str, str] = {}
        self.fail_after_append = False
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
        if data_source_id == "projects":
            self.markdown[page["id"]] = markdown or ""
        if data_source_id == "projects" and self.fail_after_project_create:
            self.fail_after_project_create = False
            raise NotionConnectionError("respuesta incierta")
        return page

    def update_page_properties(self, page_id: str, properties: dict) -> dict:
        self.update_calls += 1
        for page in self.projects:
            if page["id"] == page_id:
                page["properties"].update(_as_response_properties(properties))
                return page
        raise NotionConnectionError("page not found")

    def append_page_markdown(self, page_id: str, markdown: str) -> dict:
        self.append_calls += 1
        self.markdown[page_id] = "\n".join(
            filter(None, [self.markdown.get(page_id), markdown])
        )
        if self.fail_after_append:
            self.fail_after_append = False
            raise NotionConnectionError("respuesta incierta")
        return {"id": page_id}

    def retrieve_page_markdown(self, page_id: str) -> str:
        return self.markdown.get(page_id, "")


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

    def test_requires_separate_quality_evidence(self) -> None:
        invalid = payload()
        del invalid["quality"]
        with self.assertRaisesRegex(ClosePayloadError, "objeto quality"):
            validate_close_payload(invalid)

    def test_rejects_activities_out_of_chronological_order(self) -> None:
        invalid = payload()
        later = copy.deepcopy(invalid["activities"][0])
        later["title"] = "Actividad posterior"
        later["reported_at"] = "2026-06-28T23:59:00-05:00"
        invalid["activities"] = [later, invalid["activities"][0]]
        with self.assertRaisesRegex(ClosePayloadError, "orden cronológico estricto"):
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
        self.assertEqual(result.activity_pages[0].id, "activities-1")
        self.assertEqual(result.activity_pages[0].url, "https://notion.test/activities-1")

    def test_creates_activities_in_reported_order(self) -> None:
        ordered = payload()
        second = copy.deepcopy(ordered["activities"][0])
        second["title"] = "Actividad posterior"
        second["reported_at"] = "2026-06-28T23:59:00-05:00"
        ordered["activities"].append(second)

        self.service.execute(ordered)

        titles = [
            page["properties"]["Titulo"]["title"][0]["text"]["content"]
            for page in self.client.activities
        ]
        self.assertEqual(
            titles,
            [
                "auto_Notification V1.0 — Migración inicial",
                "auto_Notification V1.0 — Actividad posterior",
            ],
        )

    def test_second_run_reuses_project_and_activity(self) -> None:
        first = self.service.execute(payload())
        second = self.service.execute(payload())
        self.assertEqual(first.session_page_id, second.session_page_id)
        self.assertEqual(second.session_action, "existing")
        self.assertEqual(second.activities_created, 0)
        self.assertEqual(second.activities_existing, 1)
        self.assertEqual(len(self.client.projects), 1)
        self.assertEqual(len(self.client.activities), 1)

    def test_retry_reconciles_uncertain_session_log_without_duplicate(self) -> None:
        self.service.execute(payload())
        next_payload = payload()
        next_payload["session"].update(
            version="V1.1", git_tag="V1.1", git_commit="a" * 40
        )
        next_payload["activities"][0]["title"] = "Mejora"
        self.client.fail_after_append = True

        with self.assertRaises(NotionConnectionError):
            self.service.execute(next_payload)
        marker = f"trazabilidad:V1.1:{'a' * 40}"
        self.client.markdown["projects-1"] = self.client.markdown[
            "projects-1"
        ].replace(marker, f"\\<!-- {marker} --\\>")
        result = self.service.execute(next_payload)

        self.assertEqual(self.client.markdown[result.session_page_id].count(marker), 1)
        self.assertEqual(result.activities_existing, 1)

    def test_new_version_updates_same_project(self) -> None:
        first = self.service.execute(payload())
        next_payload = payload()
        next_payload["session"]["version"] = "V1.1"
        next_payload["session"]["git_tag"] = "V1.1"
        next_payload["session"]["git_commit"] = "a" * 40
        next_payload["activities"][0]["title"] = "Mejora"
        second = self.service.execute(next_payload)
        self.assertEqual(first.session_page_id, second.session_page_id)
        self.assertEqual(second.session_action, "existing")
        self.assertEqual(len(self.client.projects), 1)
        self.assertEqual(len(self.client.activities), 2)
        self.assertEqual(self.client.update_calls, 1)
        self.assertEqual(self.client.append_calls, 1)

    def test_composes_activity_title_with_project_and_version(self) -> None:
        self.service.execute(payload())
        stored = self.client.activities[0]["properties"]["Titulo"]["title"][0]["text"]["content"]
        self.assertEqual(stored, "auto_Notification V1.0 — Migración inicial")

    def test_does_not_duplicate_existing_title_prefix(self) -> None:
        prefixed = payload()
        prefixed["activities"][0]["title"] = "auto_Notification V1.0 — Migración inicial"
        first = self.service.execute(prefixed)
        self.assertEqual(first.activities_created, 1)
        stored = self.client.activities[0]["properties"]["Titulo"]["title"][0]["text"]["content"]
        self.assertEqual(stored, "auto_Notification V1.0 — Migración inicial")
        # Un payload sin prefijo reusa la actividad ya prefijada (no duplica).
        second = self.service.execute(payload())
        self.assertEqual(second.activities_created, 0)
        self.assertEqual(second.activities_existing, 1)

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
