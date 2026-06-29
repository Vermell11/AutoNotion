# Reglas globales del Sistema de Trazabilidad

Estas reglas aplican a todos los proyectos conectados con [[Sistema de Trazabilidad]].
Son canónicas, obligatorias y no deben copiarse dentro de cada proyecto.

## Jerarquía

1. Seguridad y una instrucción explícita vigente del usuario.
2. Esta nota de reglas globales.
3. `Proyectos/<Proyecto>/Reglas.md`.
4. Convenciones técnicas inferidas del repositorio.

Una regla de proyecto puede especializar el trabajo local, pero no contradecir estas
reglas globales. Una excepción global requiere aprobación explícita del usuario y debe
documentarse como decisión.

## Flujo obligatorio de inicio

Toda IA, incluyendo Codex y Claude Code, debe:

1. Leer `AGENTS.md` o `CLAUDE.md`.
2. Consultar `PROJECT_CONTEXT.md`, que funciona únicamente como índice mínimo.
3. Seguir sus enlaces a esta nota, a `Proyectos/<Proyecto>/Reglas.md`, al resumen, a la
   última sesión cerrada y a `Sesiones/En curso.md` cuando exista en [[Obsidian]].
4. Consultar el grafo existente de [[Graphify]] antes de inspeccionar el código o
   proponer una extracción.

[[Notion]] no se consulta para reconstruir contexto rutinario.

## Memoria de sesiones

- Durante el trabajo activo se mantiene `Proyectos/<Proyecto>/Sesiones/En curso.md`.
- Se actualiza después de acuerdos o cambios relevantes, sin copiar la conversación.
- Incluye reto, resumen ejecutivo, acuerdos, trabajo, validaciones, estado, pendientes,
  continuidad y conexiones.
- Al cerrar, se convierte en `Sesiones/<Fecha> - <Versión>.md`; no quedan dos copias
  divergentes.
- Una nota histórica conserva su contexto original. Las decisiones posteriores se
  agregan como actualización enlazada, no como reescritura silenciosa.

## Versionamiento Git

- Cada sesión cerrada y confirmada debe tener un tag Git anotado e inmutable.
- El formato base es `V<mayor>.<menor>` y la primera versión es `V1.0`.
- La IA propone la siguiente versión y el usuario la confirma como parte del borrador
  de cierre.
- Nunca se mueve, reemplaza ni reutiliza un tag publicado.
- Crear o publicar el tag no autoriza por sí mismo el registro en [[Notion]].

## Autorización para registrar la sesión

- La IA no decide cuándo termina la sesión.
- Terminar una tarea, resolver el reto, pausar o recibir mensajes de continuidad no
  inicia el cierre.
- La IA espera a que el usuario diga explícitamente que desea cerrar o cargar en
  [[Notion]] lo realizado durante la sesión.
- Después muestra el borrador completo con reto, resultado, resumen, inicio, fin,
  duración, horas, versión, tag, commit y actividades relacionadas.
- `Duración minutos` y `Horas` representan trabajo activo. Si la sesión cruza una pausa
  prolongada, se documentan los intervalos y se excluye la pausa; no se registra todo
  el tiempo de pared como trabajo.
- Antes de escribir pregunta: “¿Confirmas que deseas cerrar y registrar esta sesión en
  Notion?”.
- Solo una respuesta afirmativa inequívoca autoriza una única fila de cierre.
- Sin esa confirmación, la sesión continúa abierta y no se crea, actualiza ni publica
  ninguna fila de sesión.

Relacionado con [[Obsidian]], [[Notion]] y [[Graphify]].
