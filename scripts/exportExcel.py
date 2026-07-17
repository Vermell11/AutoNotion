#!/usr/bin/env python3
"""Exporta automáticamente la página principal de Notion a public/output."""

from __future__ import annotations

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from trazabilidad.cli import main  # noqa: E402


PAGE_ID = "388bc5d6-9357-8046-bc4f-d8f1e6405c0b"


if __name__ == "__main__":
    raise SystemExit(main(["export-excel", "--page-id", PAGE_ID, "--include-content"]))
