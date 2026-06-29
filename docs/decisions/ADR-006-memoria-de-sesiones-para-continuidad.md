# ADR-006: Memoria de sesiones para continuidad

- Fecha: 2026-06-28
- Estado: aceptada

## Contexto

Una nota que solo registra reto, tareas y resultado puede ser suficiente para auditoría,
pero no siempre permite que una IA reconstruya acuerdos, conexiones, estado y pendientes.
Además, si la conversación se interrumpe antes del cierre, la última sesión cerrada no
contiene el trabajo en curso.

## Decisión

- Cada proyecto mantiene `Sesiones/En curso.md` mientras exista trabajo activo.
- La nota se actualiza después de acuerdos o cambios relevantes, sin copiar la
  conversación completa.
- Al cerrar, se convierte en `Sesiones/<Fecha> - <Versión>.md`; no se mantienen dos
  copias divergentes.
- Una sesión cerrada incluye como mínimo: reto, resumen ejecutivo, tiempo, acuerdos,
  trabajo realizado, validaciones y evidencia, estado al cerrar, pendientes,
  continuidad y conexiones.
- `PROJECT_CONTEXT.md` apunta a la última sesión cerrada y a `En curso.md` cuando exista.
- Las sesiones históricas no se reescriben para simular conocimiento posterior; se
  admiten notas de actualización que enlacen decisiones que las superaron.

## Consecuencias

- Una IA puede retomar trabajo aun si la sesión anterior no alcanzó el cierre.
- Obsidian conserva suficiente contexto sin almacenar transcripciones completas.
- El cierre transforma una memoria provisional en evidencia estable.
- Los prompts y reglas deben mantener esta estructura en todos los proyectos.
