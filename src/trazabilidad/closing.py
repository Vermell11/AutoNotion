"""Cierre idempotente de sesiones y actividades en Notion."""

from __future__ import annotations

import json
import re
import tomllib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .config import ConfigurationError, DEFAULT_CONFIG_FILE
from .notion_client import NotionClient, NotionError


class ClosePayloadError(ValueError):
    """El payload de cierre no cumple el contrato público."""


@dataclass(frozen=True)
class CloseTargets:
    projects_data_source_id: str
    activities_data_source_id: str


@dataclass(frozen=True)
class CloseResult:
    status: str
    session_action: str
    session_page_id: str | None
    session_url: str | None
    activities_created: int
    activities_existing: int
    activities_planned: int


PROJECT_SCHEMA = {
    "Nombre": "title",
    "Fecha sesión": "date",
    "Resuelto": "checkbox",
    "Commit Git": "rich_text",
    "Repositorio": "url",
    "Objetivo": "rich_text",
    "Duración minutos": "number",
    "Obsidian": "url",
    "Versión": "rich_text",
    "Ámbito": "select",
    "Inicio": "date",
    "Reto o compromiso": "rich_text",
    "Fin": "date",
    "Estado": "status",
    "Horas": "number",
    "Resumen": "rich_text",
    "Tag Git": "rich_text",
}

ACTIVITY_SCHEMA = {
    "Titulo": "title",
    "Category": "select",
    "Date Reported": "date",
    "Horas": "number",
    "Descripcion": "rich_text",
    "Status": "status",
    "Proyecto": "relation",
}

SESSION_REQUIRED = {
    "name",
    "start",
    "end",
    "session_date",
    "duration_minutes",
    "hours",
    "challenge",
    "resolved",
    "summary",
    "version",
    "git_tag",
    "git_commit",
}

ACTIVITY_REQUIRED = {
    "title",
    "category",
    "reported_at",
    "hours",
    "description",
    "status",
}


def load_close_targets(config_file: Path = DEFAULT_CONFIG_FILE) -> CloseTargets:
    try:
        data = tomllib.loads(config_file.read_text(encoding="utf-8"))
        projects_id = str(data["projects"]["data_source_id"]).strip()
        activities_id = str(data["activities"]["data_source_id"]).strip()
    except (FileNotFoundError, OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise ConfigurationError("No fue posible leer la configuración de cierre.") from exc
    except (KeyError, TypeError) as exc:
        raise ConfigurationError(
            "La configuración debe definir projects.data_source_id y "
            "activities.data_source_id."
        ) from exc
    if not projects_id or not activities_id:
        raise ConfigurationError("Los data_source_id de cierre no pueden estar vacíos.")
    return CloseTargets(projects_id, activities_id)


def load_close_payload(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ClosePayloadError(f"No existe el payload: {path}") from exc
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ClosePayloadError("El payload de cierre no es JSON válido.") from exc
    if not isinstance(payload, dict):
        raise ClosePayloadError("El payload de cierre debe ser un objeto JSON.")
    validate_close_payload(payload)
    return payload


def validate_close_payload(payload: dict[str, Any]) -> None:
    session = payload.get("session")
    activities = payload.get("activities", [])
    if not isinstance(session, dict):
        raise ClosePayloadError("El payload requiere un objeto session.")
    if not isinstance(activities, list) or not all(
        isinstance(activity, dict) for activity in activities
    ):
        raise ClosePayloadError("activities debe ser una lista de objetos.")

    missing = sorted(SESSION_REQUIRED - session.keys())
    if missing:
        raise ClosePayloadError(
            "Faltan campos obligatorios de sesión: " + ", ".join(missing)
        )
    for field in (
        "name",
        "start",
        "end",
        "session_date",
        "challenge",
        "summary",
        "version",
        "git_tag",
        "git_commit",
    ):
        if not isinstance(session[field], str) or not session[field].strip():
            raise ClosePayloadError(f"session.{field} debe ser texto no vacío.")

    for field in ("start", "end"):
        try:
            value = datetime.fromisoformat(session[field])
        except ValueError as exc:
            raise ClosePayloadError(f"session.{field} no es un timestamp ISO válido.") from exc
        if value.tzinfo is None:
            raise ClosePayloadError(f"session.{field} debe incluir zona horaria.")

    if datetime.fromisoformat(session["end"]) < datetime.fromisoformat(session["start"]):
        raise ClosePayloadError("session.end no puede ser anterior a session.start.")
    _validate_iso_date(session["session_date"], "session.session_date")
    if not isinstance(session["resolved"], bool):
        raise ClosePayloadError("session.resolved debe ser booleano.")
    _validate_number(session, "duration_minutes", "session")
    _validate_number(session, "hours", "session")
    if abs(float(session["hours"]) - float(session["duration_minutes"]) / 60) > 0.02:
        raise ClosePayloadError("session.hours no coincide con duration_minutes / 60.")
    if session["version"] != session["git_tag"]:
        raise ClosePayloadError("session.version y session.git_tag deben coincidir.")
    if not re.fullmatch(r"[0-9a-fA-F]{40}", session["git_commit"]):
        raise ClosePayloadError(
            "session.git_commit debe ser el SHA completo de 40 caracteres."
        )

    for index, activity in enumerate(activities, start=1):
        missing_activity = sorted(ACTIVITY_REQUIRED - activity.keys())
        if missing_activity:
            raise ClosePayloadError(
                f"Actividad {index}: faltan " + ", ".join(missing_activity)
            )
        for field in ("title", "category", "reported_at", "description", "status"):
            if not isinstance(activity[field], str) or not activity[field].strip():
                raise ClosePayloadError(
                    f"Actividad {index}: {field} debe ser texto no vacío."
                )
        _validate_number(activity, "hours", f"Actividad {index}")
        _validate_iso_date(activity["reported_at"], f"Actividad {index}.reported_at")


def _validate_number(value: dict[str, Any], field: str, prefix: str) -> None:
    number = value[field]
    if isinstance(number, bool) or not isinstance(number, (int, float)) or number < 0:
        raise ClosePayloadError(f"{prefix}.{field} debe ser un número no negativo.")


def _validate_iso_date(value: str, label: str) -> None:
    try:
        datetime.fromisoformat(value)
    except ValueError as exc:
        raise ClosePayloadError(f"{label} no es una fecha ISO válida.") from exc


class SessionCloseService:
    """Valida, reconcilia y crea un cierre sin duplicar trabajo previo."""

    def __init__(self, client: NotionClient, targets: CloseTargets) -> None:
        self.client = client
        self.targets = targets

    def execute(self, payload: dict[str, Any], *, dry_run: bool = False) -> CloseResult:
        validate_close_payload(payload)
        self._preflight(payload)
        session = payload["session"]
        activities = payload.get("activities", [])
        existing_session = self._find_session(session)

        if dry_run:
            return CloseResult(
                status="dry_run",
                session_action="existing" if existing_session else "would_create",
                session_page_id=existing_session.get("id") if existing_session else None,
                session_url=existing_session.get("url") if existing_session else None,
                activities_created=0,
                activities_existing=(
                    self._count_existing_activities(existing_session["id"], activities)
                    if existing_session
                    else 0
                ),
                activities_planned=len(activities),
            )

        session_page = existing_session or self._create_session_reconciled(
            session, payload.get("markdown")
        )
        created = 0
        existing = 0
        for activity in activities:
            if self._find_activity(session_page["id"], activity):
                existing += 1
                continue
            self._create_activity_reconciled(session_page["id"], activity)
            created += 1

        return CloseResult(
            status="completed",
            session_action="existing" if existing_session else "created",
            session_page_id=session_page.get("id"),
            session_url=session_page.get("url"),
            activities_created=created,
            activities_existing=existing,
            activities_planned=len(activities),
        )

    def _preflight(self, payload: dict[str, Any]) -> None:
        self.client.verify_connection()
        projects = self.client.retrieve_data_source(
            self.targets.projects_data_source_id
        )
        activities = self.client.retrieve_data_source(
            self.targets.activities_data_source_id
        )
        _assert_schema(projects, PROJECT_SCHEMA, "Proyectos")
        _assert_schema(activities, ACTIVITY_SCHEMA, "Actividades")
        session = payload["session"]
        _assert_option(projects, "Estado", "status", session.get("status", "Done"))
        if session.get("scope"):
            _assert_option(projects, "Ámbito", "select", session["scope"])
        for activity in payload.get("activities", []):
            _assert_option(
                activities, "Category", "select", activity["category"]
            )
            _assert_option(
                activities, "Status", "status", activity["status"]
            )

    def _find_session(self, session: dict[str, Any]) -> dict[str, Any] | None:
        matches = []
        for page in self.client.query_data_source(
            self.targets.projects_data_source_id
        ):
            properties = page.get("properties", {})
            if (
                _plain(properties.get("Nombre", {}).get("title")) == session["name"]
                and _plain(properties.get("Versión", {}).get("rich_text"))
                == session["version"]
                and _plain(properties.get("Commit Git", {}).get("rich_text"))
                == session["git_commit"]
            ):
                matches.append(page)
        if len(matches) > 1:
            raise ClosePayloadError(
                "Notion contiene varias sesiones con la misma identidad "
                "(Nombre, Versión, Commit Git)."
            )
        return matches[0] if matches else None

    def _create_session_reconciled(
        self, session: dict[str, Any], markdown: Any
    ) -> dict[str, Any]:
        try:
            return self.client.create_data_source_page(
                data_source_id=self.targets.projects_data_source_id,
                properties=_session_properties(session),
                markdown=markdown if isinstance(markdown, str) and markdown.strip() else None,
            )
        except NotionError:
            reconciled = self._find_session(session)
            if reconciled:
                return reconciled
            raise

    def _find_activity(
        self, session_page_id: str, activity: dict[str, Any]
    ) -> dict[str, Any] | None:
        for page in self.client.query_data_source(
            self.targets.activities_data_source_id
        ):
            properties = page.get("properties", {})
            relation_ids = {
                item.get("id")
                for item in properties.get("Proyecto", {}).get("relation", [])
            }
            if (
                _plain(properties.get("Titulo", {}).get("title"))
                == activity["title"]
                and session_page_id in relation_ids
            ):
                return page
        return None

    def _count_existing_activities(
        self, session_page_id: str, activities: list[dict[str, Any]]
    ) -> int:
        return sum(
            self._find_activity(session_page_id, activity) is not None
            for activity in activities
        )

    def _create_activity_reconciled(
        self, session_page_id: str, activity: dict[str, Any]
    ) -> dict[str, Any]:
        try:
            return self.client.create_data_source_page(
                data_source_id=self.targets.activities_data_source_id,
                properties=_activity_properties(session_page_id, activity),
            )
        except NotionError:
            reconciled = self._find_activity(session_page_id, activity)
            if reconciled:
                return reconciled
            raise


def _assert_schema(
    response: dict[str, Any], expected: dict[str, str], label: str
) -> None:
    properties = response.get("properties", {})
    errors = [
        f"{name} ({properties.get(name, {}).get('type', 'ausente')} != {kind})"
        for name, kind in expected.items()
        if properties.get(name, {}).get("type") != kind
    ]
    if errors:
        raise ClosePayloadError(
            f"Esquema incompatible en {label}: " + "; ".join(errors)
        )


def _assert_option(
    response: dict[str, Any], property_name: str, kind: str, value: str
) -> None:
    definition = response.get("properties", {}).get(property_name, {})
    options = {
        option.get("name")
        for option in definition.get(kind, {}).get("options", [])
        if isinstance(option, dict)
    }
    if value not in options:
        available = ", ".join(sorted(str(option) for option in options if option))
        raise ClosePayloadError(
            f"{property_name} no admite '{value}'. Opciones: {available or '(ninguna)'}."
        )


def _session_properties(session: dict[str, Any]) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "Nombre": _title(session["name"]),
        "Fecha sesión": _date(session["session_date"]),
        "Inicio": _date(session["start"]),
        "Fin": _date(session["end"]),
        "Duración minutos": {"number": session["duration_minutes"]},
        "Horas": {"number": session["hours"]},
        "Reto o compromiso": _rich_text(session["challenge"]),
        "Resuelto": {"checkbox": session["resolved"]},
        "Resumen": _rich_text(session["summary"]),
        "Versión": _rich_text(session["version"]),
        "Tag Git": _rich_text(session["git_tag"]),
        "Commit Git": _rich_text(session["git_commit"]),
        "Estado": {"status": {"name": session.get("status", "Done")}},
    }
    optional = {
        "scope": ("Ámbito", lambda value: {"select": {"name": value}}),
        "objective": ("Objetivo", _rich_text),
        "repository": ("Repositorio", lambda value: {"url": value}),
        "obsidian": ("Obsidian", lambda value: {"url": value}),
    }
    for field, (property_name, builder) in optional.items():
        value = session.get(field)
        if isinstance(value, str) and value.strip():
            properties[property_name] = builder(value)
    return properties


def _activity_properties(
    session_page_id: str, activity: dict[str, Any]
) -> dict[str, Any]:
    return {
        "Titulo": _title(activity["title"]),
        "Category": {"select": {"name": activity["category"]}},
        "Date Reported": _date(activity["reported_at"]),
        "Horas": {"number": activity["hours"]},
        "Descripcion": _rich_text(activity["description"]),
        "Status": {"status": {"name": activity["status"]}},
        "Proyecto": {"relation": [{"id": session_page_id}]},
    }


def _title(value: str) -> dict[str, Any]:
    return {"title": [{"type": "text", "text": {"content": value}}]}


def _rich_text(value: str) -> dict[str, Any]:
    return {"rich_text": [{"type": "text", "text": {"content": value}}]}


def _date(value: str) -> dict[str, Any]:
    return {"date": {"start": value}}


def _plain(value: Any) -> str:
    if not isinstance(value, list):
        return ""
    return "".join(
        item.get("plain_text", "")
        for item in value
        if isinstance(item, dict)
    )
