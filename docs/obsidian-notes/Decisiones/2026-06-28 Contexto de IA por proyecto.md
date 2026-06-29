# 2026-06-28 Contexto de IA por proyecto

## Estado

Aceptada.

## Decisión

[[Obsidian]] conserva la memoria humana detallada y [[Graphify]] el contexto técnico
derivado. `PROJECT_CONTEXT.md` funciona únicamente como índice portable para Codex y
Claude Code. [[Notion]] queda fuera de la lectura rutinaria y se utiliza para cierres,
métricas, reportes y acceso por API.

El orden de lectura es:

`AGENTS/CLAUDE → PROJECT_CONTEXT → Obsidian → Graphify → código`

## Consecuencias

Se evita duplicar la documentación narrativa en Notion y se reduce la dependencia de
red. Cada cierre debe actualizar la sesión de Obsidian, el índice, el grafo, Git y la
fila estructurada de Notion.

Relacionado con [[Sistema de Trazabilidad]] y [[Proyectos/Notion/Resumen]].
