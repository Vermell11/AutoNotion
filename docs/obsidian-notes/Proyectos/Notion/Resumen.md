# Notion

## Resumen ejecutivo

Este proyecto es la base técnica de [[Sistema de Trazabilidad]]. Conecta de forma
segura con [[Notion]] para consultar y registrar sesiones, actividades, horas y
estados; centraliza en [[Obsidian]] la documentación y continuidad de cada proyecto; y
usa [[Graphify]] para comprender relaciones y arquitectura del código.

También permite que Codex y Claude Code retomen el trabajo desde la última sesión
documentada, calcula la duración de las sesiones y conserva evidencia mediante commits
y tags Git. El cierre y registro de sesiones todavía es asistido y requiere
confirmación humana. Aún no genera reportes, dashboards, correos ni sincronizaciones
automáticas.

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
- [[Proyectos/Notion/Arquitectura/Arquitectura del sistema]]
- Última sesión cerrada: [[Proyectos/Notion/Sesiones/2026-06-29 - V1.3]]
- Sesión en curso: ninguna.
- Decisiones: [[2026-06-28 Arquitectura inicial]] y
  [[2026-06-28 Trazabilidad por sesiones]], [[2026-06-28 Contexto de IA por proyecto]],
  [[2026-06-28 Confirmación explícita de cierre]] y
  [[2026-06-28 Reglas globales y por proyecto]],
  [[2026-06-28 Memoria de sesiones para continuidad]] y
  [[2026-06-29 Conector central de cierre en Notion]],
  [[2026-06-29 Adopción de Ponytail]]

## Estado

- Versión publicada: `V1.3`.
- Repositorio: https://github.com/Vermell11/AutoNotion
- V1.3 añade un conector central idempotente para que otros proyectos cierren
  en Notion sin copiar secretos e incorpora [[Ponytail]] como criterio portable.
- El siguiente objetivo es medir y reducir los tokens consumidos al iniciar, mantener
  y cerrar sesiones sin perder continuidad.

## Continuidad para IA

La IA lee `AGENTS.md` o `CLAUDE.md`, consulta `PROJECT_CONTEXT.md` como índice, lee las
reglas globales y del proyecto, esta nota, la última sesión cerrada y `En curso.md` si
existe; después consulta el grafo y solo entonces inspecciona el código. No consulta
Notion para contexto rutinario.

Una tarea terminada no cierra la sesión. La IA espera a que el usuario indique cuándo
desea cargarla; después muestra el borrador y solicita confirmación explícita para
cerrar y registrar en [[Notion]]. Sin ella, la sesión permanece abierta.

Para tareas de código, después del contexto y el grafo se aplica [[Ponytail]] y se
revisa la complejidad del diff antes del cierre.
