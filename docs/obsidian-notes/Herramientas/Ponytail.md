# Ponytail

[[Ponytail]] es el criterio de implementación mínima del [[Sistema de Trazabilidad]].
Ayuda a reducir código, dependencias y contexto innecesario, pero no es una fuente de
verdad.

## Uso estándar

Después de leer las reglas, el contexto de [[Obsidian]] y el grafo de [[Graphify]], la
IA comprende el flujo real y aplica esta escalera:

1. Omitir lo que no necesita existir.
2. Reutilizar código y patrones del repositorio.
3. Preferir la biblioteca estándar.
4. Usar capacidades nativas de la plataforma.
5. Reutilizar dependencias ya instaladas.
6. Escribir solo entonces el mínimo código que funciona.

En Codex se usan `ponytail` y `ponytail-review` cuando están disponibles. En Claude
Code se usan sus equivalentes instalados; si no existen, se aplica manualmente esta
nota.

Ponytail se instala como capacidad global del agente y cada proyecto la activa desde
`AGENTS.md`. No se copia la skill dentro de repositorios: evitar duplicación y deriva
de versiones también es parte de la optimización.

## Límites

- No sustituye pruebas, documentación durable ni decisiones humanas.
- No elimina seguridad, validación en límites de confianza, prevención de pérdida de
  datos, accesibilidad ni requisitos explícitos.
- No justifica instalar una dependencia para ahorrar unas pocas líneas.
- Sus métricas publicadas son benchmarks del proyecto Ponytail, no ahorros medidos de
  este repositorio; no se inventan cifras locales de tokens o líneas.

## Instalación local

Las skills `ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt`,
`ponytail-gain` y `ponytail-help` se instalaron desde el repositorio oficial
`DietrichGebert/ponytail`. Codex debe reiniciarse para descubrirlas automáticamente.

Relacionado con [[Sistema de Trazabilidad]], [[Obsidian]] y [[Graphify]].
