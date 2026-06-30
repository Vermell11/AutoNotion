# Arquitectura del sistema Notion

## Fuentes de verdad

- [[Obsidian]]: propósito, estado, decisiones, arquitectura y sesiones detalladas.
- [[Graphify]]: relaciones derivadas del código.
- [[Notion]]: ledger estructurado, métricas, horas y exposición por API.
- Git: implementación y evidencia de versiones.

## Flujo de inicio

`AGENTS.md / CLAUDE.md → PROJECT_CONTEXT.md → En curso (si existe) → Graphify 600 → máximo 3 fuentes → Ponytail → código`

Reglas extensas, resumen, estado, ADR y sesiones históricas se cargan solo cuando la
tarea las requiere. Notion queda fuera del flujo normal de lectura.

## Flujo de cierre

`Borrador → confirmación → Obsidian/PROJECT_CONTEXT/Graphify/pruebas → commit final → close-session --dry-run → tag local → close-session → status=completed → push`

La fila de Notion contiene propiedades estructuradas y un resumen de máximo 120
palabras con solo trabajo y resultado. La narrativa y evidencia permanecen en Obsidian.
Completar una tarea no activa este flujo; sin confirmación explícita, la sesión sigue
abierta y no se escribe la fila.

`closing.py` valida el payload y esquemas, reconcilia `Nombre + Versión + Commit Git` y
reanuda actividades faltantes. El proyecto consumidor invoca el CLI central mediante
su ruta absoluta y no recibe la API Key.

## Estructura por proyecto

```text
Proyectos/Notion/
├── Resumen.md
├── Reglas.md
├── Estado actual.md
├── Sesiones/
│   ├── En curso.md
│   └── <Fecha> - <Versión>.md
├── Decisiones/
└── Arquitectura/
```
