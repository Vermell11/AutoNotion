# Cierre de sesión

Se ejecuta solo después de que el usuario pida cerrar y confirme el borrador.

## Resumen para Notion

Debe indicar únicamente qué se hizo y el resultado, en máximo 120 palabras. No incluir
horas, fechas, versión, commit, tag, archivos, pruebas, métricas de Graphify ni contexto
ya conservado en Obsidian. Las descripciones de actividades admiten máximo 80 palabras.

Actividades: `title` sin prefijo (el conector añade proyecto/versión),
`reported_at` ascendente y `Backend` por `Date Reported ASC`; lo nuevo queda al
final.

## Secuencia autónoma

1. Finalizar la memoria operacional de Obsidian: sesión, `Estado actual.md`,
   `Backlog.md`, `Roadmap.md` si cambió, decisiones durables y `PROJECT_CONTEXT.md`
   solo si cambió contexto estable.
   REGLA DE REDACCIÓN de `PROJECT_CONTEXT.md`: se escribe ANTES del commit final
   como si la versión ya estuviera entregada — describe el estado logrado y el
   reto SIGUIENTE. Nunca contiene "registrar/cerrar la versión X", SHA, tag,
   URLs de cierre ni estado de push (regla 14 del contrato): ese estado
   transitorio vive en Obsidian, no en la cápsula. Así el finalize no deja la
   cápsula obsoleta.
2. Crear el commit final y obtener el SHA completo.
   ANTES de `git add`: revisar `git status` y EXCLUIR todo archivo untracked
   ajeno al alcance de la sesión (artefactos personales, salidas de otras
   herramientas, carpetas output/tmp). Nunca `git add -A` a ciegas: un archivo
   personal publicado en un tag obligó a purgar historia (V1.4, 2026-07-13).
3. Construir fuera del repositorio un JSON basado en
   [`config/session-close.example.json`](../config/session-close.example.json).
   `quality` separa auditoría offline, alertas conocidas y validación online; cero
   offline no elimina alertas.
4. Ejecutar el preflight coordinado:

```bash
python3 scripts/notion.py close-project prepare \
  --project /ruta/al/proyecto \
  --payload /tmp/cierre.json
```

5. Mostrar el borrador completo y solicitar la confirmación explícita.
6. Solo después de confirmarla, ejecutar:

```bash
python3 scripts/notion.py close-project finalize \
  --project /ruta/al/proyecto \
  --payload /tmp/cierre.json
```

`finalize` revalida Git y Notion, crea el tag anotado, exige `status=completed` y
publica `main` y el tag mediante un único push atómico. Una reejecución acepta
únicamente el mismo tag anotado apuntando al mismo commit. En una primera versión, el
remoto puede estar vacío: el mismo push crea `main` y el tag.

Con Graphify, `built_at_commit` identifica el corpus; después sólo puede cambiar
`graphify-out/` y el reporte debe coincidir. Otro cambio bloquea el preflight.

El payload no contiene secretos. Usa el nombre de la carpeta raíz, timestamps con zona,
tiempo activo, versión y tag iguales, SHA de 40 caracteres y opciones reales de Notion.
Una segunda ejecución reconcilia la sesión y actividades sin duplicarlas.

7. Reconciliación post-finalize (OBLIGATORIA, sin nueva confirmación): agregar el
   bloque "Cierre ejecutado" (commit/tag final, IDs de Notion, métricas de
   Graphify) a `Estado actual.md` y a la nota de sesión en Obsidian, y verificar
   anti-obsoletos: `PROJECT_CONTEXT.md` y `Estado actual.md` no pueden seguir
   pidiendo registrar/cerrar la versión recién publicada, ni citar
   `SCHEMA_VERSION`, formaciones u otros hechos del código que el cierre haya
   cambiado. Un cierre sin este paso NO está completo.
   COHERENCIA DE NUMERACIÓN: el "siguiente paso" en `PROJECT_CONTEXT.md`,
   `Estado actual.md` y `Roadmap.md` no puede llevar un número de versión
   menor o igual al recién publicado. Las historias planificadas NO llevan
   número fijo: se nombran por su título ("Agenda operativa") y reciben
   versión al entrar en construcción. Si una reprioritización deja un número
   invertido (origen: "V1.4.1" quedó detrás de V1.4.2, 2026-07-13), se
   retira el rótulo en los tres documentos como parte de este paso.
   Si el proyecto tiene `CONTEXT_MAP.md`, verificar que siga fiel a la
   estructura (módulos, archivos, puntos de extensión) y actualizarlo si la
   sesión la cambió.
   Copiar `activity_pages`: título+ID+URL; conteo insuficiente.

Si el preflight falla, no crear ni publicar el tag. Mantener la sesión abierta y pedir
al usuario únicamente cualquier dato o mapeo realmente ambiguo. El agente ejecuta las
operaciones; no delega comandos ni solicita copiar salidas de terminal.
