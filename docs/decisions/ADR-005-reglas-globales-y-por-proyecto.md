# ADR-005: Reglas globales y reglas por proyecto

- Fecha: 2026-06-28
- Estado: aceptada

## Contexto

Repetir todas las reglas en cada proyecto provoca divergencias. Mantener únicamente
reglas globales tampoco permite documentar pruebas, despliegues, secretos locales o
convenciones particulares de cada repositorio.

## Decisión

- Obsidian conserva una nota canónica de reglas globales aplicable a todos los
  proyectos.
- Cada proyecto conserva `Proyectos/<Proyecto>/Reglas.md` solo con especializaciones
  locales.
- Las reglas locales no pueden contradecir las globales.
- `PROJECT_CONTEXT.md` funciona como índice y apunta a ambas capas.
- `AGENTS.md` y `CLAUDE.md` hacen cumplir el flujo dentro del repositorio.
- Los prompts para proyectos nuevos y existentes crean o actualizan la capa local y
  enlazan la global, sin duplicarla.

Las reglas globales incluyen el flujo obligatorio de inicio, el tag Git anotado por
versión cerrada y la prohibición de registrar una sesión en Notion hasta que el usuario
indique que desea cargarla y confirme el borrador.

## Consecuencias

- Las políticas transversales cambian en un solo lugar.
- Cada repositorio conserva instrucciones técnicas concretas.
- La precedencia es explícita y las excepciones requieren una decisión documentada.
- Codex y Claude Code reconstruyen contexto con el mismo orden.
