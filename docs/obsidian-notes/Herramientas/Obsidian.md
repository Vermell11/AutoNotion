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

Las herramientas de IA leen el contrato y la cápsula, la sesión abierta si existe y
consultan [[Graphify]] con presupuesto 600. Abren máximo tres fuentes. Reglas, resumen,
estado, ADR y sesiones históricas se cargan bajo demanda. [[Notion]] no participa en
esa lectura.

`Sesiones/En curso.md` se mantiene durante el trabajo activo. Al cierre confirmado se
convierte en la nota fechada de la versión usando [[Plantilla - Sesión de proyecto]].
Debe permanecer bajo 500 tokens estimados y conservar solo reto, resultado, decisiones,
validación y continuidad.

Cada `Resumen.md` de proyecto debe recordar que una tarea terminada no equivale a una
sesión cerrada. La IA muestra primero el borrador de cierre y solicita confirmación
humana explícita; sin ella, no publica una fila de sesión en [[Notion]].
