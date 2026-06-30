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

## Optimización de código y tokens

- En tareas de código se usa [[Ponytail]] después de comprender el flujo real.
- La escalera obligatoria es: no construir si no es necesario; reutilizar código
  existente; preferir biblioteca estándar; usar capacidades nativas; reutilizar una
  dependencia ya instalada; y solo entonces escribir el mínimo código que funciona.
- Antes de cerrar un cambio de código relevante se realiza una revisión Ponytail de
  complejidad. Si la skill no está disponible, la IA aplica manualmente el mismo
  criterio y lo declara.
- Nunca se añade una dependencia solo para reducir líneas.
- La simplificación no elimina seguridad, validación en límites de confianza, manejo
  de errores que evita pérdida de datos, accesibilidad, requisitos explícitos ni una
  verificación mínima ejecutable.
- Ponytail optimiza la implementación y el contexto producido; no reemplaza
  [[Obsidian]], [[Graphify]], las pruebas ni las decisiones humanas.

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

## Conector central de cierre

- Todo proyecto usa el comando canónico:
  `python3 "/Users/andresortegacorpus/Library/Mobile Documents/com~apple~CloudDocs/code/Notion/scripts/notion.py" close-session`.
- El payload JSON sigue
  `/Users/andresortegacorpus/Library/Mobile Documents/com~apple~CloudDocs/code/Notion/config/session-close.example.json`,
  se guarda fuera del repositorio consumidor y nunca contiene secretos.
- Después del commit final se usa su SHA completo y se ejecuta `--dry-run`.
- Si el preflight falla, la sesión permanece pendiente y no se crea ni publica el tag.
- Si pasa, se crea el tag local, se ejecuta el cierre sin `--dry-run` y se exige
  `status=completed`.
- Solo después se publican `main` y el tag. No se permiten commits posteriores al tag
  para agregar URL o metadata de cierre.
- Una segunda ejecución reconcilia la identidad `Nombre + Versión + Commit Git`,
  reutiliza filas existentes y completa actividades faltantes.
- El preflight valida opciones reales de select/status. Nunca se inventan categorías o
  estados; si el mapeo es ambiguo, se pide decisión humana.
- Nunca copiar `key.txt`, pasar tokens por argumentos ni crear clientes alternativos.

Relacionado con [[Obsidian]], [[Notion]], [[Graphify]] y [[Ponytail]].
