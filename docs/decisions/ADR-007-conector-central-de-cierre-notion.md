# ADR-007: Conector central de cierre en Notion

- Fecha: 2026-06-29
- Estado: aceptada

## Contexto

Los prompts estándar definían campos e IDs de Notion, pero asumían que cada agente
disponía de un conector de escritura. Un proyecto consumidor pudo completar Git,
Obsidian y Graphify, pero dejó el registro de Notion como payload pendiente porque no
tenía cliente ejecutable ni acceso autorizado al secreto central.

## Decisión

- El repositorio `Notion` ofrece un único comando `close-session`.
- Los proyectos consumidores invocan ese comando por su ruta canónica y nunca copian
  credenciales ni código del cliente.
- El payload es JSON validado y no contiene secretos.
- `--dry-run` verifica conexión, esquemas e identidad sin escribir.
- La identidad idempotente del proyecto es `Nombre`; las sesiones se preservan como
  bitácora acumulada y actividades relacionadas.
- Las actividades se identifican por título y relación con la sesión.
- Una ejecución posterior reanuda cierres parciales sin duplicar filas.
- El tag no se publica hasta que Notion confirme el cierre.

## Consecuencias

- Los prompts pasan de describir un cierre a disponer de una operación ejecutable.
- Los secretos permanecen centralizados.
- Los fallos de red pueden reconciliarse de forma segura.
- El cierre requiere que el repositorio central siga disponible en su ruta canónica.
