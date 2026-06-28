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
- Campos: `Nombre`, `Estado`, `Ámbito`, `Responsable`, `Inicio`, `Fin`, `Objetivo`,
  `Repositorio` y `Obsidian`.

`Nombre` siempre procede de la carpeta raíz y puede repetirse. La identidad de una
sesión la forman su página, fecha, versión y commit; nunca se deduplica solo por nombre.
Cada cierre registra reto, resolución, resumen y evidencia Git.

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
- Operaciones de escritura idempotentes con una clave externa.
- Confirmación humana antes de registrar una actividad durante la siguiente fase.
- Fechas almacenadas con zona horaria explícita; horas como duración, no texto.
- Descubrimiento no implica permisos de escritura.
