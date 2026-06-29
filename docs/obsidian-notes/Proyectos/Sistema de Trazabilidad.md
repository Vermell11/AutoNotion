# Sistema de Trazabilidad

> Esta nota se conserva como entrada histórica. El proyecto activo vive en
> [[Proyectos/Notion/Resumen]].

## Propósito

Centralizar medición en [[Notion]], conocimiento humano en [[Obsidian]] y contexto
técnico derivado en [[Graphify]].

## Estado

Fase 1: arquitectura base, seguridad, cliente de lectura para Notion y estrategia
documental. No hay sincronización ni automatizaciones programadas.

La extracción inicial y sus actualizaciones de [[Graphify]] comenzaron el 2026-06-28.
Las métricas vigentes se consultan en `GRAPH_REPORT.md`; no se duplican aquí porque el
grafo es derivado y cambia con cada actualización.

La conexión de [[Notion]] fue validada el 2026-06-28 y ve nueve fuentes. Como hay
nombres duplicados, los destinos se seleccionan por ID.

La fuente canónica de actividades ya fue identificada bajo el encabezado **Base de
datos de trabajo**: `033bc5d6-9357-83c6-b71e-07d61caa648f`. El mapeo está documentado
en [[Notion]].

La fuente canónica de proyectos es `c36049cf-9d28-4999-8f0a-f0e15deaa8b4` y está
relacionada bidireccionalmente con las actividades.

## Fuentes de verdad

- [[Notion]]: actividades, horas, estado, proyecto, fechas y reportes.
- [[Obsidian]]: decisiones, arquitectura, reuniones, lecciones y bitácora.
- [[Graphify]]: relaciones de código y dependencias derivadas.

## Decisiones

- [[2026-06-28 Arquitectura inicial]]
- [[2026-06-28 Trazabilidad por sesiones]]
- [[2026-06-28 Confirmación explícita de cierre]]
- [[2026-06-28 Reglas globales y por proyecto]]
- [[2026-06-28 Memoria de sesiones para continuidad]]

## Reglas

- Reglas transversales: [[Reglas globales del Sistema de Trazabilidad]].
- Reglas locales del proyecto activo: [[Proyectos/Notion/Reglas]].
- Las reglas locales especializan, pero no contradicen, las globales.

## Regla de sesiones y versiones

- El nombre del proyecto siempre es el nombre de la carpeta raíz.
- Cada sesión define al inicio un reto o compromiso verificable.
- Terminar una tarea o resolver el reto no cierra la sesión.
- La IA espera a que el usuario indique cuándo desea cargar la sesión. Solo entonces
  muestra el borrador y pregunta si confirma cerrar y registrar en [[Notion]].
- Sin una respuesta afirmativa inequívoca, no escribe la fila.
- Cada cierre confirmado crea una fila nueva en **Proyectos** con resumen y resultado.
- No existe una fila global que se sobrescriba entre sesiones.
- Cada versión cerrada lleva un tag Git anotado e inmutable.
- La primera versión de este proyecto es `V1.0`.

## Plantillas

- [[Prompts de Trazabilidad]]
- [[Prompt - Integrar proyecto nuevo al Sistema de Trazabilidad]]
- [[Prompt - Migrar proyecto existente al Sistema de Trazabilidad]]
- [[Plantilla - Sesión de proyecto]]

## Siguientes hitos

- Implementar un comando de cierre idempotente y reconciliable.
- Implementar el flujo confirmado de actividades.
- Diseñar reportes y dashboards después de estabilizar la captura.

## Riesgos actuales

- La credencial todavía vive en un archivo local transitorio.
- Puede haber divergencia entre documentación del código y esta bóveda.
- Las salidas de [[Graphify]] pueden quedar obsoletas o contener inferencias.
