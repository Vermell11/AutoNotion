# 2026-06-28 Confirmación explícita de cierre

## Estado

Aceptada.

## Decisión

En cada proyecto, terminar una tarea, resolver el reto o pausar el trabajo no significa
que la sesión haya terminado.

Codex, Claude Code o cualquier otra IA esperan a que el usuario indique explícitamente
que desea cerrar o cargar lo realizado. Solo entonces muestran un borrador con reto,
resultado, resumen, inicio, fin, duración, horas, versión, tag, commit y actividades
relacionadas. Después deben preguntar explícitamente:
“¿Confirmas que deseas cerrar y registrar esta sesión en Notion?”.

Solo una respuesta afirmativa inequívoca autoriza el cierre. Sin ella, la sesión
permanece abierta y no se crea ni actualiza su fila en [[Notion]]. Mensajes como
“perfecto”, “procedamos” o la finalización de una tarea no constituyen autorización.

## Consecuencias

El usuario controla el límite real de la sesión, las métricas publicadas corresponden a
trabajo completo y todas las herramientas aplican la misma barrera de cierre.

Relacionado con [[Sistema de Trazabilidad]], [[Notion]], [[Obsidian]] y [[Graphify]].
