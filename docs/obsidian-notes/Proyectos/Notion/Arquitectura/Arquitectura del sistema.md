# Arquitectura del sistema Notion

## Fuentes de verdad

- [[Obsidian]]: propósito, estado, decisiones, arquitectura y sesiones detalladas.
- [[Graphify]]: relaciones derivadas del código.
- [[Notion]]: ledger estructurado, métricas, horas y exposición por API.
- Git: implementación y evidencia de versiones.

## Flujo de inicio

`~/.claude/CLAUDE.md → contrato canónico → AGENTS/PROJECT_CONTEXT → En curso (si existe) → Graphify 600 → máximo 3 fuentes → Ponytail → código`

Reglas extensas, resumen, estado, ADR y sesiones históricas se cargan solo cuando la
tarea las requiere. Notion queda fuera del flujo normal de lectura.

## Flujo de cierre

`Preparación → Obsidian/PROJECT_CONTEXT/Graphify/pruebas → commit final → close-project prepare → borrador → confirmación → close-project finalize → push atómico`

La fila de Notion contiene propiedades estructuradas y un resumen de máximo 120
palabras con solo trabajo y resultado. La narrativa y evidencia permanecen en Obsidian.
Completar una tarea no activa este flujo; sin confirmación explícita, la sesión sigue
abierta y no se escribe la fila.

`closing.py` valida el payload y esquemas, reconcilia el proyecto por `Nombre` y
reanuda actividades faltantes. El proyecto consumidor invoca el CLI central mediante
su ruta absoluta y no recibe la API Key.

`excel_export.py` descubre bases descendientes, pagina sus data sources, normaliza
propiedades y crea un libro con índice y una hoja por fuente sin modificar Notion.

`weekly_report.py` filtra de lunes a domingo la fuente de actividades y dibuja un PDF
16:9 determinista. `scripts/reporteSemanal.py` resuelve configuración, nombre de
salida y ejecución sin argumentos; no escribe en Notion.

`project_close.py` coordina las dos fases: valida Git y Notion, crea el tag anotado
solo tras confirmación y publica rama + tag como una unidad; si el remoto está vacío,
crea `main` durante esa publicación.

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
