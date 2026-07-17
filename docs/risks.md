# Riesgos y mitigaciones

| Riesgo | Estado | Mitigación |
|---|---|---|
| Token dentro del árbol del proyecto | abierto, transitorio | `.gitignore`, modo `600`, migrar a entorno/llavero y rotar ante exposición |
| No existe repositorio Git en esta carpeta | resuelto | repositorio publicado y versionado |
| Nueve fuentes de Notion visibles y nombres duplicados | mitigado | IDs canónicos en configuración y preflight de esquemas |
| Permisos de Notion distintos entre conexión y usuario | abierto | aplicar privilegio mínimo y prueba de lectura/escritura separada |
| Divergencia entre `docs/` y Obsidian | abierto | checklist de cierre en `AGENTS.md`; Obsidian prevalece para conocimiento |
| Conflictos de sincronización de iCloud en la bóveda | abierto | cambios pequeños, nombres estables y revisión antes de automatizar |
| Grafo desactualizado o con ruido | futuro | actualizaciones incrementales tras cambios arquitectónicos y control de salud |
| Falsas relaciones inferidas por Graphify | futuro | conservar procedencia/confianza y no tratar inferencias como decisiones |
| Doble registro o horas inconsistentes | mitigado | confirmación, identidad de proyecto `Nombre` y actividades por `Titulo + Proyecto`, reconciliación y validación temporal |
| Ruta absoluta del conector central | abierto | distribuir/instalar el CLI sin duplicar secretos |

El descubrimiento del 2026-06-28 encontró dos fuentes llamadas **Reporte de Tickets**;
la canónica fue renombrada después a **Base de datos de trabajo**. También encontró dos
**Documentos** y varias fuentes de calendario/tareas. El nombre no es una clave
confiable; la selección debe hacerse por `data_source_id`.
