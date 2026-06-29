# Prompts de Trazabilidad

Plantillas reutilizables para integrar proyectos con [[Sistema de Trazabilidad]].
Funcionan con Codex y Claude Code.

## Plantillas

- [[Prompt - Integrar proyecto nuevo al Sistema de Trazabilidad]]
- [[Prompt - Migrar proyecto existente al Sistema de Trazabilidad]]

## Copias en Notion

- [Integrar proyecto nuevo](https://app.notion.com/p/Prompt-Integrar-proyecto-nuevo-al-Sistema-de-Trazabilidad-38dbc5d6935781cc9f1fc5f6e05a16b9)
- [Migrar proyecto existente](https://app.notion.com/p/Prompt-Migrar-proyecto-existente-al-Sistema-de-Trazabilidad-38dbc5d6935781ce95b5f54623ec21b7)

## Reglas comunes

- Sustituir los campos entre corchetes por el contexto real.
- La IA reconstruye contexto desde `PROJECT_CONTEXT.md`, [[Obsidian]] y [[Graphify]],
  no desde [[Notion]].
- Notion se usa para cierres, métricas, reportes y exposición por API.
- Al inicio se acuerda un reto verificable; al cierre se crea una fila nueva de sesión
  con inicio, fin, duración, horas y resultado.
- Cada versión cerrada lleva un tag Git anotado; la primera es `V1.0`.
- Cada proyecto usa `Proyectos/<Proyecto>/Resumen.md`, `Estado actual.md`, `Sesiones/`,
  `Decisiones/` y `Arquitectura/`.
- [[Obsidian]] conserva el contexto y las decisiones humanas.
- [[Graphify]] conserva relaciones técnicas derivadas y no se ejecuta sin autorización.
- Nunca incluir secretos en prompts, notas, logs ni control de versiones.
