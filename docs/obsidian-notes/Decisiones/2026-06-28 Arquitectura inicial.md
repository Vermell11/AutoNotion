# 2026-06-28 Arquitectura inicial

## Estado

Aceptada.

## Decisión

Separar las fuentes de verdad de [[Sistema de Trazabilidad]]:

- [[Notion]]: datos transaccionales y medición.
- [[Obsidian]]: conocimiento y decisiones humanas.
- [[Graphify]]: relaciones técnicas derivadas.

La primera fase usa Notion en modo lectura, mantiene Obsidian manualmente y no ejecuta
Graphify. Las automatizaciones futuras deberán ser confirmadas, idempotentes y
auditables.

## Consecuencias

Se reduce la duplicación, cada dato tiene un dueño y el conocimiento derivado puede
regenerarse sin perder el razonamiento humano.
