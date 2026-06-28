# Sistema de Trazabilidad

## Propósito

Centralizar medición en [[Notion]], conocimiento humano en [[Obsidian]] y contexto
técnico derivado en [[Graphify]].

## Estado

Fase 1: arquitectura base, seguridad, cliente de lectura para Notion y estrategia
documental. No hay sincronización ni automatizaciones programadas.

La extracción inicial y su actualización incremental de [[Graphify]] se completaron el
2026-06-28 con 188 nodos, 273 aristas y 18 comunidades. El diagnóstico final quedó
sin extremos faltantes, aristas colgantes, bucles ni colapsos.

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

## Regla de sesiones y versiones

- El nombre del proyecto siempre es el nombre de la carpeta raíz.
- Cada sesión define al inicio un reto o compromiso verificable.
- Cada cierre crea una fila nueva en **Proyectos** con resumen y resultado del reto.
- No existe una fila global que se sobrescriba entre sesiones.
- Cada versión cerrada lleva un tag Git anotado e inmutable.
- La primera versión de este proyecto es `V1.0`.

## Plantillas

- [[Prompts de Trazabilidad]]
- [[Prompt - Integrar proyecto nuevo al Sistema de Trazabilidad]]
- [[Prompt - Migrar proyecto existente al Sistema de Trazabilidad]]

## Siguientes hitos

- Validar el modelo de datos de Notion.
- Publicar este repositorio en Git después de verificar secretos e ignorados.
- Usar actualizaciones incrementales de Graphify tras cambios arquitectónicos.
- Diseñar confirmación e idempotencia antes de cualquier escritura.

## Riesgos actuales

- La credencial todavía vive en un archivo local transitorio.
- La carpeta aún no es un repositorio Git.
- Puede haber divergencia entre documentación del código y esta bóveda.
- Las salidas de [[Graphify]] pueden quedar obsoletas o contener inferencias.
