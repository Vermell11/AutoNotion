# 2026-06-28 Trazabilidad por sesiones

## Estado

Aceptada.

## Decisión

En [[Sistema de Trazabilidad]], cada fila activa de la fuente **Proyectos** representa
un proyecto canónico. `Nombre` siempre proviene de la carpeta raíz y no debe repetirse
en la tabla activa.

Cada sesión registra fecha, reto o compromiso, si fue resuelto, resumen, versión, tag y
commit Git como entrada acumulada en el cuerpo del proyecto y como actividades
relacionadas. Cada cierre actualiza el proyecto existente en vez de crear otra fila.

Toda versión cerrada lleva un tag Git anotado e inmutable. La primera versión es
`V1.0`. Codex y Claude Code deben proponer un reto verificable al inicio y registrar el
cierre al terminar.

## Consecuencias

Se conserva un historial append-only por proyecto y sesión. No se debe deduplicar por
nombre ni reintentar automáticamente una creación no idempotente.

Relacionado con [[Notion]], [[Obsidian]], [[Graphify]] y [[Sistema de Trazabilidad]].
