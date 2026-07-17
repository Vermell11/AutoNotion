# Notion

[[Notion]] es la fuente de verdad transaccional de [[Sistema de Trazabilidad]].

Almacena actividades, categorías, prioridades, horas, estado, proyecto, fecha,
responsable y reportes. La documentación extensa permanece en [[Obsidian]] y se enlaza.

El cliente verifica conexión, descubre fuentes y ofrece un cierre compartido e
idempotente. El secreto no debe aparecer en esta bóveda, registros ni control de
versiones.

## Fuente de actividades

En la página principal, el encabezado y la fuente operativa se llaman
**Base de datos de trabajo**. La fuente antes denominada **Reporte de Tickets**
conservó su identificador.

- `data_source_id`: `033bc5d6-9357-83c6-b71e-07d61caa648f`
- Actividad: `Titulo`
- Categoría: `Category`
- Fecha y hora: `Date Reported`
- Horas invertidas: `Horas`
- Descripción: `Descripcion`
- Estado: `Status`

Este ID es la referencia canónica. No seleccionar destinos únicamente por nombre.

## Fuente de sesiones por proyecto

La base **Proyectos** usa el `data_source_id`
`c36049cf-9d28-4999-8f0a-f0e15deaa8b4`.

`Proyectos` conserva una sola fila canónica por proyecto. `Nombre` siempre es el
nombre de la carpeta raíz y no debe repetirse en la tabla activa. El cierre hace
upsert de ese registro y agrega cada sesión al cuerpo de la página como bitácora
acumulada, además de relacionar actividades mediante `Proyecto` ↔ `Actividades`.

Terminar una tarea o resolver el reto no cierra la sesión. La IA espera a que el
usuario indique cuándo desea cargarla. Solo entonces muestra el borrador y pregunta
explícitamente si confirma cerrar y registrar la sesión en Notion. Sin una respuesta
afirmativa inequívoca, no se crea ni actualiza ninguna fila.

Codex y Claude Code no leen Notion para reconstruir contexto rutinario. La memoria vive
en [[Obsidian]] y el contexto técnico en [[Graphify]]. Notion es la capa de métricas,
reportes y exposición estructurada por API.

## Exportación Excel

`export-excel` pagina todas las filas y crea en `public/output/` un libro con hoja
`Índice` y una hoja por data source. Puede exportar todas las fuentes visibles o limitar
el recorrido a bases descendientes de una página con `--page-id`. `--include-content`
añade el cuerpo textual de cada fila/página. Es una operación de solo lectura.

Para uso directo, `python3 scripts/exportExcel.py` ejecuta la página principal,
incluye contenido y guarda automáticamente el archivo en `public/output/`.

## Conector compartido

Todo proyecto usa:

```text
python3 "/Users/andresortegacorpus/Library/Mobile Documents/com~apple~CloudDocs/code/Notion/scripts/notion.py" close-session
```

El payload sigue `config/session-close.example.json`. Primero se ejecuta con
`--dry-run`; si falla, no se crea ni publica el tag. Cuando pasa, se crea el tag local,
se ejecuta el cierre real y se exige `status=completed` antes de publicar Git.

La identidad del proyecto es `Nombre`; el SHA completo queda como evidencia de la
última sesión. El comando reutiliza el proyecto existente y completa actividades
faltantes, por lo que puede reanudarse después de una respuesta incierta sin
duplicar filas en `Proyectos`.

El preflight también valida las opciones reales de `Estado`, `Ámbito`, `Category` y
`Status`. Los agentes no inventan valores; solicitan una decisión cuando el mapeo no es
inequívoco.
