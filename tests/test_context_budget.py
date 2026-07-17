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
        # Presupuesto 1100 → 1600 (2026-07-13, aprobado): la doctrina de cierre
        # creció con reconciliación post-finalize, coherencia de numeración y
        # regla de títulos de actividades.
        self.assertLessEqual(
            estimated_tokens(
                "docs/obsidian-notes/Plantillas/Plantilla - Sesión de proyecto.md",
                "docs/session-close.md",
                "config/session-close.example.json",
            ),
            1600,
        )

    def test_prompts_are_small_and_share_the_canonical_contract(self) -> None:
        contract = "docs/obsidian-notes/Plantillas/Contrato base - Sistema de Trazabilidad.md"
        for prompt in (
            "docs/obsidian-notes/Plantillas/Prompt - Integrar proyecto nuevo al Sistema de Trazabilidad.md",
            "docs/obsidian-notes/Plantillas/Prompt - Migrar proyecto existente al Sistema de Trazabilidad.md",
            "docs/obsidian-notes/Plantillas/Prompt - Guardar avance de sesión.md",
            "docs/obsidian-notes/Plantillas/Prompt - Cerrar sesión en el Sistema de Trazabilidad.md",
        ):
            with self.subTest(prompt=prompt):
                self.assertLessEqual(estimated_tokens(prompt), 300)
                self.assertLessEqual(estimated_tokens(contract, prompt), 1800)
                self.assertIn(
                    "Contrato base - Sistema de Trazabilidad.md",
                    (ROOT / prompt).read_text(encoding="utf-8"),
                )

    def test_contract_maps_context_graph_and_notion_credentials(self) -> None:
        contract = (
            ROOT
            / "docs/obsidian-notes/Plantillas/"
            "Contrato base - Sistema de Trazabilidad.md"
        ).read_text(encoding="utf-8")
        for expected in (
            "AGENTS.md",
            "PROJECT_CONTEXT.md",
            "Graphify",
            "NOTION_API_KEY",
            "key.txt",
            "scripts/notion.py check",
            "close-project prepare",
            "close-project finalize",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, contract)

    def test_save_progress_prompt_never_closes_the_session(self) -> None:
        prompt = (
            ROOT
            / "docs/obsidian-notes/Plantillas/Prompt - Guardar avance de sesión.md"
        ).read_text(encoding="utf-8")
        self.assertIn("no Notion, tag ni push", prompt)


if __name__ == "__main__":
    unittest.main()
