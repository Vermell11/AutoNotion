# Estrategia de Obsidian

La bóveda `Cerebro` es la única autoridad para conocimiento humano. Este repositorio
conserva documentación operativa cercana al código, pero las decisiones, reuniones,
lecciones y contexto durable deben terminar en Obsidian.

## Arquitectura orientada por proyecto

- `Proyectos/<Proyecto>/Resumen.md`: propósito, navegación y versión actual.
- `Proyectos/<Proyecto>/Estado actual.md`: capacidades y brechas al objetivo final.
- `Proyectos/<Proyecto>/Sesiones/`: memoria cronológica detallada.
- `Proyectos/<Proyecto>/Arquitectura/`: arquitectura durable.
- `Proyectos/<Proyecto>/Decisiones/`: índice o decisiones propias del proyecto.
- `Herramientas/`: contratos, límites y forma de uso.
- `Decisiones/`: una nota fechada por decisión relevante.
- `Plantillas/`: prompts reutilizables para proyectos nuevos y migraciones.
- Futuro: `Reuniones/`, `Lecciones/` y `Bitácora/`.

Usar enlaces estables por nombre: `[[Sistema de Trazabilidad]]`, `[[Notion]]`,
`[[Obsidian]]`, `[[Graphify]]`. Evitar duplicar métricas de Notion; enlazarlas.

## Mantenimiento

- Actualizar la nota del proyecto cuando cambien arquitectura, alcance o riesgos.
- Crear una decisión cuando existan alternativas y consecuencias durables.
- Mantener notas atómicas de herramientas y enlazarlas desde proyectos.
- No volcar automáticamente todo cambio de código: registrar solo contexto útil.
- Revisar alineación documental al cerrar cada cambio relevante.
- Actualizar primero la sesión y el estado del proyecto; Notion recibe solo el resumen
  estructurado y las métricas.
