# 2026-06-28 Trazabilidad por sesiones

## Estado

Aceptada.

## Decisión

En [[Sistema de Trazabilidad]], cada fila de la fuente **Proyectos** representa una
sesión cerrada, no un proyecto global. `Nombre` siempre proviene de la carpeta raíz y
puede repetirse.

Cada sesión registra fecha, reto o compromiso, si fue resuelto, resumen, versión, tag y
commit Git. Cada cierre crea una fila nueva y las actividades se relacionan con ella.

Toda versión cerrada lleva un tag Git anotado e inmutable. La primera versión es
`V1.0`. Codex y Claude Code deben proponer un reto verificable al inicio y registrar el
cierre al terminar.

## Consecuencias

Se conserva un historial append-only por proyecto y sesión. No se debe deduplicar por
nombre ni reintentar automáticamente una creación no idempotente.

Relacionado con [[Notion]], [[Obsidian]], [[Graphify]] y [[Sistema de Trazabilidad]].
