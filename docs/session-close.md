# Cierre compartido de sesiones en Notion

El conector canónico vive en este repositorio y permite que cualquier proyecto del
ecosistema registre una sesión sin copiar la API Key:

```text
/Users/andresortegacorpus/Library/Mobile Documents/com~apple~CloudDocs/code/Notion/scripts/notion.py
```

## Contrato

El comando recibe un JSON basado en
[`config/session-close.example.json`](../config/session-close.example.json). El archivo:

- no contiene secretos;
- usa el nombre exacto de la carpeta raíz;
- incluye timestamps con zona horaria y trabajo activo;
- usa el SHA completo obtenido con `git rev-parse HEAD`;
- incluye la versión y el tag propuesto;
- puede incluir cero o más actividades;
- debe guardarse fuera del repositorio que se está cerrando para evitar un commit
  posterior al tag.

## Preflight sin escritura

Después de preparar el commit final, pero antes de crear o publicar el tag:

```bash
python3 "/Users/andresortegacorpus/Library/Mobile Documents/com~apple~CloudDocs/code/Notion/scripts/notion.py" \
  close-session --payload "/tmp/<Proyecto>-<Versión>-notion.json" --dry-run
```

El preflight valida credencial, esquemas, tipos, SHA completo e identidad
`Nombre + Versión + Commit Git`. También comprueba que `Estado`, `Ámbito`, `Category`
y `Status` existan realmente en los esquemas. No crea filas.

No inventar opciones de select/status. Si el preflight rechaza una categoría o estado,
usar la lista que entrega el error y pedir al usuario el mapeo cuando no sea inequívoco.

## Cierre

1. Configurar y verificar el remoto antes del commit final.
2. Completar Obsidian, `PROJECT_CONTEXT.md`, pruebas y Graphify.
3. Crear el commit final y obtener su SHA completo.
4. Construir el payload fuera del repositorio.
5. Ejecutar el preflight.
6. Crear localmente el tag anotado, sin publicarlo todavía.
7. Ejecutar el mismo comando sin `--dry-run`.
8. Verificar que devuelva `status=completed`.
9. Publicar `main` y el tag.

Si una respuesta de creación es incierta, se consulta Notion por la identidad estable
antes de reintentar. Una segunda ejecución reutiliza la sesión y actividades existentes
y completa únicamente lo pendiente.

## Condiciones de bloqueo

- Si el conector no existe o el preflight falla, no crear ni publicar el tag.
- Si una opción no existe y el mapeo es ambiguo, pedir decisión humana.
- No declarar la sesión cerrada en Notion.
- Mantener `Sesiones/En curso.md` y reportar el error concreto.
- Nunca copiar `key.txt`, pasar tokens por argumentos ni crear otro cliente dentro del
  proyecto consumidor.
