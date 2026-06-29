# ADR-004: Confirmación explícita de cierre

- Fecha: 2026-06-28
- Estado: aceptada

## Contexto

Completar una tarea o resolver el reto de una sesión no implica que el usuario haya
terminado de trabajar. Registrar el cierre en Notion antes de tiempo publica métricas,
resumen y versión incompletos.

## Decisión

- La IA espera a que el usuario diga explícitamente que desea cerrar o cargar en
  Notion lo realizado durante la sesión; no inicia ese flujo por inferencia.
- La IA prepara y muestra un borrador de cierre con reto, resultado, resumen, inicio,
  fin, duración, horas, versión, tag, commit y actividades relacionadas.
- Después pregunta explícitamente si el usuario confirma cerrar y registrar la sesión
  en Notion.
- Solo una respuesta afirmativa inequívoca autoriza el cierre.
- Sin confirmación, la sesión permanece abierta y no se crea ni actualiza su fila.
- Mensajes de continuidad, una tarea resuelta o una pausa no constituyen autorización.
- Después de la confirmación se ejecuta una sola vez el flujo de cierre y se reconcilia
  antes de reintentar una escritura cuyo resultado sea incierto.

## Consecuencias

- El usuario conserva control sobre el límite real de cada sesión.
- Notion solo contiene cierres deliberados y métricas completas.
- Codex, Claude Code y los prompts reutilizables aplican la misma barrera.
- El cierre sigue siendo asistido hasta implementar idempotencia automatizada.
