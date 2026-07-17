# Notion

## Resumen ejecutivo

Este proyecto es la base técnica de [[Sistema de Trazabilidad]]. Conecta de forma
segura con [[Notion]] para consultar y registrar sesiones, actividades, horas y
estados; centraliza en [[Obsidian]] la documentación y continuidad de cada proyecto; y
usa [[Graphify]] para comprender relaciones y arquitectura del código.

También permite que Codex y Claude Code retomen el trabajo desde la última sesión
documentada, calcula la duración de las sesiones y conserva evidencia mediante commits
y tags Git. El cierre y registro de sesiones todavía es asistido y requiere
confirmación humana. Ya genera un primer informe semanal PDF, pero aún no ofrece
dashboards, correos ni sincronizaciones automáticas.

El cierre externo usa dos fases coordinadas: conserva la confirmación humana y
automatiza las barreras Git, Notion y publicación para impedir tags sobre un commit
fallido.

## Propósito

Construir [[Sistema de Trazabilidad]] como ecosistema personal:

- [[Notion]] para sesiones, actividades, métricas y datos compartibles por API.
- [[Obsidian]] para conocimiento humano y continuidad por proyecto.
- [[Graphify]] para relaciones técnicas derivadas.
- [[Ponytail]] para reducir código, dependencias y contexto innecesario.
- Git para evidencia versionada e inmutable.

## Navegación

- [[Reglas globales del Sistema de Trazabilidad]]
- [[Proyectos/Notion/Reglas]]
- [[Proyectos/Notion/Estado actual]]
- [[Proyectos/Notion/Backlog]]
- [[Proyectos/Notion/Roadmap]]
- [[Proyectos/Notion/Arquitectura/Arquitectura del sistema]]
- Última sesión cerrada: [[Proyectos/Notion/Sesiones/2026-06-29 - V1.4]]
- Sesión en curso: [[Proyectos/Notion/Sesiones/En curso]] (`V1.5`).
- Decisiones: [[2026-06-28 Arquitectura inicial]] y
  [[2026-06-28 Trazabilidad por sesiones]], [[2026-06-28 Contexto de IA por proyecto]],
  [[2026-06-28 Confirmación explícita de cierre]] y
  [[2026-06-28 Reglas globales y por proyecto]],
  [[2026-06-28 Memoria de sesiones para continuidad]] y
  [[2026-06-29 Conector central de cierre en Notion]],
  [[2026-06-29 Adopción de Ponytail]] y
  [[2026-06-29 Contexto progresivo y presupuestos]]

## Estado

- Versión publicada: `V1.4`.
- Repositorio: https://github.com/Vermell11/AutoNotion
- V1.3 añade un conector central idempotente para que otros proyectos cierren
  en Notion sin copiar secretos e incorpora [[Ponytail]] como criterio portable.
- V1.4 redujo el arranque estimado de ~6300 a ≤1500 tokens y el cierre de ~2425 a
  ~738 con cápsula compacta, Graphify limitado y presupuestos automáticos.
- V1.5 implementa una exportación Excel de solo lectura con índice y una hoja por
  fuente de datos, un informe semanal PDF desde `Base de datos de trabajo` y el
  Contrato de Memoria Operacional para que Obsidian sea la continuidad completa.

## Continuidad para IA

La IA lee el contrato y la cápsula, la sesión abierta si existe y consulta Graphify con
presupuesto 600. Abre máximo tres fuentes; esta nota, las reglas y la historia se
cargan solo cuando aportan evidencia. No consulta Notion para contexto rutinario.

Una tarea terminada no cierra la sesión. La IA espera a que el usuario indique cuándo
desea cargarla; después muestra el borrador y solicita confirmación explícita para
cerrar y registrar en [[Notion]]. Sin ella, la sesión permanece abierta.

Antes de guardar avance o cerrar, la IA actualiza la memoria operacional de Obsidian:
sesión, estado actual, backlog, roadmap si cambió, decisiones durables y cápsula solo
si cambió contexto estable. ControlP lee esa continuidad, no el chat original.

Para tareas de código, después del contexto y el grafo se aplica [[Ponytail]] y se
revisa la complejidad del diff antes del cierre.
