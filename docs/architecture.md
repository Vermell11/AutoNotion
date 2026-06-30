# Arquitectura inicial

## Límites de responsabilidad

| Sistema | Autoridad | No debe asumir |
|---|---|---|
| Notion | actividades y datos medibles | documentación técnica extensa |
| Obsidian | conocimiento y decisiones humanas | métricas transaccionales |
| Graphify | relaciones técnicas derivadas | decisiones o hechos no presentes en fuentes |
| Ponytail | criterio de implementación mínima | sustituir fuentes, pruebas o controles |
| Este repositorio | adaptadores, contratos y operación | convertirse en una cuarta fuente de verdad |

## Flujo operativo

```text
key.txt / NOTION_API_KEY
          |
          v
config -> NotionClient -> API Notion (lectura y cierres estructurados)

AGENTS / CLAUDE -> PROJECT_CONTEXT -> reglas globales -> reglas del proyecto
                  -> resumen + última sesión + En curso -> Graphify
                  -> Ponytail -> código mínimo + verificación

propuesta -> confirmación -> Obsidian/Graphify/pruebas -> commit final
          -> close-session --dry-run -> tag local -> close-session
          -> status=completed -> push main/tag
```

Notion no participa en la lectura rutinaria de contexto por IA. Conserva métricas,
sesiones y datos compartibles por API. No existen aún sincronización automática,
disparadores por cambios, reportes ni tareas programadas.

Una tarea completada no activa el cierre. Sin confirmación humana explícita después de
mostrar el borrador, la sesión sigue abierta y no se escribe su fila en Notion.

Obsidian separa reglas globales de `Proyectos/<Proyecto>/Reglas.md`. Las reglas locales
especializan el repositorio y no pueden contradecir las globales.

## Capas

- `config.py`: resolución de credenciales y valores operativos.
- `notion_client.py`: transporte, reintentos, errores y paginación.
- `closing.py`: contrato, preflight, idempotencia y reanudación del cierre.
- `session.py`: duración determinista entre timestamps con zona horaria.
- `cli.py`: interfaz para lectura y cierre compartido.
- `scripts/`: ejecución desde el checkout.
- `tests/`: contratos sin llamadas reales.

Las futuras integraciones deben depender del cliente, no duplicar llamadas HTTP.
