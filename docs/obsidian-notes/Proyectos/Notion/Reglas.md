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

## Punteros

- [[Proyectos/Notion/Resumen]]
- [[Proyectos/Notion/Estado actual]]
- [[Proyectos/Notion/Arquitectura/Arquitectura del sistema]]
