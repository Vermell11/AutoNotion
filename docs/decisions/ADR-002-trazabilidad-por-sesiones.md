# ADR-002: Trazabilidad por sesiones y versiones

- Fecha: 2026-06-28
- Estado: aceptada

## Contexto

Una fila global por proyecto oculta la secuencia de trabajo y obliga a sobrescribir el
historial. Además, el nombre del proyecto se repite legítimamente porque siempre se
deriva de la carpeta raíz.

## Decisión

Cada fila de la fuente **Proyectos** representa el cierre de una sesión:

- `Nombre`: nombre de la carpeta raíz.
- `Fecha sesión`: fecha y hora del cierre.
- `Reto o compromiso`: resultado verificable acordado al inicio.
- `Resuelto`: indica si se cumplió.
- `Resumen`: trabajo realizado.
- `Versión`, `Tag Git` y `Commit Git`: evidencia versionada del cierre.

Las filas no se deduplican por nombre. Cada versión cerrada usa un tag Git anotado e
inmutable; la primera versión es `V1.0`.

## Consecuencias

- El historial queda append-only y auditable.
- Varias filas con el mismo nombre son correctas si pertenecen a sesiones distintas.
- Las actividades se relacionan con la fila de sesión aplicable.
- Los reintentos de creación no deben ser automáticos sin una clave idempotente.
