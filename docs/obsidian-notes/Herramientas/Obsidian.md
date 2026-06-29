# Obsidian

[[Obsidian]] y esta bóveda son la fuente central de documentación humana de
[[Sistema de Trazabilidad]].

Aquí viven decisiones, arquitectura, reuniones, lecciones, bitácora y contexto de
proyectos. Las métricas viven en [[Notion]]; las relaciones derivadas, en [[Graphify]].

Regla práctica: documentar contexto durable, no copiar cada cambio ni cada métrica.

## Estructura por proyecto

```text
Reglas/
└── Reglas globales del Sistema de Trazabilidad.md

Proyectos/<Proyecto>/
├── Resumen.md
├── Reglas.md
├── Estado actual.md
├── Sesiones/
│   ├── En curso.md
│   └── <Fecha> - <Versión>.md
├── Decisiones/
└── Arquitectura/
```

Las reglas globales aplican a todos los proyectos. `Reglas.md` contiene solo
convenciones locales y no puede contradecirlas.

Las herramientas de IA leen `AGENTS.md` o `CLAUDE.md`, consultan `PROJECT_CONTEXT.md`
como índice, leen las reglas globales y locales, el resumen y la última sesión, y
después consultan [[Graphify]] antes del código. [[Notion]] no forma parte de esa
lectura rutinaria.

`Sesiones/En curso.md` se mantiene durante el trabajo activo. Al cierre confirmado se
convierte en la nota fechada de la versión usando [[Plantilla - Sesión de proyecto]].
Debe resumir acuerdos, evidencia, estado y continuidad, no reproducir la conversación.

Cada `Resumen.md` de proyecto debe recordar que una tarea terminada no equivale a una
sesión cerrada. La IA muestra primero el borrador de cierre y solicita confirmación
humana explícita; sin ella, no publica una fila de sesión en [[Notion]].
