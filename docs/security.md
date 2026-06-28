# Seguridad

## Estado actual

`public/apikey/key.txt` es un mecanismo transitorio. Está cubierto por reglas redundantes
de `.gitignore` y debe tener permisos `600`. No debe copiarse a notas, logs, capturas,
issues, prompts ni argumentos de proceso.

Antes de inicializar o publicar Git:

```bash
git check-ignore -v public/apikey/key.txt
git status --ignored
```

Si el archivo alguna vez fue versionado, ignorarlo no elimina su historial: hay que
rotar el token de inmediato y limpiar el historial con un procedimiento acordado.

## Migración a entorno

1. Definir `NOTION_API_KEY` mediante llavero/gestor de secretos o entorno de ejecución.
2. Confirmar `python3 scripts/notion.py check`.
3. Mover `key.txt` fuera del repositorio y después eliminar el fallback en una ADR.
4. En CI, usar el almacén de secretos del proveedor, nunca variables escritas en YAML.

El entorno tiene precedencia sobre el archivo para permitir una migración sin corte.

## Controles recomendados

- Privilegios mínimos y conexión separada para automatización.
- Compartir solo las páginas o fuentes necesarias.
- Rotación ante sospecha de exposición.
- Revisión de dependencias y pinning antes de añadir paquetes externos.
- Escaneo de secretos en pre-commit y CI cuando exista repositorio remoto.
- Redacción de tokens en excepciones y prohibición de volcar requests completos.
