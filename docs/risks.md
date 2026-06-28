# Riesgos y mitigaciones

| Riesgo | Estado | Mitigación |
|---|---|---|
| Token dentro del árbol del proyecto | abierto, transitorio | `.gitignore`, modo `600`, migrar a entorno/llavero y rotar ante exposición |
| No existe repositorio Git en esta carpeta | abierto | inicializar solo cuando se decida; validar ignore antes del primer commit |
| Nueve fuentes de Notion visibles y nombres duplicados | abierto | seleccionar IDs canónicos y documentarlos en Fase 2 |
| Permisos de Notion distintos entre conexión y usuario | abierto | aplicar privilegio mínimo y prueba de lectura/escritura separada |
| Divergencia entre `docs/` y Obsidian | abierto | checklist de cierre en `AGENTS.md`; Obsidian prevalece para conocimiento |
| Conflictos de sincronización de iCloud en la bóveda | abierto | cambios pequeños, nombres estables y revisión antes de automatizar |
| Grafo desactualizado o con ruido | futuro | actualizaciones incrementales tras cambios arquitectónicos y control de salud |
| Falsas relaciones inferidas por Graphify | futuro | conservar procedencia/confianza y no tratar inferencias como decisiones |
| Doble registro o horas inconsistentes | futuro | clave idempotente, validación y confirmación humana antes de escribir |

El descubrimiento del 2026-06-28 encontró dos fuentes llamadas **Reporte de Tickets**,
dos llamadas **Documentos** y varias fuentes de calendario/tareas. El nombre no es una
clave confiable; la selección debe hacerse por `data_source_id`.
