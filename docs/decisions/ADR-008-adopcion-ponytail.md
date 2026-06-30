# ADR-008: Adopción de Ponytail

## Estado

Aceptada el 2026-06-29.

## Contexto

El sistema necesita reglas reutilizables para limitar código, dependencias y contexto
generado por IA sin debilitar seguridad, contratos ni verificaciones.

## Decisión

Usar Ponytail como criterio global para tareas de código, después de comprender el
flujo y consultar el contexto y el grafo. La escalera prioriza no construir, reutilizar,
stdlib, capacidades nativas, dependencias instaladas y el mínimo código funcional.

Antes del cierre de cambios de código relevantes se realiza una revisión de
complejidad. La regla se documenta de forma portable para que siga aplicando cuando la
skill no esté instalada.

## Consecuencias

- Menos abstracciones, dependencias y contexto innecesarios.
- Los prompts de proyectos nuevos y migrados comparten el mismo criterio.
- No se atribuyen al repositorio ahorros de tokens o líneas que no puedan medirse.
- Seguridad, validación, prevención de pérdida de datos, accesibilidad, requisitos y
  verificaciones mínimas quedan fuera de cualquier simplificación.
