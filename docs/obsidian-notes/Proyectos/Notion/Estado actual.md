# Estado actual de Notion

- Estado vivo: en curso.
- Reto activo: salidas Excel/PDF seguras, cierre externo autónomo y memoria
  operacional obligatoria en Obsidian.
- Último resultado: contrato base, prompts y plantillas actualizados para que guardar
  avance o cerrar exija memoria operacional antes de Notion.
- Validación actual: `68` pruebas pasan, incluidas XLSX/PDF y append incierto; la API
  real exportó `4` fuentes/`134` filas; `git diff --check` y `compileall` pasan.
- Siguiente paso: crear el commit final, ejecutar el preflight y presentar el borrador.
- Bloqueos: ninguno técnico.
- Cierre/publicación: pendiente; no registrar en Notion todavía.

## Qué hace actualmente

- Cliente Python seguro para la API `2026-03-11` de [[Notion]].
- Verificación, descubrimiento, paginación y consulta de esquemas.
- Creación y actualización de bases, páginas, contenido y propiedades.
- Protección frente a reintentos duplicados de operaciones de creación.
- Ledger de sesiones y relación con actividades.
- Cálculo de duración con timestamps y zona horaria.
- Documentación en [[Obsidian]], grafo [[Graphify]] y versionado Git.
- Reglas globales y locales separadas, con continuidad mediante una nota de sesión en
  curso y sesiones cerradas.
- Cierre humano asistido: la IA espera la orden del usuario, presenta el borrador y
  solicita confirmación antes de escribir en [[Notion]].
- Comando central `close-session` con preflight, SHA completo, identidad idempotente,
  creación de actividades relacionadas y reanudación de cierres parciales.
- Regla [[Ponytail]] documentada para reducir código y contexto innecesarios en Codex,
  Claude Code y los prompts estándar.
- Divulgación progresiva en V1.4 con presupuestos automáticos para arranque, cierre y
  prompts.
- Exportación Excel de fuentes visibles o bases descendientes de una página,
  implementada y pendiente de validación contra la API real.
- Informe semanal PDF de solo lectura desde `Base de datos de trabajo`, con
  indicadores, gráficos, avances y detalle de actividades.
- Coordinador `close-project prepare/finalize`: bloquea árboles sucios, SHA o tags
  inconsistentes y ramas divergentes; tras confirmación registra Notion y publica
  rama + tag de forma atómica, también en la primera publicación de un remoto vacío.
- Prompts separados para migración completa en Claude Code y continuidad sin cierre
  desde Claude App.
- Bootstrap global de Claude Code: carga automáticamente contrato, proyecto, Obsidian,
  Graphify y conector Notion; los cuatro prompts son disparadores breves.
- Contrato de Memoria Operacional: ninguna sesión se considera guardada o cerrada si
  antes no actualizó sesión, estado actual, backlog, roadmap si cambió, decisiones
  durables y cápsula estable cuando aplique.

## Qué todavía no hace

- No detecta cambios automáticamente.
- No pregunta ni registra actividades mediante un flujo dedicado.
- No genera dashboards, correos ni tareas programadas.
- El informe semanal existe, pero su ejecución todavía es manual.
- No sincroniza automáticamente Obsidian, Notion y código.
- El conector todavía depende de la ruta local canónica de este repositorio.
- La sincronización con ControlP depende de que cada agente mantenga la memoria
  operacional de Obsidian antes de guardar o cerrar.

## Avance al propósito final

La base, seguridad, memoria por proyecto y continuidad de IA están operativas. El
registro de actividades es parcial y la reportería está iniciada, aún sin automatizar.
V1.4 redujo el contexto obligatorio sin alterar el modelo de trazabilidad:
Graphify selecciona fuentes, Obsidian conserva detalle y Notion solo el resultado
ejecutivo. Después se retomarán la distribución del conector y los reportes.

## Referencias

- [[Proyectos/Notion/Resumen]]
- [[Proyectos/Notion/Reglas]]
- [[Proyectos/Notion/Backlog]]
- [[Proyectos/Notion/Roadmap]]
- [[Proyectos/Notion/Arquitectura/Arquitectura del sistema]]
- [[Proyectos/Notion/Sesiones/2026-06-29 - V1.3]]
- [[Proyectos/Notion/Sesiones/2026-06-29 - V1.4]]
