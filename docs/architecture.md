# Arquitectura inicial

## Límites de responsabilidad

| Sistema | Autoridad | No debe asumir |
|---|---|---|
| Notion | actividades y datos medibles | documentación técnica extensa |
| Obsidian | conocimiento y decisiones humanas | métricas transaccionales |
| Graphify | relaciones técnicas derivadas | decisiones o hechos no presentes en fuentes |
| Este repositorio | adaptadores, contratos y operación | convertirse en una cuarta fuente de verdad |

## Flujo de Fase 1

```text
key.txt / NOTION_API_KEY
          |
          v
config -> NotionClient -> API Notion (lectura: identidad y descubrimiento)

docs del repositorio <----alineación manual----> bóveda Cerebro

repositorios --(futuro: extract/update)--> graphify-out --(consulta)--> agentes
```

No existe aún escritura en Notion, sincronización, disparador por cambios ni tarea
programada. Esa ausencia es deliberada para mantener el sistema auditable.

## Capas

- `config.py`: resolución de credenciales y valores operativos.
- `notion_client.py`: transporte, reintentos, errores y paginación.
- `cli.py`: interfaz humana y salida apta para automatización futura.
- `scripts/`: ejecución desde el checkout.
- `tests/`: contratos sin llamadas reales.

Las futuras integraciones deben depender del cliente, no duplicar llamadas HTTP.
