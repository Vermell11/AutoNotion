# Cierre de sesión

Se ejecuta solo después de que el usuario pida cerrar y confirme el borrador.

## Resumen para Notion

Debe indicar únicamente qué se hizo y el resultado, en máximo 120 palabras. No incluir
horas, fechas, versión, commit, tag, archivos, pruebas, métricas de Graphify ni contexto
ya conservado en Obsidian. Las descripciones de actividades admiten máximo 80 palabras.

## Secuencia

1. Finalizar Obsidian, `PROJECT_CONTEXT.md`, Graphify y pruebas.
2. Crear el commit final y obtener el SHA completo.
3. Construir fuera del repositorio un JSON basado en
   [`config/session-close.example.json`](../config/session-close.example.json).
4. Ejecutar:

```bash
python3 scripts/notion.py close-session --payload /tmp/cierre.json --dry-run
```

5. Si pasa, crear el tag anotado y ejecutar el mismo comando sin `--dry-run`.
6. Exigir `status=completed`; solo entonces publicar `main` y el tag.

El payload no contiene secretos. Usa el nombre de la carpeta raíz, timestamps con zona,
tiempo activo, versión y tag iguales, SHA de 40 caracteres y opciones reales de Notion.
Una segunda ejecución reconcilia la sesión y actividades sin duplicarlas.

Si el preflight falla, no crear ni publicar el tag. Mantener la sesión abierta y pedir
al usuario cualquier mapeo ambiguo.
