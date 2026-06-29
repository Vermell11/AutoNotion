# 2026-06-28 Reglas globales y por proyecto

## Estado

Aceptada.

## Decisión

[[Sistema de Trazabilidad]] separa sus reglas en dos capas:

- [[Reglas globales del Sistema de Trazabilidad]] contiene las políticas obligatorias
  para todos los proyectos.
- `Proyectos/<Proyecto>/Reglas.md` contiene únicamente convenciones locales.

Las reglas del proyecto pueden especializar, pero nunca contradecir, las globales.
`PROJECT_CONTEXT.md` enlaza ambas capas sin duplicar su contenido.

Las reglas globales fijan el flujo de inicio, el uso de tags Git anotados e inmutables
y la espera obligatoria hasta que el usuario indique que desea cargar la sesión en
[[Notion]] y confirme el borrador de cierre.

Relacionado con [[Obsidian]], [[Notion]], [[Graphify]] y
[[Reglas globales del Sistema de Trazabilidad]].
