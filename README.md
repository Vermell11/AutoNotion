# Sistema de Trazabilidad

Base personal para centralizar actividades y medición en Notion, conocimiento humano
en Obsidian y contexto técnico derivado en Graphify.

## Estado

Fase 1: arquitectura, seguridad, cliente de lectura para Notion y documentación.
No incluye sincronización, reportes, correo ni tareas programadas.

## Inicio rápido

Requiere Python 3.11 o posterior y no tiene dependencias externas.

```bash
python3 scripts/notion.py check
python3 scripts/notion.py discover
python3 -m unittest discover -s tests
```

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
están en [AGENTS.md](AGENTS.md).

## Versionado

Cada versión cerrada usa un tag Git anotado e inmutable. La versión inicial es `V1.0`.
Al finalizar cada sesión se crea una fila nueva en Notion con reto, resultado, resumen,
versión, tag y commit.

## Comandos

- `check`: valida la credencial con `GET /v1/users/me`.
- `discover`: pagina `POST /v1/search` y lista las fuentes de datos compartidas.
- `discover --json`: produce JSON seguro para herramientas posteriores.

El descubrimiento solo puede ver contenido al que la conexión o usuario tenga acceso.
Si faltan fuentes, revisa permisos y el uso de **Add connections** en Notion.
