# Project Context

## Identity

- Project name: `Notion` (derived from the repository root folder).
- Current released version: `V1.1`.
- Repository: https://github.com/Vermell11/AutoNotion

## Ultimate purpose

Provide one personal ecosystem where Notion stores measurable work, Obsidian stores
human knowledge, Graphify stores derived technical relationships, and AI tools can
continue safely from the last documented session.

## Canonical context

- Project summary:
  `/Users/andresortegacorpus/Library/Mobile Documents/com~apple~CloudDocs/code/Brain/Cerebro/Proyectos/Notion/Resumen.md`
- Current state:
  `/Users/andresortegacorpus/Library/Mobile Documents/com~apple~CloudDocs/code/Brain/Cerebro/Proyectos/Notion/Estado actual.md`
- Last closed session:
  `/Users/andresortegacorpus/Library/Mobile Documents/com~apple~CloudDocs/code/Brain/Cerebro/Proyectos/Notion/Sesiones/2026-06-28 - V1.1.md`
- Architecture:
  `/Users/andresortegacorpus/Library/Mobile Documents/com~apple~CloudDocs/code/Brain/Cerebro/Proyectos/Notion/Arquitectura/Arquitectura del sistema.md`

## Technical graph

- Graph data: `graphify-out/graph.json`
- Audit report: `graphify-out/GRAPH_REPORT.md`
- Interactive graph: `graphify-out/graph.html`
- Query the existing graph before rebuilding it.

## Notion write targets

- Activities data source: `033bc5d6-9357-83c6-b71e-07d61caa648f`
- Session ledger (`Proyectos`): `c36049cf-9d28-4999-8f0a-f0e15deaa8b4`

Notion is not part of the normal AI read path. Use it at session close for structured
metrics or when a human explicitly requests reporting, reconciliation, or API access.

## Next session

Agree a new measurable commitment before making changes. Recommended direction:
implement an idempotent, reusable session-close command without adding automatic
synchronization prematurely.

## Required read order

1. `AGENTS.md` or `CLAUDE.md`.
2. This file.
3. Obsidian project summary, current state, and last closed session.
4. Existing Graphify graph.
5. Source code and repository documentation relevant to the task.
