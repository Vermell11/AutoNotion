# ADR-003: Contexto de IA por proyecto

- Fecha: 2026-06-28
- Estado: aceptada

## Contexto

Leer Notion en cada sesión duplica la memoria de Obsidian, introduce dependencia de red
y mezcla métricas con contexto narrativo. Codex y Claude Code necesitan además un punto
de entrada portable dentro del repositorio.

## Decisión

- Obsidian conserva propósito, estado actual, arquitectura y sesiones detalladas.
- Graphify conserva relaciones técnicas derivadas.
- `PROJECT_CONTEXT.md` es un índice mínimo con punteros, versión y reto; no duplica la
  documentación.
- `AGENTS.md` y `CLAUDE.md` exigen el mismo orden de lectura.
- Notion queda fuera de la lectura rutinaria y recibe el cierre estructurado, métricas y
  datos disponibles por API.

## Consecuencias

- La IA puede continuar sin consultar servicios externos.
- El contexto narrativo tiene una sola fuente de verdad.
- El repositorio conserva un puntero portable aun cuando la bóveda no esté disponible.
- El cierre debe mantener alineados Obsidian, el índice, Graphify, Git y Notion.
