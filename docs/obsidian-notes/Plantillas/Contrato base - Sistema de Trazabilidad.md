# Contrato base - Sistema de Trazabilidad

Este contrato se aplica a proyectos nuevos y migrados. Las plantillas de entrada solo
definen el modo y el contexto variable.

## Constantes

- Bóveda:
  `/Users/andresortegacorpus/Library/Mobile Documents/com~apple~CloudDocs/code/Brain/Cerebro`
- Sesiones en Notion: `c36049cf-9d28-4999-8f0a-f0e15deaa8b4`
- Actividades en Notion: `033bc5d6-9357-83c6-b71e-07d61caa648f`
- Conector:
  `/Users/andresortegacorpus/Library/Mobile Documents/com~apple~CloudDocs/code/Notion/scripts/notion.py`

## Fuentes

- Notion: sesiones, actividades y métricas.
- Obsidian: contexto humano, decisiones y continuidad.
- Graphify: índice técnico derivado.
- Git: implementación y evidencia versionada.

## Contrato por proyecto

1. El nombre es el de la carpeta raíz.
2. `AGENTS.md` contiene solo invariantes, carga progresiva, Ponytail y barrera de
   cierre. `CLAUDE.md` apunta a ese contrato.
3. `PROJECT_CONTEXT.md` es una cápsula menor a 400 tokens estimados: identidad,
   propósito, estado, último resultado, reto actual y punteros.
4. Arranque: leer contrato y cápsula; leer sesión abierta si existe; consultar
   Graphify con `--budget 600`; abrir máximo tres fuentes. Reglas extensas, resumen,
   estado, ADR y sesiones históricas se cargan bajo demanda.
5. Ponytail es capacidad global, no código copiado al repositorio. Para código:
   comprender el flujo, reutilizar, preferir stdlib/nativo y hacer el cambio mínimo.
   Nunca simplificar seguridad, validación, prevención de pérdida de datos,
   accesibilidad, requisitos ni una prueba útil.
6. Obsidian usa `Proyectos/<Proyecto>/` con `Resumen.md`, `Estado actual.md`,
   `Reglas.md`, `Sesiones/`, `Decisiones/` y `Arquitectura/`.
7. Las sesiones siguen [[Plantilla - Sesión de proyecto]] y no superan 500 tokens
   estimados. No copian la conversación ni inventarios disponibles en Git.
8. Graphify se extrae una vez por repositorio y después se actualiza por cambios
   relevantes. No se reconstruye en cada inicio.
9. Notion no se lee para contexto. El resumen de cierre contiene solo trabajo y
   resultado, máximo 120 palabras; las actividades, máximo 80 palabras. El resto queda
   en Obsidian o propiedades estructuradas.
10. Una tarea terminada no cierra la sesión. Solo una petición y confirmación explícitas
    autorizan el flujo de `docs/session-close.md`.
11. Nunca mostrar, copiar ni versionar secretos. Los proyectos no implementan clientes
    Notion paralelos ni copian `key.txt`.

## Presupuesto

El arranque predeterminado debe permanecer en ≤1500 tokens estimados, incluida la
consulta inicial del grafo. Si requiere más contexto, la IA explica qué evidencia falta
y carga solo la fuente necesaria.

Relacionado con [[Sistema de Trazabilidad]], [[Ponytail]], [[Graphify]], [[Obsidian]] y
[[Notion]].
