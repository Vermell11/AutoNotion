from __future__ import annotations

import math
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
GRAPH_QUERY_BUDGET = 600


def estimated_tokens(*paths: str) -> int:
    return math.ceil(sum(len((ROOT / path).read_text(encoding="utf-8")) for path in paths) / 4)


class ContextBudgetTests(unittest.TestCase):
    def test_default_startup_stays_within_budget(self) -> None:
        paths = ["AGENTS.md", "PROJECT_CONTEXT.md"]
        open_session = "docs/obsidian-notes/Proyectos/Notion/Sesiones/En curso.md"
        if (ROOT / open_session).exists():
            paths.append(open_session)
        self.assertLessEqual(estimated_tokens(*paths) + GRAPH_QUERY_BUDGET, 1500)

    def test_close_context_stays_within_budget(self) -> None:
        self.assertLessEqual(
            estimated_tokens(
                "docs/obsidian-notes/Plantillas/Plantilla - Sesión de proyecto.md",
                "docs/session-close.md",
                "config/session-close.example.json",
            ),
            1100,
        )

    def test_bootstrap_prompts_share_a_compact_contract(self) -> None:
        contract = "docs/obsidian-notes/Plantillas/Contrato base - Sistema de Trazabilidad.md"
        for prompt in (
            "docs/obsidian-notes/Plantillas/Prompt - Integrar proyecto nuevo al Sistema de Trazabilidad.md",
            "docs/obsidian-notes/Plantillas/Prompt - Migrar proyecto existente al Sistema de Trazabilidad.md",
        ):
            with self.subTest(prompt=prompt):
                self.assertLessEqual(estimated_tokens(contract, prompt), 1300)


if __name__ == "__main__":
    unittest.main()
