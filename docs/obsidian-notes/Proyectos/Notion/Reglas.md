# Reglas del proyecto Notion

Estas reglas especializan [[Reglas globales del Sistema de Trazabilidad]] para la
carpeta raíz `Notion`. No pueden contradecir las reglas globales.

## Reglas locales

- Tratar `public/apikey/key.txt` como secreto local transitorio: nunca mostrarlo,
  documentarlo ni versionarlo.
- Preferir `NOTION_API_KEY`; usar `key.txt` solo mediante el cargador autorizado.
- Ejecutar las pruebas con `PYTHONPATH=src python3 -m unittest discover -s tests -v`.
- Mantener alineadas las especificaciones de `docs/obsidian-notes/` con la bóveda
  canónica `Cerebro`; [[Obsidian]] prevalece para conocimiento humano.
- Consultar el grafo existente antes de reconstruirlo. Actualizar [[Graphify]] durante
  un cierre confirmado o cuando el usuario lo solicite explícitamente.
- Mantener `Sesiones/En curso.md` con [[Plantilla - Sesión de proyecto]] y convertirla
  en la nota fechada al cerrar; no conservar dos versiones divergentes.
- Usar siempre los `data_source_id` canónicos documentados; nunca seleccionar una
  fuente de [[Notion]] únicamente por nombre.
- Los proyectos externos usan el comando central `scripts/notion.py close-session`;
  nunca se copia el secreto ni se implementa un cliente alternativo.
- Para código Python, aplicar [[Ponytail]] después de consultar el grafo y rastrear
  los llamadores. Preferir stdlib y patrones existentes; no añadir dependencias.
- Antes del borrador de cierre, revisar el diff con `ponytail-review` y aplicar solo
  simplificaciones que conserven seguridad, errores, contratos y pruebas.

## Punteros

- [[Proyectos/Notion/Resumen]]
- [[Proyectos/Notion/Estado actual]]
- [[Proyectos/Notion/Arquitectura/Arquitectura del sistema]]
