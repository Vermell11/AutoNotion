"""Carga de configuración local sin exponer credenciales."""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_KEY_FILE = PROJECT_ROOT / "public" / "apikey" / "key.txt"
DEFAULT_CONFIG_FILE = PROJECT_ROOT / "config" / "notion.toml"


class ConfigurationError(RuntimeError):
    """Configuración ausente o inválida."""


@dataclass(frozen=True)
class Settings:
    token: str
    api_version: str = "2026-03-11"
    api_base_url: str = "https://api.notion.com/v1"
    timeout_seconds: float = 20.0
    max_retries: int = 3
    credential_source: str = "unknown"


def load_settings(
    key_file: Path = DEFAULT_KEY_FILE, config_file: Path = DEFAULT_CONFIG_FILE
) -> Settings:
    """Carga entorno primero y usa el archivo local solo como transición."""
    public_config: dict[str, Any] = {}
    try:
        if config_file.exists():
            public_config = tomllib.loads(config_file.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise ConfigurationError("La configuración pública de Notion no es válida.") from exc

    token = os.environ.get("NOTION_API_KEY", "").strip()
    source = "NOTION_API_KEY"

    if not token:
        source = str(key_file.relative_to(PROJECT_ROOT)) if key_file.is_relative_to(PROJECT_ROOT) else "key file"
        try:
            raw_token = key_file.read_bytes()
            encoding = "utf-16" if raw_token.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig"
            token = raw_token.decode(encoding).strip()
        except FileNotFoundError as exc:
            raise ConfigurationError(
                "No se encontró NOTION_API_KEY ni el archivo local de credenciales."
            ) from exc
        except (OSError, UnicodeDecodeError) as exc:
            raise ConfigurationError("No fue posible leer la credencial de Notion.") from exc

    if not token:
        raise ConfigurationError("La credencial de Notion está vacía.")

    return Settings(
        token=token,
        api_version=os.environ.get(
            "NOTION_API_VERSION", str(public_config.get("api_version", "2026-03-11"))
        ),
        api_base_url=os.environ.get(
            "NOTION_API_BASE_URL",
            str(public_config.get("api_base_url", "https://api.notion.com/v1")),
        ).rstrip("/"),
        timeout_seconds=float(public_config.get("timeout_seconds", 20)),
        max_retries=int(public_config.get("max_retries", 3)),
        credential_source=source,
    )
