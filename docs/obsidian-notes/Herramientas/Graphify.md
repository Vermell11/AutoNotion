# Graphify

[[Graphify]] es la fuente derivada para relaciones de código, dependencias y contexto
técnico de [[Sistema de Trazabilidad]].

Se ejecuta por repositorio, inicialmente de forma manual. Sus resultados son
regenerables y no sustituyen decisiones de [[Obsidian]]. Codex y Claude Code deberán
consultar el grafo existente antes de solicitar una reconstrucción.

## Uso eficiente

Al iniciar una tarea se consulta con términos específicos y `--budget 600`. La salida
sirve para escoger como máximo tres fuentes; no se carga el grafo completo ni toda la
documentación. Solo se amplía a 1200 cuando la primera consulta no aporta evidencia
suficiente.

## Extracción inicial de Notion

Completada el 2026-06-28. Las métricas cambian con cada actualización; la fuente
vigente es:

`/Users/andresortegacorpus/Library/Mobile Documents/com~apple~CloudDocs/code/Notion/graphify-out/GRAPH_REPORT.md`

La extracción inicial señaló referencias externas no materializadas. Después de la
actualización incremental final, el diagnóstico quedó limpio: cero extremos faltantes,
aristas colgantes, bucles o colapsos. Las siguientes ejecuciones deberían ser
incrementales después de cambios relevantes.
