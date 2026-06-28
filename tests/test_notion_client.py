from __future__ import annotations

import io
import json
import unittest
from urllib.error import HTTPError, URLError

from trazabilidad.config import Settings
from trazabilidad.notion_client import (
    NotionAuthenticationError,
    NotionClient,
    NotionConnectionError,
)


class FakeResponse:
    def __init__(self, payload: dict) -> None:
        self._body = json.dumps(payload).encode()

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self) -> bytes:
        return self._body


class NotionClientTests(unittest.TestCase):
    def setUp(self) -> None:
        self.settings = Settings(token="super-secret", max_retries=0)

    def test_verify_connection_returns_limited_identity(self) -> None:
        def opener(request, timeout):
            self.assertEqual(request.full_url, "https://api.notion.com/v1/users/me")
            self.assertEqual(request.headers["Authorization"], "Bearer super-secret")
            return FakeResponse(
                {"id": "bot-id", "name": "Trazabilidad", "type": "bot", "owner": {"email": "x"}}
            )

        result = NotionClient(self.settings, opener=opener).verify_connection()
        self.assertEqual(result, {"id": "bot-id", "name": "Trazabilidad", "type": "bot"})

    def test_discovery_paginates_and_maps_sources(self) -> None:
        responses = iter(
            [
                {
                    "results": [
                        {
                            "object": "data_source",
                            "id": "source-1",
                            "title": [{"plain_text": "Actividades"}],
                            "parent": {"database_id": "database-1"},
                            "url": "https://notion.so/example",
                        }
                    ],
                    "has_more": True,
                    "next_cursor": "next",
                },
                {"results": [], "has_more": False, "next_cursor": None},
            ]
        )
        requests = []

        def opener(request, timeout):
            requests.append(json.loads(request.data))
            return FakeResponse(next(responses))

        found = NotionClient(self.settings, opener=opener).discover_data_sources()
        self.assertEqual(found[0].title, "Actividades")
        self.assertEqual(requests[1]["start_cursor"], "next")

    def test_create_markdown_page_uses_data_source_parent(self) -> None:
        captured = {}

        def opener(request, timeout):
            captured.update(json.loads(request.data))
            return FakeResponse({"object": "page", "id": "page-1", "url": "https://notion.so/page"})

        result = NotionClient(self.settings, opener=opener).create_markdown_page(
            data_source_id="source-1",
            title_property="Nombre",
            title="Prompt",
            markdown="# Contenido",
        )
        self.assertEqual(result["id"], "page-1")
        self.assertEqual(captured["parent"]["data_source_id"], "source-1")
        self.assertEqual(
            captured["properties"]["Nombre"]["title"][0]["text"]["content"], "Prompt"
        )
        self.assertEqual(captured["markdown"], "# Contenido")

    def test_create_markdown_page_accepts_page_parent(self) -> None:
        captured = {}

        def opener(request, timeout):
            captured.update(json.loads(request.data))
            return FakeResponse({"object": "page", "id": "page-2"})

        NotionClient(self.settings, opener=opener).create_markdown_page(
            parent_page_id="parent-1",
            title="Prompt",
            markdown="# Contenido",
        )
        self.assertEqual(
            captured["parent"], {"type": "page_id", "page_id": "parent-1"}
        )
        self.assertIn("title", captured["properties"])

    def test_search_pages_filters_objects(self) -> None:
        def opener(request, timeout):
            payload = json.loads(request.data)
            self.assertEqual(payload["filter"]["value"], "page")
            return FakeResponse(
                {
                    "results": [{"object": "page", "id": "page-1"}],
                    "has_more": False,
                }
            )

        found = NotionClient(self.settings, opener=opener).search_pages("Prompt")
        self.assertEqual(found[0]["id"], "page-1")

    def test_retrieve_block_children_uses_pagination_query(self) -> None:
        def opener(request, timeout):
            self.assertIn("page_size=100", request.full_url)
            return FakeResponse(
                {"results": [{"object": "block", "id": "block-1"}], "has_more": False}
            )

        found = NotionClient(self.settings, opener=opener).retrieve_block_children("page-1")
        self.assertEqual(found[0]["id"], "block-1")

    def test_replace_page_markdown_uses_replace_content(self) -> None:
        captured = {}

        def opener(request, timeout):
            self.assertEqual(request.method, "PATCH")
            self.assertTrue(request.full_url.endswith("/pages/page-1/markdown"))
            captured.update(json.loads(request.data))
            return FakeResponse({"object": "page_markdown", "id": "page-1"})

        NotionClient(self.settings, opener=opener).replace_page_markdown(
            "page-1", "# Nuevo contenido"
        )
        self.assertEqual(captured["type"], "replace_content")
        self.assertEqual(
            captured["replace_content"]["new_str"], "# Nuevo contenido"
        )

    def test_create_database_nests_initial_data_source_schema(self) -> None:
        captured = {}

        def opener(request, timeout):
            captured.update(json.loads(request.data))
            return FakeResponse({"object": "database", "id": "database-1"})

        NotionClient(self.settings, opener=opener).create_database(
            parent_page_id="page-1",
            title="Proyectos",
            properties={"Nombre": {"title": {}}},
        )
        self.assertEqual(captured["parent"]["page_id"], "page-1")
        self.assertEqual(
            captured["initial_data_source"]["properties"]["Nombre"], {"title": {}}
        )

    def test_update_data_source_properties_uses_patch(self) -> None:
        captured = {}

        def opener(request, timeout):
            self.assertEqual(request.method, "PATCH")
            captured.update(json.loads(request.data))
            return FakeResponse({"object": "data_source", "id": "source-1"})

        NotionClient(self.settings, opener=opener).update_data_source_properties(
            "source-1", {"Proyecto": {"relation": {"data_source_id": "source-2"}}}
        )
        self.assertIn("Proyecto", captured["properties"])

    def test_create_data_source_page_accepts_complete_properties(self) -> None:
        captured = {}

        def opener(request, timeout):
            captured.update(json.loads(request.data))
            return FakeResponse({"object": "page", "id": "project-1"})

        NotionClient(self.settings, opener=opener).create_data_source_page(
            data_source_id="projects",
            properties={"Nombre": {"title": [{"text": {"content": "Notion"}}]}},
            markdown="# Notion",
        )
        self.assertEqual(captured["parent"]["data_source_id"], "projects")
        self.assertEqual(captured["markdown"], "# Notion")

    def test_update_page_properties_does_not_replace_content(self) -> None:
        captured = {}

        def opener(request, timeout):
            captured.update(json.loads(request.data))
            return FakeResponse({"object": "page", "id": "project-1"})

        NotionClient(self.settings, opener=opener).update_page_properties(
            "project-1", {"Estado": {"status": {"name": "In progress"}}}
        )
        self.assertIn("properties", captured)
        self.assertNotIn("markdown", captured)

    def test_authentication_error_never_contains_token(self) -> None:
        error = HTTPError(
            "https://api.notion.com/v1/users/me",
            401,
            "super-secret",
            {},
            io.BytesIO(b'{"message":"super-secret"}'),
        )

        def opener(request, timeout):
            raise error

        with self.assertRaises(NotionAuthenticationError) as caught:
            NotionClient(self.settings, opener=opener).verify_connection()
        cause = caught.exception.__cause__
        if isinstance(cause, HTTPError):
            cause.close()
        self.assertNotIn("super-secret", str(caught.exception))

    def test_network_error_is_redacted(self) -> None:
        def opener(request, timeout):
            raise URLError("failed near super-secret")

        with self.assertRaises(NotionConnectionError) as caught:
            NotionClient(self.settings, opener=opener).verify_connection()
        self.assertNotIn("super-secret", str(caught.exception))

    def test_non_idempotent_post_is_not_retried(self) -> None:
        attempts = 0

        def opener(request, timeout):
            nonlocal attempts
            attempts += 1
            raise HTTPError(
                request.full_url,
                503,
                "temporary",
                {},
                None,
            )

        with self.assertRaises(NotionConnectionError) as caught:
            NotionClient(
                Settings(token="super-secret", max_retries=3),
                opener=opener,
                sleeper=lambda _: None,
            ).create_data_source_page(
                data_source_id="projects",
                properties={"Nombre": {"title": [{"text": {"content": "Notion"}}]}},
            )
        cause = caught.exception.__cause__
        if isinstance(cause, HTTPError):
            cause.close()
        self.assertEqual(attempts, 1)

    def test_trash_page_sets_in_trash(self) -> None:
        captured = {}

        def opener(request, timeout):
            captured.update(json.loads(request.data))
            return FakeResponse({"object": "page", "id": "duplicate", "in_trash": True})

        NotionClient(self.settings, opener=opener).trash_page("duplicate")
        self.assertTrue(captured["in_trash"])
