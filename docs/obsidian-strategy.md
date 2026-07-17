# Estrategia de Obsidian

La bóveda `Cerebro` es la única autoridad para conocimiento humano. Este repositorio
conserva documentación operativa cercana al código, pero las decisiones, reuniones,
lecciones y contexto durable deben terminar en Obsidian.

## Arquitectura orientada por proyecto

- `Reglas/Reglas globales del Sistema de Trazabilidad.md`: políticas obligatorias y
  transversales.
- `Proyectos/<Proyecto>/Resumen.md`: propósito, navegación y versión actual.
- `Proyectos/<Proyecto>/Reglas.md`: convenciones locales que no contradicen las
  globales.
- `Proyectos/<Proyecto>/Estado actual.md`: capacidades y brechas al objetivo final.
- `Proyectos/<Proyecto>/Backlog.md`: pendientes accionables con prioridad, origen y
  estado.
- `Proyectos/<Proyecto>/Roadmap.md`: hitos, sprints o features futuras vigentes.
- `Proyectos/<Proyecto>/Sesiones/`: memoria cronológica detallada.
- `Proyectos/<Proyecto>/Arquitectura/`: arquitectura durable.
- `Proyectos/<Proyecto>/Decisiones/`: índice o decisiones propias del proyecto.
- `Herramientas/`: contratos, límites y forma de uso.
- `Decisiones/`: una nota fechada por decisión relevante.
- `Plantillas/`: prompts reutilizables para proyectos nuevos y migraciones.
- Futuro: `Reuniones/`, `Lecciones/` y `Bitácora/`.

Usar enlaces estables por nombre: `[[Sistema de Trazabilidad]]`, `[[Notion]]`,
`[[Obsidian]]`, `[[Graphify]]` y `[[Reglas globales del Sistema de Trazabilidad]]`.
Evitar duplicar reglas globales o métricas de Notion; enlazarlas.

La precedencia es: seguridad e instrucción vigente del usuario, reglas globales,
reglas del proyecto y convenciones inferidas del repositorio.

Mientras una sesión está abierta se mantiene `Sesiones/En curso.md`. Al cierre
confirmado se convierte en la nota fechada de la versión usando la plantilla común. La
nota debe permitir reconstruir acuerdos, evidencia, estado y próximos pasos sin
almacenar la conversación completa.

La memoria operacional mínima debe quedar actualizada antes de guardar avance o cerrar:
sesión, estado actual, backlog, roadmap si cambió, decisiones durables y cápsula solo
si cambió contexto estable. Notion conserva el resumen transaccional; Obsidian conserva
la continuidad completa para lectores como ControlP.

## Mantenimiento

- Actualizar la nota del proyecto cuando cambien arquitectura, alcance o riesgos.
- Crear una decisión cuando existan alternativas y consecuencias durables.
- Mantener notas atómicas de herramientas y enlazarlas desde proyectos.
- No volcar automáticamente todo cambio de código: registrar solo contexto útil.
- Revisar alineación documental al cerrar cada cambio relevante.
- Cada resumen de proyecto recuerda que una tarea terminada no cierra la sesión; antes
  de publicar el cierre se muestra el borrador y se exige confirmación explícita.
- Actualizar primero la sesión y el estado del proyecto; Notion recibe solo el resumen
  estructurado y las métricas después de la confirmación.
