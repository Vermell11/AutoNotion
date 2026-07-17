# Estado actual y avance al propósito final

## Propósito último

Construir un ecosistema personal donde:

- Notion conserve actividades, sesiones, horas, estados y datos compartibles por API.
- Obsidian sea la memoria humana y contextual por proyecto.
- Graphify mantenga relaciones técnicas derivadas del código.
- Codex y Claude Code continúen desde la última sesión sin reconstruir contexto.

## Capacidades actuales

La aplicación es una base Python pequeña que actualmente:

- Carga `NOTION_API_KEY` o, temporalmente, `public/apikey/key.txt` en UTF-8/UTF-16.
- Verifica autenticación contra Notion.
- Descubre y pagina fuentes de datos.
- Consulta esquemas, bases, páginas y bloques.
- Crea bases, páginas Markdown y filas con propiedades completas.
- Actualiza esquemas, propiedades y contenido Markdown.
- Envía duplicados a la papelera.
- Distingue operaciones reintentables de creaciones no idempotentes.
- Calcula duración exacta de sesiones a partir de timestamps con zona horaria.
- Ejecuta preflight de conexión y esquemas para cierres externos.
- Registra sesiones y actividades con identidad idempotente y reanudación parcial.
- Coordina cierre Git + Notion en dos fases y publica rama/tag de forma atómica,
  incluso sobre un remoto inicialmente vacío.
- Mantiene pruebas unitarias sin llamadas reales.
- Exporta fuentes visibles o bases descendientes de una página a Excel.
- Genera un informe semanal PDF desde `Base de datos de trabajo`.

El CLI público ofrece `check`, `discover`, `export-excel`, `close-session` y
`close-project`; los
wrappers `exportExcel.py` y `reporteSemanal.py` cubren ejecuciones sin argumentos.

## Avance por capacidad

| Capacidad final | Estado | Evidencia / brecha |
|---|---|---|
| Arquitectura y seguridad base | Completa | ADR, reglas, `.gitignore`, secreto fuera de Git |
| Documentación humana en Obsidian | Completa para Notion | Estructura por proyecto y sesiones |
| Contexto técnico Graphify | Operativo | Grafo local, reporte y actualización incremental |
| Continuidad Codex/Claude | Operativa | `PROJECT_CONTEXT.md`, `AGENTS.md`, `CLAUDE.md` |
| Presupuesto de contexto | En optimización | Divulgación progresiva y pruebas V1.4 |
| Ledger de sesiones en Notion | Operativo | Una fila nueva por cierre, métricas y evidencia Git |
| Registro de actividades | Operativo asistido | `close-session` crea y relaciona actividades confirmadas |
| Medición automática de sesiones | Parcial | Cálculo implementado; cierre aún es asistido |
| Reportes y dashboards | Parcial | Primer informe semanal PDF; sin dashboard |
| Detección automática de cambios | Pendiente | No implementada |
| Sincronización automática | Pendiente | Deliberadamente fuera de alcance |
| Correos y tareas programadas | Pendiente | Deliberadamente fuera de alcance |

## Lectura honesta del avance

La fundación y la continuidad entre sesiones están resueltas. El sistema todavía no es
una plataforma automatizada: requiere una IA o persona para ejecutar el cierre, escribir
la fila de Notion y mantener Obsidian. El siguiente salto de valor es distribuir el
conector como comando portable y ampliar la reportería según uso real.

V1.4 aplica divulgación progresiva: contrato y cápsula compactos, Graphify con
presupuesto 600, máximo tres fuentes y contexto frío bajo demanda. El baseline
documental estimado fue ~6300 tokens al iniciar y ~2425 al cerrar.

El cierre asistido exige mostrar un borrador y obtener confirmación humana
explícita. La IA espera a que el usuario indique cuándo desea cargar la sesión;
resolver una tarea o el reto no autoriza escribir en Notion.

La sesión abierta y su versión histórica usan un formato compacto. Notion recibe solo
trabajo y resultado; Obsidian conserva decisiones y continuidad.

## Riesgos vigentes

- `key.txt` sigue siendo un fallback local y debe migrarse a llavero o entorno.
- Las copias de notas en `docs/obsidian-notes/` requieren sincronización con la bóveda.
- Graphify es derivado y puede quedar desactualizado.
- Notion no debe convertirse en una segunda memoria narrativa.
