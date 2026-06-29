# Obsidian

[[Obsidian]] y esta bóveda son la fuente central de documentación humana de
[[Sistema de Trazabilidad]].

Aquí viven decisiones, arquitectura, reuniones, lecciones, bitácora y contexto de
proyectos. Las métricas viven en [[Notion]]; las relaciones derivadas, en [[Graphify]].

Regla práctica: documentar contexto durable, no copiar cada cambio ni cada métrica.

## Estructura por proyecto

```text
Proyectos/<Proyecto>/
├── Resumen.md
├── Estado actual.md
├── Sesiones/
├── Decisiones/
└── Arquitectura/
```

Las herramientas de IA leen el resumen, estado y última sesión antes de consultar
[[Graphify]] y el código. [[Notion]] no forma parte de esa lectura rutinaria.
