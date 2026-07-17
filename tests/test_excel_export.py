from __future__ import annotations

from datetime import datetime
import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from trazabilidad.excel_export import (
    discover_page_data_sources,
    normalize_page,
    property_value,
    _write_workbook,
)
from trazabilidad.notion_client import DataSourceSummary


class FakeClient:
    def retrieve_block_children(self, block_id: str) -> list[dict]:
        return {
            "root": [
                {"id": "nested", "type": "child_page", "has_children": True},
                {"id": "database-1", "type": "child_database", "has_children": True},
            ],
            "nested": [
                {"id": "database-2", "type": "child_database", "has_children": True}
            ],
        }.get(block_id, [])

    def retrieve_database(self, database_id: str) -> dict:
        return {
            "data_sources": [
                {"id": f"source-{database_id}", "name": f"Fuente {database_id}"}
            ]
        }


class ExcelExportTests(unittest.TestCase):
    def test_discovers_data_sources_recursively_without_entering_databases(self) -> None:
        sources = discover_page_data_sources(FakeClient(), "root")
        self.assertEqual(
            {source.id for source in sources},
            {"source-database-1", "source-database-2"},
        )

    def test_normalizes_page_properties(self) -> None:
        schema = {
            "properties": {
                "Nombre": {"type": "title"},
                "Horas": {"type": "number"},
                "Estado": {"type": "status"},
                "Etiquetas": {"type": "multi_select"},
            }
        }
        page = {
            "id": "page-1",
            "url": "https://notion.test/page-1",
            "created_time": "2026-06-29T10:00:00Z",
            "last_edited_time": "2026-06-29T11:00:00Z",
            "properties": {
                "Nombre": {
                    "type": "title",
                    "title": [{"plain_text": "Actividad"}],
                },
                "Horas": {"type": "number", "number": 1.5},
                "Estado": {"type": "status", "status": {"name": "Done"}},
                "Etiquetas": {
                    "type": "multi_select",
                    "multi_select": [{"name": "A"}, {"name": "B"}],
                },
            },
        }
        row = normalize_page(page, schema, content="Detalle")
        self.assertEqual(row["Nombre"], "Actividad")
        self.assertEqual(row["Horas"], 1.5)
        self.assertEqual(row["Estado"], "Done")
        self.assertEqual(row["Etiquetas"], "A; B")
        self.assertEqual(row["_Contenido"], "Detalle")
        self.assertIsInstance(row["_Creado"], datetime)

    def test_formula_and_relation_values_are_readable(self) -> None:
        self.assertEqual(
            property_value(
                {"type": "formula", "formula": {"type": "number", "number": 3}}
            ),
            3,
        )
        self.assertEqual(
            property_value(
                {
                    "type": "relation",
                    "relation": [{"id": "one"}, {"id": "two"}],
                }
            ),
            "one; two",
        )

    def test_splits_long_page_content_without_losing_text(self) -> None:
        content = "x" * 64_001
        row = normalize_page(
            {"id": "page", "properties": {}},
            {"properties": {}},
            content=content,
        )
        self.assertEqual(
            "".join(
                value for key, value in row.items() if key.startswith("_Contenido")
            ),
            content,
        )

    @unittest.skipUnless(importlib.util.find_spec("xlsxwriter"), "requiere XlsxWriter")
    def test_writes_index_and_source_sheet(self) -> None:
        source = DataSourceSummary("source-1", "Actividades", "database-1", None)
        schema = {"properties": {"Nombre": {"type": "title"}}}
        rows = [
            {
                "_Page ID": "page-1",
                "_URL": "",
                "_Creado": "",
                "_Modificado": "",
                "Nombre": "Prueba",
            }
        ]
        with TemporaryDirectory() as directory:
            output = Path(directory) / "export.xlsx"
            _write_workbook(output, [(source, schema, rows)], include_content=False)
            self.assertGreater(output.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
