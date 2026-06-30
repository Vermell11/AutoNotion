# Estrategia de Graphify

Graphify es un índice técnico derivado y regenerable. La primera extracción del
repositorio `Notion` se completó el 2026-06-28.

## Estado del grafo

- El tamaño y las comunidades cambian con cada actualización; consultar
  `GRAPH_REPORT.md` para las métricas vigentes.
- Salidas locales: `graphify-out/graph.json`, `graph.html` y `GRAPH_REPORT.md`.
- Costo semántico externo: 0 tokens; la documentación se extrajo localmente.

La extracción inicial mostró aristas externas no materializadas y relaciones paralelas.
Tras incorporar los cambios finales mediante actualización incremental, el diagnóstico
reportó cero extremos faltantes, aristas colgantes, bucles o colapsos.

## Dónde ejecutarlo

Ejecutar por raíz de repositorio con identidad propia, no sobre toda la bóveda ni sobre
un directorio padre que mezcle proyectos. Este repositorio será candidato cuando tenga
una implementación suficiente; repositorios de producto existentes son candidatos
inmediatos. Excluir secretos, binarios, dependencias vendorizadas y artefactos.

## Cuándo

1. La primera extracción manual ya fue completada en este repositorio.
2. Actualización incremental después de cambios arquitectónicos, no por cada edición.
3. Consulta del grafo existente antes de reconstruirlo.
4. Automatización futura mediante hook posterior al commit o CI solo tras medir costo,
   duración, ruido y comportamiento en ramas.

No se instalarán hooks ni `watch` hasta medir el comportamiento de actualizaciones
incrementales en varios cambios reales.

## Integraciones

- **Obsidian:** una nota índice por repositorio enlaza `GRAPH_REPORT.md`, fecha de última
  extracción y decisiones humanas relacionadas. No importar una nota por nodo por
  defecto: produce ruido y mezcla conocimiento derivado con curado.
- **Codex:** `AGENTS.md` ordena consultar `graphify-out/graph.json` cuando exista para
  preguntas de arquitectura; reconstruir solo por solicitud o política explícita.
- **Claude Code:** `CLAUDE.md` apunta a `AGENTS.md` y `PROJECT_CONTEXT.md`, y exige
  consultar el grafo existente antes de reconstruirlo.

## Recuperación con presupuesto

- Orientación: consulta específica con `--budget 600`.
- La salida selecciona fuentes; no sustituye leer el fragmento relevante.
- Abrir como máximo tres fuentes por defecto.
- Ampliar a `--budget 1200` solo cuando falten relaciones o evidencia.
- Guardar resultados en memoria de Graphify únicamente para hallazgos no obvios que
  evitarán repetir una investigación; no guardar cada consulta.
- Las sesiones históricas y toda la bóveda no se cargan de forma preventiva.

## Política de actualización propuesta

- Full extract: alta inicial, cambio mayor de estructura o reparación.
- Incremental update: después de commits que alteren dependencias, módulos o flujos.
- Cluster-only: cuando cambie el análisis comunitario sin cambiar el corpus.
- Watch mode: no recomendado al inicio; genera actividad y artefactos continuos.
- Salidas `graphify-out/`: locales y excluidas de Git por defecto. Publicar solo un
  reporte aprobado si existe una necesidad concreta.

Antes de adoptar comandos se debe registrar versión instalada, verificar la sintaxis
real y decidir exclusiones. La skill disponible documenta `--update`, consulta, hooks y
exportación Obsidian; el comando exacto debe verificarse porque la solicitud menciona
`graphify extract .` y la interfaz instalada puede diferir.
