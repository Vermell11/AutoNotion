# Arquitectura del sistema Notion

## Fuentes de verdad

- [[Obsidian]]: propósito, estado, decisiones, arquitectura y sesiones detalladas.
- [[Graphify]]: relaciones derivadas del código.
- [[Notion]]: ledger estructurado, métricas, horas y exposición por API.
- Git: implementación y evidencia de versiones.

## Flujo de inicio

`AGENTS.md / CLAUDE.md → PROJECT_CONTEXT.md → Obsidian → Graphify → código`

Notion queda fuera del flujo normal de lectura.

## Flujo de cierre

`Obsidian → PROJECT_CONTEXT.md → Graphify update → pruebas → commit/tag → fila Notion`

La fila de Notion contiene resumen conciso, reto, resultado, inicio, fin, duración,
horas, versión, tag y commit. La narrativa completa permanece en la nota de sesión.

## Estructura por proyecto

```text
Proyectos/Notion/
├── Resumen.md
├── Estado actual.md
├── Sesiones/
├── Decisiones/
└── Arquitectura/
```
