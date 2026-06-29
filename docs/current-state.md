# Estado actual y avance al propósito final

## Propósito último

Construir un ecosistema personal donde:

- Notion conserve actividades, sesiones, horas, estados y datos compartibles por API.
- Obsidian sea la memoria humana y contextual por proyecto.
- Graphify mantenga relaciones técnicas derivadas del código.
- Codex y Claude Code continúen desde la última sesión sin reconstruir contexto.

## Capacidades actuales

La aplicación es una base Python sin dependencias externas que actualmente:

- Carga `NOTION_API_KEY` o, temporalmente, `public/apikey/key.txt` en UTF-8/UTF-16.
- Verifica autenticación contra Notion.
- Descubre y pagina fuentes de datos.
- Consulta esquemas, bases, páginas y bloques.
- Crea bases, páginas Markdown y filas con propiedades completas.
- Actualiza esquemas, propiedades y contenido Markdown.
- Envía duplicados a la papelera.
- Distingue operaciones reintentables de creaciones no idempotentes.
- Calcula duración exacta de sesiones a partir de timestamps con zona horaria.
- Mantiene pruebas unitarias sin llamadas reales.

El CLI público todavía ofrece únicamente `check` y `discover`. Las operaciones de
escritura existen como biblioteca y se usan de forma controlada durante los cierres.

## Avance por capacidad

| Capacidad final | Estado | Evidencia / brecha |
|---|---|---|
| Arquitectura y seguridad base | Completa | ADR, reglas, `.gitignore`, secreto fuera de Git |
| Documentación humana en Obsidian | Completa para Notion | Estructura por proyecto y sesiones |
| Contexto técnico Graphify | Operativo | Grafo local, reporte y actualización incremental |
| Continuidad Codex/Claude | Operativa | `PROJECT_CONTEXT.md`, `AGENTS.md`, `CLAUDE.md` |
| Ledger de sesiones en Notion | Operativo | Una fila nueva por cierre, métricas y evidencia Git |
| Registro de actividades | Parcial | Fuente y cliente disponibles; falta flujo humano estable |
| Medición automática de sesiones | Parcial | Cálculo implementado; cierre aún es asistido |
| Reportes y dashboards | Pendiente | No implementados |
| Detección automática de cambios | Pendiente | No implementada |
| Sincronización automática | Pendiente | Deliberadamente fuera de alcance |
| Correos y tareas programadas | Pendiente | Deliberadamente fuera de alcance |

## Lectura honesta del avance

La fundación y la continuidad entre sesiones están resueltas. El sistema todavía no es
una plataforma automatizada: requiere una IA o persona para ejecutar el cierre, escribir
la fila de Notion y mantener Obsidian. El siguiente salto de valor es un flujo
idempotente de registro de actividades y sesiones, seguido por reportes.

El cierre asistido exige ahora mostrar un borrador y obtener confirmación humana
explícita. La IA espera a que el usuario indique cuándo desea cargar la sesión;
resolver una tarea o el reto no autoriza escribir en Notion.

La continuidad durante una sesión abierta se conserva en `Sesiones/En curso.md`. Al
cierre confirmado se transforma en una nota fechada con resumen, acuerdos, evidencia,
estado, pendientes y conexiones.

## Riesgos vigentes

- `key.txt` sigue siendo un fallback local y debe migrarse a llavero o entorno.
- Las copias de notas en `docs/obsidian-notes/` requieren sincronización con la bóveda.
- Graphify es derivado y puede quedar desactualizado.
- Notion no debe convertirse en una segunda memoria narrativa.
