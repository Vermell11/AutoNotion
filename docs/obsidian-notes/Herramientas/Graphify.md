# Graphify

[[Graphify]] es la fuente derivada para relaciones de código, dependencias y contexto
técnico de [[Sistema de Trazabilidad]].

Se ejecuta por repositorio, inicialmente de forma manual. Sus resultados son
regenerables y no sustituyen decisiones de [[Obsidian]]. Codex y Claude Code deberán
consultar el grafo existente antes de solicitar una reconstrucción.

## Extracción inicial de Notion

Completada el 2026-06-28:

- 27 archivos.
- 188 nodos.
- 273 aristas.
- 18 comunidades.
- Reporte: `/Users/andresortegacorpus/Library/Mobile Documents/com~apple~CloudDocs/code/Notion/graphify-out/GRAPH_REPORT.md`

La extracción inicial señaló referencias externas no materializadas. Después de la
actualización incremental final, el diagnóstico quedó limpio: cero extremos faltantes,
aristas colgantes, bucles o colapsos. Las siguientes ejecuciones deberían ser
incrementales después de cambios relevantes.
