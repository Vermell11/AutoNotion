# Contrato para agentes

## Invariantes

- Notion conserva métricas; Obsidian, conocimiento; Graphify, relaciones derivadas.
- Nunca mostrar, documentar ni versionar secretos. Usar `NOTION_API_KEY`; `key.txt`
  solo mediante el cargador autorizado.
- No usar Notion para reconstruir contexto rutinario.
- Una tarea terminada no cierra la sesión. Solo una confirmación explícita autoriza
  escribir el cierre en Notion.
- Cada cierre usa un tag Git anotado e inmutable.

## Inicio progresivo

1. Leer este archivo y `PROJECT_CONTEXT.md`.
2. Leer `Sesiones/En curso.md` solo si el índice indica que existe.
3. Consultar el grafo con términos de la tarea y `--budget 600`; abrir máximo tres
   fuentes y ampliar a 1200 solo si falta evidencia.
4. Cargar reglas, ADR, estado o historia solo cuando la tarea lo requiera.

## Código

- Activar Ponytail: comprender el flujo, omitir, reutilizar, preferir stdlib/nativo y
  escribir el cambio mínimo. Antes de editar, localizar llamadores.
- No simplificar seguridad, validación en límites de confianza, prevención de pérdida
  de datos, accesibilidad, requisitos explícitos ni la verificación mínima.
- Revisar complejidad con `ponytail-review` antes del cierre de cambios relevantes.

## Memoria y cierre

- Obsidian es canónico. La sesión contiene solo reto, resultado, decisiones, validación
  y siguiente paso.
- Documentar una ADR solo para decisiones durables con alternativas o consecuencias.
- Ante una solicitud explícita de cierre, leer `docs/session-close.md`, mostrar el
  borrador y preguntar: “¿Confirmas que deseas cerrar y registrar esta sesión en
  Notion?”.
- En Notion, el resumen contiene solo trabajo y resultado. El resto usa propiedades
  estructuradas u Obsidian.
