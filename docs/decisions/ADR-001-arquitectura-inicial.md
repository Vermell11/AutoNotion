# ADR-001: Separación de fuentes de verdad

- Fecha: 2026-06-28
- Estado: aceptada

## Contexto

El sistema debe medir trabajo, conservar conocimiento humano y ofrecer contexto técnico
sin duplicar responsabilidades ni crear sincronización prematura.

## Decisión

Notion será autoridad transaccional; Obsidian, autoridad documental; Graphify, índice
técnico derivado. Este repositorio contendrá adaptadores y contratos. La Fase 1 tendrá
solo lectura de Notion y alineación manual con Obsidian.

## Consecuencias

- Cada dato tiene un propietario claro.
- Graphify puede regenerarse sin pérdida de decisiones.
- La duplicación se reemplaza por enlaces e identificadores.
- La automatización futura requiere idempotencia, confirmación humana y trazabilidad.
- Durante esta fase hay mantenimiento documental manual deliberado.
