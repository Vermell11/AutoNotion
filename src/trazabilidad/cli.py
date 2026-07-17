"""CLI segura para las operaciones iniciales de Notion."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
import sys
from datetime import datetime
from pathlib import Path

from .closing import (
    ClosePayloadError,
    SessionCloseService,
    load_close_payload,
    load_close_targets,
)
from .config import (
    ConfigurationError,
    DEFAULT_CONFIG_FILE,
    load_settings,
)
from .excel_export import ExcelExportError, export_excel
from .notion_client import NotionClient, NotionError
from .project_close import ProjectCloseCoordinator, ProjectCloseError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="trazabilidad-notion")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="verifica conexión y autenticación")
    discover = commands.add_parser("discover", help="lista fuentes de datos disponibles")
    discover.add_argument("--query", help="filtra por texto del título")
    discover.add_argument("--json", action="store_true", help="salida JSON")
    close = commands.add_parser(
        "close-session",
        help="valida y registra una sesión con actividades sin duplicarlas",
    )
    close.add_argument("--payload", required=True, type=Path, help="payload JSON de cierre")
    close.add_argument(
        "--dry-run",
        action="store_true",
        help="valida conexión, esquemas e identidad sin escribir",
    )
    close.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_FILE,
        help="configuración pública con los data_source_id",
    )
    project_close = commands.add_parser(
        "close-project",
        help="coordina preflight o cierre final de Git + Notion",
    )
    project_close.add_argument(
        "phase",
        choices=("prepare", "finalize"),
        help="prepare no escribe; finalize requiere confirmación previa del usuario",
    )
    project_close.add_argument("--project", required=True, type=Path, help="raíz Git")
    project_close.add_argument("--payload", required=True, type=Path, help="payload JSON")
    project_close.add_argument("--remote", default="origin", help="remoto Git")
    project_close.add_argument("--branch", default="main", help="rama que se publicará")
    project_close.add_argument("--tag-message", help="mensaje del tag anotado")
    project_close.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_FILE,
        help="configuración pública con los data_source_id",
    )
    export = commands.add_parser(
        "export-excel",
        help="exporta fuentes visibles de Notion a un libro con una hoja por fuente",
    )
    export.add_argument(
        "--page-id",
        help="limita la exportación a bases descendientes de esta página",
    )
    export.add_argument(
        "--output",
        type=Path,
        help="archivo .xlsx; por defecto se crea en public/output",
    )
    export.add_argument(
        "--include-content",
        action="store_true",
        help="incluye el texto del cuerpo de cada página (más llamadas a la API)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        config_file = (
            args.config
            if args.command in {"close-session", "close-project"}
            else DEFAULT_CONFIG_FILE
        )
        settings = load_settings(config_file=config_file)
        client = NotionClient(settings)
        if args.command == "check":
            identity = client.verify_connection()
            label = identity.get("name") or identity.get("type") or "conexión"
            print(f"Conexión válida: {label}.")
            return 0

        if args.command == "close-session":
            payload = load_close_payload(args.payload)
            result = SessionCloseService(
                client, load_close_targets(args.config)
            ).execute(payload, dry_run=args.dry_run)
            print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
            return 0

        if args.command == "close-project":
            payload = load_close_payload(args.payload)
            coordinator = ProjectCloseCoordinator(
                SessionCloseService(client, load_close_targets(args.config))
            )
            options = {
                "remote": args.remote,
                "branch": args.branch,
            }
            if args.phase == "prepare":
                result = coordinator.prepare(args.project, payload, **options)
            else:
                result = coordinator.finalize(
                    args.project,
                    payload,
                    tag_message=args.tag_message,
                    **options,
                )
            print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
            return 0

        if args.command == "export-excel":
            output = args.output or (
                Path(__file__).resolve().parents[2]
                / "public"
                / "output"
                / f"notion-export-{datetime.now().strftime('%Y%m%d-%H%M%S')}.xlsx"
            )
            result = export_excel(
                client,
                output,
                page_id=args.page_id,
                include_content=args.include_content,
            )
            print(
                f"Exportación completada: {result.sources} fuentes, "
                f"{result.rows} filas, {result.output}"
            )
            return 0

        sources = client.discover_data_sources(query=args.query)
        if args.json:
            print(json.dumps([source.__dict__ for source in sources], ensure_ascii=False, indent=2))
        elif not sources:
            print("No hay fuentes de datos visibles para esta conexión.")
        else:
            print(f"Fuentes de datos visibles: {len(sources)}")
            for source in sources:
                parent = f" · database={source.database_id}" if source.database_id else ""
                print(f"- {source.title} · id={source.id}{parent}")
        return 0
    except (
        ClosePayloadError,
        ConfigurationError,
        ExcelExportError,
        NotionError,
        ProjectCloseError,
    ) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
