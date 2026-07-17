"""Exportación de fuentes de datos de Notion a un libro Excel."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

from .notion_client import DataSourceSummary, NotionClient


class ExcelExportError(RuntimeError):
    """La exportación no pudo completarse."""


@dataclass(frozen=True)
class ExcelExportResult:
    output: Path
    sources: int
    rows: int


def export_excel(
    client: NotionClient,
    output: Path,
    *,
    page_id: str | None = None,
    include_content: bool = False,
) -> ExcelExportResult:
    _xlsxwriter()
    if output.suffix.lower() != ".xlsx":
        raise ExcelExportError("El archivo de salida debe terminar en .xlsx.")
    sources = (
        discover_page_data_sources(client, page_id)
        if page_id
        else client.discover_data_sources()
    )
    if not sources:
        raise ExcelExportError("No se encontraron fuentes de datos visibles.")

    datasets = []
    total_rows = 0
    for source in sources:
        schema = client.retrieve_data_source(source.id)
        rows = client.query_data_source(source.id)
        datasets.append(
            (
                DataSourceSummary(
                    id=source.id,
                    title=_source_title(schema, source.title),
                    database_id=source.database_id,
                    url=source.url or schema.get("url"),
                ),
                schema,
                [
                    normalize_page(
                        page,
                        schema,
                        content=extract_page_text(client, page["id"])
                        if include_content
                        else None,
                    )
                    for page in rows
                ],
            )
        )
        total_rows += len(rows)

    _write_workbook(output, datasets, include_content=include_content)
    return ExcelExportResult(output.resolve(), len(datasets), total_rows)


def discover_page_data_sources(
    client: NotionClient, page_id: str
) -> list[DataSourceSummary]:
    database_ids: list[str] = []
    pending = [page_id]
    seen: set[str] = set()

    while pending:
        parent_id = pending.pop()
        if parent_id in seen:
            continue
        seen.add(parent_id)
        for block in client.retrieve_block_children(parent_id):
            block_id = block.get("id")
            if not isinstance(block_id, str):
                continue
            if block.get("type") == "child_database":
                database_ids.append(block_id)
            elif block.get("has_children"):
                pending.append(block_id)

    found: dict[str, DataSourceSummary] = {}
    for database_id in database_ids:
        database = client.retrieve_database(database_id)
        for source in database.get("data_sources", []):
            if not isinstance(source, dict) or not source.get("id"):
                continue
            source_id = str(source["id"])
            found[source_id] = DataSourceSummary(
                id=source_id,
                title=str(source.get("name") or "(sin título)"),
                database_id=database_id,
                url=None,
            )
    return list(found.values())


def normalize_page(
    page: dict[str, Any],
    schema: dict[str, Any],
    *,
    content: str | None = None,
) -> dict[str, Any]:
    values: dict[str, Any] = {
        "_Page ID": page.get("id", ""),
        "_URL": page.get("url", ""),
        "_Creado": _parse_iso(page.get("created_time")),
        "_Modificado": _parse_iso(page.get("last_edited_time")),
    }
    properties = page.get("properties", {})
    for name in schema.get("properties", {}):
        values[name] = property_value(properties.get(name, {}))
    if content is not None:
        chunks = [
            content[index : index + 32_000] for index in range(0, len(content), 32_000)
        ]
        if len(chunks) <= 1:
            values["_Contenido"] = content
        else:
            values.update(
                {
                    f"_Contenido {index}": chunk
                    for index, chunk in enumerate(chunks, start=1)
                }
            )
    return values


def property_value(prop: dict[str, Any]) -> Any:
    kind = prop.get("type")
    value = prop.get(kind) if isinstance(kind, str) else None
    if kind in {"title", "rich_text"}:
        return _plain_text(value)
    if kind in {"number", "checkbox", "url", "email", "phone_number"}:
        return value
    if kind in {"select", "status"}:
        return value.get("name", "") if isinstance(value, dict) else ""
    if kind == "multi_select":
        return "; ".join(item.get("name", "") for item in value or [])
    if kind == "date":
        if not isinstance(value, dict):
            return ""
        start, end = value.get("start"), value.get("end")
        return f"{start} — {end}" if end else _parse_iso(start)
    if kind == "people":
        return "; ".join(_user_label(item) for item in value or [])
    if kind == "files":
        return "; ".join(
            str(item.get("name") or _file_url(item)) for item in value or []
        )
    if kind == "relation":
        return "; ".join(str(item.get("id", "")) for item in value or [])
    if kind in {"created_time", "last_edited_time"}:
        return _parse_iso(value)
    if kind in {"created_by", "last_edited_by"}:
        return _user_label(value)
    if kind == "unique_id" and isinstance(value, dict):
        return f"{value.get('prefix') or ''}{value.get('number') or ''}"
    if kind in {"formula", "rollup"}:
        return _typed_value(value)
    return _json_text(value)


def extract_page_text(client: NotionClient, page_id: str) -> str:
    lines: list[str] = []

    def walk(parent_id: str) -> None:
        for block in client.retrieve_block_children(parent_id):
            kind = block.get("type")
            payload = block.get(kind, {}) if isinstance(kind, str) else {}
            if isinstance(payload, dict):
                text = _plain_text(payload.get("rich_text"))
                if text:
                    lines.append(text)
            block_id = block.get("id")
            if block.get("has_children") and kind != "child_database" and block_id:
                walk(str(block_id))

    walk(page_id)
    return "\n".join(lines)


def _write_workbook(
    output: Path,
    datasets: list[tuple[DataSourceSummary, dict[str, Any], list[dict[str, Any]]]],
    *,
    include_content: bool,
) -> None:
    xlsxwriter = _xlsxwriter()

    output.parent.mkdir(parents=True, exist_ok=True)
    workbook = xlsxwriter.Workbook(output, {"remove_timezone": True})
    title_format = workbook.add_format(
        {"bold": True, "font_color": "#FFFFFF", "bg_color": "#155E75"}
    )
    date_format = workbook.add_format({"num_format": "yyyy-mm-dd"})
    datetime_format = workbook.add_format({"num_format": "yyyy-mm-dd hh:mm"})
    wrap_format = workbook.add_format({"text_wrap": True, "valign": "top"})

    index = workbook.add_worksheet("Índice")
    index.hide_gridlines(2)
    index.freeze_panes(1, 0)
    index_headers = [
        "Hoja",
        "Fuente",
        "Filas",
        "Columnas",
        "Data source ID",
        "Database ID",
        "URL",
    ]
    index.write_row(0, 0, index_headers, title_format)

    used_names = {"Índice"}
    for index_row, (source, schema, rows) in enumerate(datasets, start=1):
        sheet_name = _sheet_name(source.title, used_names)
        sheet = workbook.add_worksheet(sheet_name)
        sheet.hide_gridlines(2)
        sheet.freeze_panes(1, 0)
        headers = ["_Page ID", "_URL", "_Creado", "_Modificado"]
        headers.extend(schema.get("properties", {}).keys())
        if include_content:
            headers.extend(
                sorted(
                    {
                        key
                        for row in rows
                        for key in row
                        if key.startswith("_Contenido")
                    }
                    or {"_Contenido"}
                )
            )
        sheet.write_row(0, 0, headers, title_format)

        for row_index, row in enumerate(rows, start=1):
            for column_index, header in enumerate(headers):
                _write_value(
                    sheet,
                    row_index,
                    column_index,
                    row.get(header),
                    date_format,
                    datetime_format,
                    wrap_format,
                )
        if rows:
            sheet.autofilter(0, 0, len(rows), len(headers) - 1)
        for column_index, header in enumerate(headers):
            sample = [str(row.get(header) or "") for row in rows[:100]]
            width = min(max([len(header), *(len(value) for value in sample)]) + 2, 45)
            sheet.set_column(column_index, column_index, max(width, 12))

        index.write_url(index_row, 0, f"internal:'{sheet_name}'!A1", string=sheet_name)
        index.write(index_row, 1, source.title)
        index.write_number(index_row, 2, len(rows))
        index.write_number(index_row, 3, len(headers))
        index.write(index_row, 4, source.id)
        index.write(index_row, 5, source.database_id or "")
        index.write(index_row, 6, source.url or "")

    index.autofilter(0, 0, len(datasets), len(index_headers) - 1)
    index.set_column("A:B", 28)
    index.set_column("C:D", 12)
    index.set_column("E:F", 38)
    index.set_column("G:G", 48)
    workbook.close()


def _write_value(
    sheet: Any,
    row: int,
    column: int,
    value: Any,
    date_format: Any,
    datetime_format: Any,
    wrap_format: Any,
) -> None:
    if isinstance(value, datetime):
        sheet.write_datetime(row, column, value, datetime_format)
    elif isinstance(value, date):
        sheet.write_datetime(row, column, value, date_format)
    elif isinstance(value, bool):
        sheet.write_boolean(row, column, value)
    elif isinstance(value, (int, float)):
        sheet.write_number(row, column, value)
    else:
        sheet.write(row, column, value if value is not None else "", wrap_format)


def _source_title(schema: dict[str, Any], fallback: str) -> str:
    title = _plain_text(schema.get("title"))
    return title or str(schema.get("name") or fallback or "(sin título)")


def _sheet_name(title: str, used: set[str]) -> str:
    base = re.sub(r"[\[\]:*?/\\]", " ", title).strip() or "Sin título"
    base = base[:31]
    candidate = base
    suffix = 2
    while candidate in used:
        tail = f" ({suffix})"
        candidate = f"{base[:31 - len(tail)]}{tail}"
        suffix += 1
    used.add(candidate)
    return candidate


def _plain_text(value: Any) -> str:
    if not isinstance(value, list):
        return ""
    return "".join(
        str(item.get("plain_text") or item.get("text", {}).get("content") or "")
        for item in value
        if isinstance(item, dict)
    )


def _typed_value(value: Any) -> Any:
    if not isinstance(value, dict):
        return _json_text(value)
    kind = value.get("type")
    nested = value.get(kind) if isinstance(kind, str) else value
    if kind in {"string", "number", "boolean"}:
        return nested
    if kind == "date":
        return _parse_iso(nested.get("start")) if isinstance(nested, dict) else ""
    if kind == "array":
        return "; ".join(str(_typed_value(item)) for item in nested or [])
    return _json_text(nested)


def _parse_iso(value: Any) -> Any:
    if not isinstance(value, str) or not value:
        return ""
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.date() if "T" not in value else parsed
    except ValueError:
        return value


def _user_label(value: Any) -> str:
    if not isinstance(value, dict):
        return ""
    person = value.get("person") or {}
    return str(value.get("name") or person.get("email") or value.get("id") or "")


def _file_url(value: dict[str, Any]) -> str:
    kind = value.get("type")
    payload = value.get(kind, {}) if isinstance(kind, str) else {}
    return str(payload.get("url", "")) if isinstance(payload, dict) else ""


def _json_text(value: Any) -> str:
    return "" if value is None else json.dumps(value, ensure_ascii=False, sort_keys=True)


def _xlsxwriter() -> Any:
    try:
        import xlsxwriter
    except ImportError as exc:
        raise ExcelExportError(
            "Falta XlsxWriter. Instala el proyecto con: python3 -m pip install -e ."
        ) from exc
    return xlsxwriter
