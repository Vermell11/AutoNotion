#!/usr/bin/env python3
"""Genera el informe de gestión en public/output.

Configura el informe con las variables de abajo o por línea de comandos:
    python3 scripts/reporteSemanal.py --periodo diario --ambito trabajo --fecha 2026-07-03
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import sys
import tomllib


# ---------------------------------------------------------------------------
# Configuración por defecto (editable):
PERIODO = "semanal"  # "diario" | "semanal"
AMBITO = "trabajo"   # "trabajo" (excluye Category=Personal) | "personal" | "todo"
FECHA = None         # None = hoy; o una fecha como date(2026, 7, 3)
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from trazabilidad.config import DEFAULT_CONFIG_FILE, load_settings  # noqa: E402
from trazabilidad.notion_client import NotionClient, NotionError  # noqa: E402
from trazabilidad.weekly_report import (  # noqa: E402
    PERIODS,
    SCOPES,
    WeeklyReportError,
    generate_weekly_report,
    period_bounds,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--periodo", choices=PERIODS, default=PERIODO)
    parser.add_argument("--ambito", choices=SCOPES, default=AMBITO)
    parser.add_argument(
        "--fecha",
        type=date.fromisoformat,
        default=FECHA,
        help="fecha de referencia AAAA-MM-DD (por defecto, hoy)",
    )
    return parser.parse_args()


def output_path(periodo: str, ambito: str, start: date, end: date) -> Path:
    if periodo == "diario":
        name = f"reporte-diario-{start.isoformat()}"
    else:
        name = f"reporte-semanal-{start.isoformat()}-al-{end.isoformat()}"
    if ambito != "trabajo":
        name += f"-{ambito}"
    return ROOT / "public" / "output" / f"{name}.pdf"


def main() -> int:
    args = parse_args()
    try:
        config = tomllib.loads(DEFAULT_CONFIG_FILE.read_text(encoding="utf-8"))
        activities = config["activities"]
        start, end = period_bounds(args.fecha, args.periodo)
        fields = {
            key: activities.get(config_key, "")
            for key, config_key in {
                "title": "title_property",
                "date": "datetime_property",
                "status": "status_property",
                "category": "category_property",
                "module": "module_property",
                "hours": "hours_property",
            }.items()
        }
        result = generate_weekly_report(
            NotionClient(load_settings()),
            data_source_id=activities["data_source_id"],
            output=output_path(args.periodo, args.ambito, start, end),
            reference=args.fecha,
            fields=fields,
            period=args.periodo,
            scope=args.ambito,
        )
        print(
            f"Informe {result.period} ({result.scope}): {result.activities} actividades, "
            f"{result.hours:g} horas, {result.output}"
        )
        return 0
    except (KeyError, OSError, tomllib.TOMLDecodeError, WeeklyReportError, NotionError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
