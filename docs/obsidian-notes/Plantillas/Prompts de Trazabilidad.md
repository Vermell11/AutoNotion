# Prompts de Trazabilidad

Plantillas reutilizables para integrar proyectos con [[Sistema de Trazabilidad]].
Funcionan con Codex y Claude Code.

## Plantillas

- [[Prompt - Integrar proyecto nuevo al Sistema de Trazabilidad]]
- [[Prompt - Migrar proyecto existente al Sistema de Trazabilidad]]
- [[Plantilla - Sesión de proyecto]]

## Copias en Notion

- [Integrar proyecto nuevo](https://app.notion.com/p/Prompt-Integrar-proyecto-nuevo-al-Sistema-de-Trazabilidad-38dbc5d6935781cc9f1fc5f6e05a16b9)
- [Migrar proyecto existente](https://app.notion.com/p/Prompt-Migrar-proyecto-existente-al-Sistema-de-Trazabilidad-38dbc5d6935781ce95b5f54623ec21b7)

## Reglas comunes

- Sustituir los campos entre corchetes por el contexto real.
- [[Reglas globales del Sistema de Trazabilidad]] aplica a todos los proyectos;
  `Proyectos/<Proyecto>/Reglas.md` contiene solo convenciones locales compatibles.
- La IA lee `AGENTS.md` o `CLAUDE.md`, consulta `PROJECT_CONTEXT.md` como índice, lee
  las reglas, el resumen, la última sesión y `Sesiones/En curso.md` en [[Obsidian]], y
  consulta [[Graphify]].
- La IA no reconstruye contexto desde [[Notion]].
- Notion se usa para cierres, métricas, reportes y exposición por API.
- Al inicio se acuerda un reto verificable. Terminar una tarea o resolverlo no cierra
  automáticamente la sesión.
- La IA espera a que el usuario indique cuándo desea cargar la sesión. Solo entonces
  muestra el borrador y pregunta si confirma cerrar y registrar en Notion.
- Sin una respuesta afirmativa inequívoca, la sesión sigue abierta. Tras confirmarla,
  se crea una sola fila con inicio, fin, duración, horas y resultado.
- Cada versión cerrada lleva un tag Git anotado; la primera es `V1.0`.
- Cada proyecto usa `Proyectos/<Proyecto>/Resumen.md`, `Reglas.md`, `Estado actual.md`,
  `Sesiones/`, `Decisiones/` y `Arquitectura/`.
- `Sesiones/En curso.md` conserva resumen, acuerdos, trabajo, evidencia, pendientes y
  conexiones; al cierre se convierte en la nota fechada de la versión.
- [[Obsidian]] conserva el contexto y las decisiones humanas.
- [[Graphify]] conserva relaciones técnicas derivadas y no se ejecuta sin autorización.
- Nunca incluir secretos en prompts, notas, logs ni control de versiones.
