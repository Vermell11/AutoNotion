# Sistema de Trazabilidad

Base personal para centralizar actividades y medición en Notion, conocimiento humano
en Obsidian y contexto técnico derivado en Graphify.

## Estado

Versión V1.4. El cliente soporta lectura y escritura controlada en Notion,
documentación y memoria de sesiones por proyecto en Obsidian, Graphify y continuidad
entre Codex y Claude Code. Incluye un cierre idempotente compartido y reglas Ponytail
para minimizar implementación y contexto. Incluye exportación a Excel y un primer
informe semanal PDF. No incluye sincronización, correo ni tareas programadas.

El arranque usa contrato y cápsula compactos, Graphify con presupuesto inicial 600 y
máximo tres fuentes. El resto del contexto se carga bajo demanda.

## Inicio rápido

Requiere Python 3.11 o posterior.

```bash
python3 -m pip install -e .
python3 scripts/notion.py check
python3 scripts/notion.py discover
python3 scripts/notion.py export-excel
python3 scripts/exportExcel.py
python3 scripts/reporteSemanal.py
python3 scripts/notion.py close-session --payload /tmp/proyecto-v1-notion.json --dry-run
python3 scripts/notion.py close-project prepare --project /ruta --payload /tmp/cierre.json
python3 -m unittest discover -s tests
```

`close-session` valida y registra una sesión con sus actividades sin duplicar cierres
anteriores. `close-project` añade las barreras Git y coordina `prepare`/`finalize` para
que un fallo no publique un tag sobre el commit equivocado. Consulta
[el contrato y el orden de cierre](docs/session-close.md) antes de usarlo.

`export-excel` crea en `public/output/` una hoja índice y una hoja por fuente visible.
`--page-id` limita el alcance a las bases descendientes de una página y
`--include-content` añade el cuerpo textual de cada fila/página.

`scripts/exportExcel.py` aplica automáticamente la página principal configurada,
incluye el contenido y guarda el resultado en `public/output/`.

`scripts/reporteSemanal.py` consulta `Base de datos de trabajo`, filtra la semana
actual de lunes a domingo y genera un PDF visual en `public/output/`, sin modificar
Notion. Consulta [el contrato del informe](docs/weekly-report.md).

El cliente busca la credencial en este orden:

1. `NOTION_API_KEY` en el entorno (opción objetivo).
2. `public/apikey/key.txt` como compatibilidad temporal de Fase 1.

Nunca pases el token como argumento de línea de comandos: quedaría en el historial y
podría aparecer en la lista de procesos.

## Arquitectura

```text
src/trazabilidad/       cliente y configuración reutilizables
scripts/                entradas operativas mínimas
config/                 configuración no secreta
docs/                   arquitectura, seguridad y estrategias
tests/                  pruebas sin acceso a la red
public/apikey/          compatibilidad local; ignorado por Git
```

Las decisiones y estrategias están en [docs/](docs/README.md). Las reglas para agentes
están en [AGENTS.md](AGENTS.md). Toda IA debe comenzar por
[PROJECT_CONTEXT.md](PROJECT_CONTEXT.md).

## Versionado

Cada versión cerrada usa un tag Git anotado e inmutable. La versión inicial es `V1.0`.
Al finalizar cada sesión se crea una fila nueva en Notion con reto, resultado, resumen,
versión, tag y commit.

## Comandos

- `check`: valida la credencial con `GET /v1/users/me`.
- `discover`: pagina `POST /v1/search` y lista las fuentes de datos compartidas.
- `discover --json`: produce JSON seguro para herramientas posteriores.
- `export-excel`: pagina todas las filas y genera un `.xlsx` sin modificar Notion.
- `reporteSemanal.py`: genera un PDF semanal de solo lectura con indicadores y detalle.

El descubrimiento solo puede ver contenido al que la conexión o usuario tenga acceso.
Si faltan fuentes, revisa permisos y el uso de **Add connections** en Notion.
