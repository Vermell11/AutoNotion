# Estrategia de Notion

## Contrato inicial

El cliente usa la versión `2026-03-11` de la API. Verifica autenticación con
`GET /v1/users/me` y descubre fuentes mediante `POST /v1/search`, filtrando
`object = data_source` y recorriendo cursores.

Desde 2025, una base de datos es un contenedor y puede tener varias fuentes de datos.
Las automatizaciones futuras deben guardar `data_source_id`, no asumir que
`database_id` identifica la tabla operativa.

La validación del 2026-06-28 fue exitosa y descubrió nueve fuentes visibles. Como
existen nombres duplicados, la selección canónica se realiza exclusivamente por ID.

## Fuente canónica de actividades

En la página contenedora del sistema, **Base de datos de trabajo** es un encabezado.
La base incrustada inmediatamente posterior es **Reporte de Tickets**, cuya fuente
operativa canónica es:

`033bc5d6-9357-83c6-b71e-07d61caa648f`

Mapeo acordado:

- Actividad → `Titulo`
- Categoría → `Category`
- Fecha y hora → `Date Reported`
- Horas invertidas → `Horas`
- Descripción → `Descripcion`
- Estado → `Status`

Los agentes deben usar el `data_source_id`, no el encabezado, el nombre de una vista ni
el ID de la página contenedora.

## Fuente canónica de sesiones por proyecto

La base **Proyectos** conserva una fila nueva por cada sesión cerrada y está relacionada
bidireccionalmente con las actividades mediante `Proyecto` ↔ `Actividades`.

- Database ID: `d0d752eb-27f7-4733-a4fb-342db85ab9bb`
- Data source ID: `c36049cf-9d28-4999-8f0a-f0e15deaa8b4`
- Campos de cierre: `Nombre`, `Estado`, `Ámbito`, `Inicio`, `Fin`, `Fecha sesión`,
  `Duración minutos`, `Horas`, `Reto o compromiso`, `Resuelto`, `Resumen`, `Versión`,
  `Tag Git`, `Commit Git`, `Repositorio` y `Obsidian`.

`Nombre` siempre procede de la carpeta raíz y puede repetirse. La identidad idempotente
es `Nombre + Versión + Commit Git`; nunca se deduplica solo por nombre. Cada cierre
registra reto, resolución, resumen y evidencia Git.

## Política de lectura y escritura

- Codex y Claude Code no leen Notion para reconstruir contexto normal.
- El contexto narrativo se obtiene de Obsidian y el técnico de Graphify.
- Completar una tarea, resolver el reto o pausar el trabajo no cierra la sesión.
- La IA espera a que el usuario diga explícitamente cuándo desea cerrar o cargar lo
  realizado. Solo entonces muestra un borrador con reto, resultado, resumen, tiempos,
  versión y evidencia Git, y pregunta si confirma cerrar y registrar en Notion.
- Sin una respuesta afirmativa inequívoca, la sesión permanece abierta y no se crea ni
  actualiza ninguna fila de sesión.
- Tras la confirmación, Notion se escribe una sola vez. Se consulta para reportes,
  reconciliación o acceso explícito por API.
- `Inicio` y `Fin` llevan zona horaria.
- `Duración minutos` conserva el trabajo activo y `Horas` presenta su decimal
  redondeado para dashboards. Las pausas prolongadas se documentan y excluyen; inicio
  y fin conservan el tiempo de pared para auditoría.
- El resumen de Notion es conciso y enlaza la memoria detallada de Obsidian.

## Modelo propuesto para Fase 2

Una fuente principal **Actividades**:

- Nombre: título.
- Categoría: select o relación a catálogo.
- Prioridad: select.
- Horas: número decimal.
- Estado: status.
- Proyecto: relación a **Proyectos**.
- Fecha: date.
- Responsable: people.
- Ámbito: select (`Laboral`, `Personal`).
- Enlace Obsidian: URL o texto estable.
- Repositorio / referencia Graphify: texto o URL.
- Origen y fecha de registro: campos de auditoría.

Conviene separar **Proyectos** y, si se requiere gobierno central, **Categorías**.
Los reportes deben ser vistas o consumidores de estas fuentes, no copias de datos.

## Reglas

- Identificadores de fuentes en configuración local, nunca incrustados en lógica.
- Las creaciones no se reintentan a ciegas: `close-session` reconcilia antes de
  continuar y reanuda actividades faltantes.
- El preflight valida esquemas y opciones reales de select/status.
- Confirmación humana antes de registrar una actividad durante la siguiente fase.
- Fechas almacenadas con zona horaria explícita; horas como duración, no texto.
- Descubrimiento no implica permisos de escritura.
