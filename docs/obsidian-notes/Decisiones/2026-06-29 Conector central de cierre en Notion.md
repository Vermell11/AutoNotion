# 2026-06-29 Conector central de cierre en Notion

## Estado

Aceptada.

## Decisión

Todos los proyectos usan un único comando del repositorio `Notion` para cerrar sesiones
y registrar actividades. Ningún proyecto consumidor copia la API Key ni implementa un
cliente paralelo.

El cierre usa un payload JSON sin secretos, un preflight real con `--dry-run` y la
identidad de proyecto `Nombre`. El SHA debe ser completo como evidencia de la
sesión. Una ejecución posterior reutiliza el proyecto existente y completa
actividades pendientes.

El orden obligatorio es:

`documentación/Graphify/pruebas → commit final → dry-run → tag local → cierre Notion → status=completed → push main/tag`

Si el conector o el preflight fallan, la sesión permanece abierta y Git no se publica.
No se hacen commits posteriores al tag para completar URL o metadata.

Relacionado con [[Notion]], [[Sistema de Trazabilidad]],
[[Reglas globales del Sistema de Trazabilidad]] y
[[2026-06-28 Memoria de sesiones para continuidad]].
