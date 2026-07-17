# Contrato base - Sistema de Trazabilidad

Este contrato se aplica a proyectos nuevos y migrados. Las plantillas de entrada solo
definen el modo y el contexto variable.

## Bootstrap obligatorio

Ante cualquier solicitud de integrar, migrar, guardar avance, cerrar o registrar:

1. La carpeta actual es el proyecto y su nombre es el de la carpeta raíz.
2. Leer `AGENTS.md`, `PROJECT_CONTEXT.md` y la sesión abierta en
   `Proyectos/<Proyecto>/Sesiones/En curso.md` cuando exista.
3. Consultar Graphify con términos de la tarea y `--budget 600` antes del código;
   actualizarlo después de cambios relevantes.
4. Usar el conector central de este contrato para Notion. Este carga
   `NOTION_API_KEY` o `key.txt` mediante el cargador autorizado: nunca pedir al usuario
   que entregue, copie, conecte o mencione credenciales.
5. Antes de afirmar que Notion no está disponible, ejecutar `scripts/notion.py check`;
   si el sandbox bloquea red o carpetas, solicitar el permiso nativo y reintentar.
6. Ejecutar las operaciones directamente. No entregar comandos ni pedir al usuario
   pegar salidas.

Modos:

- Proyecto nuevo: inspeccionar seguridad/Git; crear contrato, cápsula y Obsidian;
  crear Graphify si falta; validar; mantener sesión abierta.
- Migración: inspeccionar sin reconstruir historia; conservar trabajo y convenciones;
  crear contrato, cápsula y Obsidian; actualizar Graphify; validar seguridad/pruebas;
  crear el commit final y preparar V1.0.
- Guardar avance: actualizar reto, resultado, decisiones, validación y siguiente paso
  mediante el Contrato de Memoria Operacional; cambiar cápsula solo si varió contexto
  estable; sin Notion, tag ni push.
- Cerrar: memoria Obsidian → Graphify vigente → pruebas y `quality` separada → commit
  → `close-project prepare` → confirmación → `close-project finalize` → Notion/push →
  reconciliar anti-obsoletos y `activity_pages` (título, ID, URL).

## Constantes

- Bóveda:
  `/Users/andresortegacorpus/Library/Mobile Documents/com~apple~CloudDocs/code/Brain/Cerebro`
- Sesiones en Notion: `c36049cf-9d28-4999-8f0a-f0e15deaa8b4`
- Actividades en Notion: `033bc5d6-9357-83c6-b71e-07d61caa648f`
- Conector:
  `/Users/andresortegacorpus/Library/Mobile Documents/com~apple~CloudDocs/code/Notion/scripts/notion.py`

## Fuentes

- Notion: sesiones, actividades y métricas.
- Obsidian: memoria operacional, contexto humano, decisiones y continuidad.
- Graphify: índice técnico derivado.
- Git: implementación y evidencia versionada.

## Contrato de Memoria Operacional

Ninguna sesión de Codex, Claude Desktop o Claude Code se considera guardada o cerrada
si antes no actualizó Obsidian. Notion conserva el ledger; Obsidian, la continuidad
que lectores como ControlP consumen sin reconstruir el chat.

Antes de guardar avance, cambiar de herramienta o cerrar, la IA debe actualizar el
paquete operacional mínimo:

- Sesión: objetivo, reto activo, resultado, decisiones, validación, continuidad,
  backlog, bloqueos, fuentes y estado real.
- `Estado actual.md`: estado vivo, reto activo, último resultado, validación,
  siguiente paso, bloqueos y cierre/publicación si aplica.
- `Backlog.md`: tareas accionables, prioridad, origen y estado.
- `Roadmap.md`: hitos, sprints o features cuando cambie alcance o cronograma.
- `Decisiones/`: solo decisiones durables con alternativas, motivo e impacto.
- `PROJECT_CONTEXT.md`: solo si cambió contexto estable.

Verificación mínima: reto activo, siguiente paso, pendientes accionables y estado real
sincronizado. Si una fuente no aplica, escribir `No aplica` y por qué.

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
   `Backlog.md`, `Roadmap.md`, `Reglas.md`, `Sesiones/`, `Decisiones/` y
   `Arquitectura/`.
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
12. En el cierre, la IA ejecuta las operaciones disponibles y solicita permisos con el
    mecanismo nativo. No delega comandos ni pide al usuario copiar salidas de terminal.
13. La migración completa se ejecuta en Claude Code local. Claude App puede guardar
    continuidad y commits locales cuando `.git` sea escribible, pero no se presume que
    tenga Graphify, autenticación GitHub ni red hacia Notion.
14. `PROJECT_CONTEXT.md` no contiene el SHA actual, URLs de cierre, estado de push ni
    métricas transitorias. Git conserva evidencia; Obsidian y Notion conservan el
    estado dinámico.

## Presupuesto

El arranque predeterminado debe permanecer en ≤1500 tokens estimados, incluida la
consulta inicial del grafo. Si requiere más contexto, la IA explica qué evidencia falta
y carga solo la fuente necesaria.

Relacionado con [[Sistema de Trazabilidad]], [[Ponytail]], [[Graphify]], [[Obsidian]] y
[[Notion]].
