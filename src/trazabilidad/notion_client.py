"""Cliente HTTP pequeño, seguro y extensible para la API pública de Notion."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from email.message import Message
from typing import Any, Callable
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .config import Settings


class NotionError(RuntimeError):
    """Error base que garantiza mensajes sin credenciales."""


class NotionAuthenticationError(NotionError):
    """La credencial no fue aceptada."""


class NotionPermissionError(NotionError):
    """La credencial no tiene acceso al recurso."""


class NotionRateLimitError(NotionError):
    """Notion mantuvo el rate limit después de los reintentos."""


class NotionConnectionError(NotionError):
    """Fallo de red o respuesta no interpretable."""


@dataclass(frozen=True)
class DataSourceSummary:
    id: str
    title: str
    database_id: str | None
    url: str | None


class NotionClient:
    """Cubre verificación y descubrimiento; admite crecer por composición."""

    def __init__(
        self,
        settings: Settings,
        *,
        opener: Callable[..., Any] = urlopen,
        sleeper: Callable[[float], None] = time.sleep,
    ) -> None:
        self._settings = settings
        self._opener = opener
        self._sleeper = sleeper

    def _safe_message(self, value: str) -> str:
        return value.replace(self._settings.token, "[REDACTED]")

    def _request(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
        *,
        retry_safe: bool | None = None,
    ) -> dict[str, Any]:
        if retry_safe is None:
            retry_safe = method in {"GET", "PATCH"}
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        request = Request(
            f"{self._settings.api_base_url}{path}",
            data=body,
            method=method,
            headers={
                "Authorization": f"Bearer {self._settings.token}",
                "Notion-Version": self._settings.api_version,
                "Content-Type": "application/json",
                "User-Agent": "sistema-trazabilidad/0.1",
            },
        )

        for attempt in range(self._settings.max_retries + 1):
            try:
                with self._opener(request, timeout=self._settings.timeout_seconds) as response:
                    raw = response.read()
                decoded = json.loads(raw.decode("utf-8"))
                if not isinstance(decoded, dict):
                    raise NotionConnectionError("Notion devolvió una respuesta inesperada.")
                return decoded
            except HTTPError as exc:
                if exc.code == 401:
                    raise NotionAuthenticationError(
                        "Notion rechazó la credencial (401). Revísala o rótala."
                    ) from exc
                if exc.code == 403:
                    raise NotionPermissionError(
                        "La conexión no tiene permisos suficientes (403)."
                    ) from exc

                retryable = retry_safe and (exc.code == 429 or 500 <= exc.code < 600)
                if retryable and attempt < self._settings.max_retries:
                    self._sleeper(self._retry_delay(attempt, exc.headers))
                    continue
                if exc.code == 429:
                    raise NotionRateLimitError(
                        "Notion limitó las solicitudes aun después de reintentar."
                    ) from exc
                raise NotionConnectionError(
                    f"Notion respondió con HTTP {exc.code}."
                ) from exc
            except (URLError, TimeoutError) as exc:
                if retry_safe and attempt < self._settings.max_retries:
                    self._sleeper(2**attempt)
                    continue
                reason = self._safe_message(str(getattr(exc, "reason", exc)))
                raise NotionConnectionError(f"No fue posible conectar con Notion: {reason}") from exc
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise NotionConnectionError("Notion devolvió JSON inválido.") from exc

        raise NotionConnectionError("No fue posible completar la solicitud.")

    @staticmethod
    def _retry_delay(attempt: int, headers: Message | None) -> float:
        retry_after = headers.get("Retry-After") if headers else None
        try:
            return min(float(retry_after), 30.0) if retry_after else float(2**attempt)
        except ValueError:
            return float(2**attempt)

    def verify_connection(self) -> dict[str, str | None]:
        """Valida el token sin devolver datos sensibles del propietario."""
        user = self._request("GET", "/users/me")
        return {
            "id": user.get("id"),
            "name": user.get("name"),
            "type": user.get("type"),
        }

    def retrieve_data_source(self, data_source_id: str) -> dict[str, Any]:
        """Obtiene el esquema necesario para construir propiedades válidas."""
        return self._request("GET", f"/data_sources/{data_source_id}")

    def retrieve_database(self, database_id: str) -> dict[str, Any]:
        """Obtiene el contenedor y sus fuentes de datos hijas."""
        return self._request("GET", f"/databases/{database_id}")

    def create_database(
        self,
        *,
        parent_page_id: str,
        title: str,
        properties: dict[str, Any],
        description: str | None = None,
        is_inline: bool = True,
    ) -> dict[str, Any]:
        """Crea una base con su fuente inicial y esquema explícito."""
        payload: dict[str, Any] = {
            "parent": {"type": "page_id", "page_id": parent_page_id},
            "title": [{"type": "text", "text": {"content": title}}],
            "is_inline": is_inline,
            "initial_data_source": {
                "title": [{"type": "text", "text": {"content": title}}],
                "properties": properties,
            },
        }
        if description:
            payload["description"] = [
                {"type": "text", "text": {"content": description}}
            ]
        return self._request("POST", "/databases", payload)

    def update_data_source_properties(
        self, data_source_id: str, properties: dict[str, Any]
    ) -> dict[str, Any]:
        """Añade, modifica o elimina propiedades del esquema."""
        if not properties:
            raise ValueError("Debe indicarse al menos una propiedad.")
        return self._request(
            "PATCH",
            f"/data_sources/{data_source_id}",
            {"properties": properties},
        )

    def retrieve_page(self, page_id: str) -> dict[str, Any]:
        """Obtiene una página para resolver identificadores suministrados."""
        return self._request("GET", f"/pages/{page_id}")

    def retrieve_block_children(self, block_id: str) -> list[dict[str, Any]]:
        """Recorre los bloques hijos directos de una página o bloque."""
        cursor: str | None = None
        found: list[dict[str, Any]] = []
        while True:
            params = {"page_size": 100}
            if cursor:
                params["start_cursor"] = cursor
            response = self._request(
                "GET", f"/blocks/{block_id}/children?{urlencode(params)}"
            )
            found.extend(
                item for item in response.get("results", []) if isinstance(item, dict)
            )
            if not response.get("has_more"):
                return found
            cursor = response.get("next_cursor")
            if not cursor:
                raise NotionConnectionError(
                    "Notion indicó más bloques, pero no entregó cursor."
                )

    def query_data_source(
        self, data_source_id: str, *, page_size: int = 100
    ) -> list[dict[str, Any]]:
        """Recorre las páginas de una fuente de datos."""
        cursor: str | None = None
        found: list[dict[str, Any]] = []
        while True:
            payload: dict[str, Any] = {"page_size": min(page_size, 100)}
            if cursor:
                payload["start_cursor"] = cursor
            response = self._request(
                "POST",
                f"/data_sources/{data_source_id}/query",
                payload,
                retry_safe=True,
            )
            found.extend(
                item for item in response.get("results", []) if isinstance(item, dict)
            )
            if not response.get("has_more"):
                return found
            cursor = response.get("next_cursor")
            if not cursor:
                raise NotionConnectionError(
                    "Notion indicó más páginas, pero no entregó cursor."
                )

    def create_markdown_page(
        self,
        *,
        title: str,
        markdown: str,
        data_source_id: str | None = None,
        parent_page_id: str | None = None,
        title_property: str = "title",
    ) -> dict[str, Any]:
        """Crea una página documental bajo una fuente o una página."""
        if not title.strip() or not markdown.strip():
            raise ValueError("El título y el contenido no pueden estar vacíos.")
        if (data_source_id is None) == (parent_page_id is None):
            raise ValueError("Debe indicarse exactamente un padre.")
        parent = (
            {"type": "data_source_id", "data_source_id": data_source_id}
            if data_source_id
            else {"type": "page_id", "page_id": parent_page_id}
        )
        return self._request(
            "POST",
            "/pages",
            {
                "parent": parent,
                "properties": {
                    title_property: {
                        "type": "title",
                        "title": [{"type": "text", "text": {"content": title}}],
                    }
                },
                "markdown": markdown,
            },
        )

    def create_data_source_page(
        self,
        *,
        data_source_id: str,
        properties: dict[str, Any],
        markdown: str | None = None,
    ) -> dict[str, Any]:
        """Crea una fila/página con propiedades completas en una fuente."""
        if not properties:
            raise ValueError("Debe indicarse al menos una propiedad.")
        payload: dict[str, Any] = {
            "parent": {
                "type": "data_source_id",
                "data_source_id": data_source_id,
            },
            "properties": properties,
        }
        if markdown:
            payload["markdown"] = markdown
        return self._request("POST", "/pages", payload)

    def update_page_properties(
        self, page_id: str, properties: dict[str, Any]
    ) -> dict[str, Any]:
        """Actualiza propiedades de una fila/página sin tocar su contenido."""
        if not properties:
            raise ValueError("Debe indicarse al menos una propiedad.")
        return self._request(
            "PATCH",
            f"/pages/{page_id}",
            {"properties": properties},
        )

    def trash_page(self, page_id: str) -> dict[str, Any]:
        """Envía una página duplicada u obsoleta a la papelera."""
        return self._request("PATCH", f"/pages/{page_id}", {"in_trash": True})

    def replace_page_markdown(self, page_id: str, markdown: str) -> dict[str, Any]:
        """Reemplaza el contenido de una página conservando sus propiedades."""
        if not markdown.strip():
            raise ValueError("El contenido no puede estar vacío.")
        return self._request(
            "PATCH",
            f"/pages/{page_id}/markdown",
            {
                "type": "replace_content",
                "replace_content": {"new_str": markdown},
            },
        )

    def discover_data_sources(self, *, query: str | None = None) -> list[DataSourceSummary]:
        """Descubre todas las fuentes compartidas, recorriendo la paginación."""
        cursor: str | None = None
        found: list[DataSourceSummary] = []

        while True:
            payload: dict[str, Any] = {
                "filter": {"property": "object", "value": "data_source"},
                "page_size": 100,
            }
            if query:
                payload["query"] = query
            if cursor:
                payload["start_cursor"] = cursor

            response = self._request("POST", "/search", payload, retry_safe=True)
            for item in response.get("results", []):
                if item.get("object") != "data_source":
                    continue
                parent = item.get("parent") or {}
                found.append(
                    DataSourceSummary(
                        id=item.get("id", ""),
                        title=_plain_title(item.get("title")),
                        database_id=parent.get("database_id"),
                        url=item.get("url"),
                    )
                )

            if not response.get("has_more"):
                break
            cursor = response.get("next_cursor")
            if not cursor:
                raise NotionConnectionError(
                    "Notion indicó más resultados, pero no entregó cursor."
                )

        return found

    def search_pages(self, query: str) -> list[dict[str, Any]]:
        """Busca páginas por título y recorre todos los resultados."""
        cursor: str | None = None
        found: list[dict[str, Any]] = []
        while True:
            payload: dict[str, Any] = {
                "query": query,
                "filter": {"property": "object", "value": "page"},
                "page_size": 100,
            }
            if cursor:
                payload["start_cursor"] = cursor
            response = self._request("POST", "/search", payload, retry_safe=True)
            found.extend(
                item for item in response.get("results", []) if isinstance(item, dict)
            )
            if not response.get("has_more"):
                return found
            cursor = response.get("next_cursor")
            if not cursor:
                raise NotionConnectionError(
                    "Notion indicó más páginas, pero no entregó cursor."
                )


def _plain_title(value: Any) -> str:
    if not isinstance(value, list):
        return "(sin título)"
    parts: list[str] = []
    for fragment in value:
        if isinstance(fragment, dict):
            text = fragment.get("plain_text")
            if isinstance(text, str):
                parts.append(text)
    return "".join(parts).strip() or "(sin título)"
