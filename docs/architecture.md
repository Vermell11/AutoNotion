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

AGENTS / CLAUDE -> PROJECT_CONTEXT -> En curso (si existe)
                  -> Graphify --budget 600 -> máximo 3 fuentes
                  -> contexto adicional bajo demanda
                  -> Ponytail -> código mínimo + verificación

propuesta -> confirmación -> Obsidian/Graphify/pruebas -> commit final
          -> close-project prepare -> confirmación del borrador
          -> close-project finalize -> tag local -> Notion completed
          -> push atómico main/tag
```

Notion no participa en la lectura rutinaria de contexto por IA. Conserva métricas,
sesiones y datos compartibles por API. El informe semanal lo consulta bajo demanda y
genera un PDF local; no existen sincronización automática, disparadores por cambios
ni tareas programadas.

Una tarea completada no activa el cierre. Sin confirmación humana explícita después de
mostrar el borrador, la sesión sigue abierta y no se escribe su fila en Notion.

Obsidian separa reglas globales de `Proyectos/<Proyecto>/Reglas.md`. Las reglas locales
especializan el repositorio y no pueden contradecir las globales.

El flujo usa divulgación progresiva. Reglas extensas, resumen, estado, ADR y sesiones
históricas son contexto frío; no se cargan en cada inicio. `PROJECT_CONTEXT.md` es una
cápsula derivada y compacta, no una nueva fuente de verdad.

## Capas

- `config.py`: resolución de credenciales y valores operativos.
- `notion_client.py`: transporte, reintentos, errores y paginación.
- `closing.py`: contrato, preflight, idempotencia y reanudación del cierre.
- `project_close.py`: barreras Git y coordinación prepare/finalize.
- `excel_export.py`: descubrimiento recursivo, normalización y libro por data source.
- `weekly_report.py`: filtro semanal, indicadores y PDF determinista.
- `session.py`: duración determinista entre timestamps con zona horaria.
- `cli.py`: interfaz para lectura y cierre compartido.
- `scripts/`: ejecución desde el checkout.
- `tests/`: contratos sin llamadas reales.

Las futuras integraciones deben depender del cliente, no duplicar llamadas HTTP.
