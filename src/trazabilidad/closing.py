"""Cierre idempotente de proyectos y actividades en Notion."""

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
class ActivityCloseRef:
    title: str
    id: str
    url: str


@dataclass(frozen=True)
class CloseResult:
    status: str
    session_action: str
    session_page_id: str | None
    session_url: str | None
    activities_created: int
    activities_existing: int
    activities_planned: int
    activity_pages: tuple[ActivityCloseRef, ...] = ()


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

MAX_NOTION_SUMMARY_WORDS = 120
MAX_ACTIVITY_DESCRIPTION_WORDS = 80


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
    quality = payload.get("quality")
    if not isinstance(session, dict):
        raise ClosePayloadError("El payload requiere un objeto session.")
    if not isinstance(activities, list) or not all(
        isinstance(activity, dict) for activity in activities
    ):
        raise ClosePayloadError("activities debe ser una lista de objetos.")
    if not isinstance(quality, dict):
        raise ClosePayloadError("El payload requiere un objeto quality.")
    for field in ("offline_audit", "online_validation"):
        if not isinstance(quality.get(field), str) or not quality[field].strip():
            raise ClosePayloadError(f"quality.{field} debe ser texto no vacío.")
    known_alerts = quality.get("known_alerts")
    if not isinstance(known_alerts, list) or not all(
        isinstance(alert, str) and alert.strip() for alert in known_alerts
    ):
        raise ClosePayloadError("quality.known_alerts debe ser una lista de textos.")

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
    _validate_word_limit(
        session["summary"], "session.summary", MAX_NOTION_SUMMARY_WORDS
    )
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
        _validate_word_limit(
            activity["description"],
            f"Actividad {index}.description",
            MAX_ACTIVITY_DESCRIPTION_WORDS,
        )
    reported = [
        datetime.fromisoformat(activity["reported_at"]).replace(tzinfo=None)
        for activity in activities
    ]
    if any(current >= following for current, following in zip(reported, reported[1:])):
        raise ClosePayloadError(
            "activities debe estar en orden cronológico estricto por reported_at."
        )


def _validate_number(value: dict[str, Any], field: str, prefix: str) -> None:
    number = value[field]
    if isinstance(number, bool) or not isinstance(number, (int, float)) or number < 0:
        raise ClosePayloadError(f"{prefix}.{field} debe ser un número no negativo.")


def _validate_iso_date(value: str, label: str) -> None:
    try:
        datetime.fromisoformat(value)
    except ValueError as exc:
        raise ClosePayloadError(f"{label} no es una fecha ISO válida.") from exc


def _validate_word_limit(value: str, label: str, maximum: int) -> None:
    if len(value.split()) > maximum:
        raise ClosePayloadError(f"{label} supera el máximo de {maximum} palabras.")


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
        # Regla de títulos (Reglas.md de ControlP): las actividades se llaman
        # "{proyecto} {versión} — {actividad}". El conector compone el prefijo
        # SIEMPRE (el payload lleva el título sin prefijo); idempotente: si el
        # título ya lo trae, no se duplica. Búsqueda y creación usan el título
        # compuesto, así crea/reusa sigue encontrando actividades renombradas.
        for activity in activities:
            activity["title"] = _composed_activity_title(session, activity["title"])
        existing_session = self._find_session(session)
        existing_activity_count = (
            self._count_existing_activities(existing_session["id"], activities)
            if existing_session
            else 0
        )

        if dry_run:
            return CloseResult(
                status="dry_run",
                session_action="existing" if existing_session else "would_create",
                session_page_id=existing_session.get("id") if existing_session else None,
                session_url=existing_session.get("url") if existing_session else None,
                activities_created=0,
                activities_existing=existing_activity_count,
                activities_planned=len(activities),
            )

        session_page = existing_session or self._create_session_reconciled(
            session, payload.get("markdown")
        )
        if existing_session:
            self._update_session_reconciled(session_page["id"], session)
        created = 0
        existing = 0
        activity_pages: list[ActivityCloseRef] = []
        for activity in activities:
            activity_page = self._find_activity(session_page["id"], activity)
            if activity_page:
                existing += 1
            else:
                activity_page = self._create_activity_reconciled(
                    session_page["id"], activity
                )
                created += 1
            activity_pages.append(_activity_close_ref(activity_page, activity["title"]))

        if existing_session:
            self._append_session_log_reconciled(session_page["id"], session)

        return CloseResult(
            status="completed",
            session_action="existing" if existing_session else "created",
            session_page_id=session_page.get("id"),
            session_url=session_page.get("url"),
            activities_created=created,
            activities_existing=existing,
            activities_planned=len(activities),
            activity_pages=tuple(activity_pages),
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
            if _plain(properties.get("Nombre", {}).get("title")) == session["name"]:
                matches.append(page)
        if len(matches) > 1:
            raise ClosePayloadError(
                "Notion contiene varios proyectos con el mismo Nombre. "
                "Consolida la base Proyectos antes de cerrar la sesión."
            )
        return matches[0] if matches else None

    def _create_session_reconciled(
        self, session: dict[str, Any], markdown: Any
    ) -> dict[str, Any]:
        try:
            return self.client.create_data_source_page(
                data_source_id=self.targets.projects_data_source_id,
                properties=_session_properties(session, overwrite_summary=True),
                markdown=_session_log_markdown(session),
            )
        except NotionError:
            reconciled = self._find_session(session)
            if reconciled:
                return reconciled
            raise

    def _update_session_reconciled(
        self, session_page_id: str, session: dict[str, Any]
    ) -> None:
        self.client.update_page_properties(
            session_page_id,
            _session_properties(session, overwrite_summary=False),
        )

    def _append_session_log_reconciled(
        self, session_page_id: str, session: dict[str, Any]
    ) -> None:
        marker = _session_log_marker(session)
        if marker not in self.client.retrieve_page_markdown(session_page_id):
            self.client.append_page_markdown(
                session_page_id,
                _session_log_markdown(session),
            )

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


def _activity_close_ref(page: dict[str, Any], title: str) -> ActivityCloseRef:
    page_id = page.get("id")
    url = page.get("url")
    if not isinstance(page_id, str) or not page_id or not isinstance(url, str) or not url:
        raise ClosePayloadError(
            f"Notion no devolvió id y URL para la actividad {title!r}; "
            "el cierre no puede reconciliarse."
        )
    return ActivityCloseRef(title=title, id=page_id, url=url)


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


def _session_properties(
    session: dict[str, Any], *, overwrite_summary: bool
) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "Nombre": _title(session["name"]),
        "Fecha sesión": _date(session["session_date"]),
        "Inicio": _date(session["start"]),
        "Fin": _date(session["end"]),
        "Duración minutos": {"number": session["duration_minutes"]},
        "Horas": {"number": session["hours"]},
        "Reto o compromiso": _rich_text(session["challenge"]),
        "Resuelto": {"checkbox": session["resolved"]},
        "Versión": _rich_text(session["version"]),
        "Tag Git": _rich_text(session["git_tag"]),
        "Commit Git": _rich_text(session["git_commit"]),
        "Estado": {"status": {"name": session.get("status", "Done")}},
    }
    if overwrite_summary or session.get("project_summary"):
        properties["Resumen"] = _rich_text(
            session.get("project_summary") or session.get("objective") or session["summary"]
        )
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


def _session_log_markdown(session: dict[str, Any]) -> str:
    return "\n".join(
        [
            _session_log_marker(session),
            f"## Sesión {session['version']} — {session['session_date']}",
            f"**Reto:** {session['challenge']}",
            "",
            f"**Resultado:** {session['summary']}",
            "",
            "**Evidencia:** "
            f"tag `{session['git_tag']}`, "
            f"commit `{session['git_commit']}`, "
            f"{session['hours']} h.",
        ]
    )


def _session_log_marker(session: dict[str, Any]) -> str:
    return f"<!-- trazabilidad:{session['version']}:{session['git_commit']} -->"


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


def _composed_activity_title(session: dict[str, Any], title: str) -> str:
    prefix = f"{session['name']} {session['version']} — "
    return title if title.startswith(prefix) else f"{prefix}{title}"


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
