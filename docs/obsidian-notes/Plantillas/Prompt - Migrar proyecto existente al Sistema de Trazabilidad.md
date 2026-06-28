# Prompt - Migrar proyecto existente al Sistema de Trazabilidad

Relacionado con [[Sistema de Trazabilidad]], [[Notion]], [[Obsidian]] y [[Graphify]].

## Cómo usarlo

Reemplaza los campos entre corchetes. Esta plantilla migra únicamente contexto vigente
y documentación; no reconstruye actividades ni horas históricas.

## Prompt

```text
Actúa como responsable de migrar este proyecto existente a mi Sistema de Trazabilidad.
La migración debe preservar la implementación y consolidar únicamente el contexto
vigente y la documentación útil. No reconstruyas actividades ni horas históricas.

CONTEXTO DEL PROYECTO
- Nombre: [NOMBRE_DEL_PROYECTO]
- Ruta o repositorio: [RUTA_O_URL]
- Tipo: [PERSONAL / LABORAL / OTRO]
- Objetivo vigente: [OBJETIVO_ACTUAL]
- Estado actual conocido: [ESTADO]
- Responsable: [RESPONSABLE]
- Bóveda Obsidian:
  `/Users/andresortegacorpus/Library/Mobile Documents/com~apple~CloudDocs/code/Brain/Cerebro`
- Fuente canónica de proyectos en Notion:
  `c36049cf-9d28-4999-8f0a-f0e15deaa8b4` (Proyectos)
- Fuente canónica de actividades en Notion:
  `033bc5d6-9357-83c6-b71e-07d61caa648f` (Reporte de Tickets, bajo el encabezado
  Base de datos de trabajo)
- Documentación que considero importante: [RUTAS_O_REFERENCIAS]
- Restricciones adicionales: [RESTRICCIONES]

FUENTES DE VERDAD
- Notion: datos operativos y medibles desde la adopción del sistema en adelante.
- Obsidian: contexto vigente, decisiones, arquitectura, reuniones y aprendizajes.
- Graphify: relaciones técnicas derivadas del código actual.
- El repositorio: implementación y documentación operativa cercana al código.

FASE 1 — INVENTARIO SIN MODIFICACIONES
0. Toma el nombre del proyecto exclusivamente del nombre de la carpeta raíz. Consulta
   la última sesión en Notion, propón un reto o compromiso verificable para esta sesión
   y pide confirmación antes de continuar.
1. Inspecciona estructura, README, documentación, configuración, pruebas, estado Git,
   reglas de agentes, archivos sensibles y graphify-out si existe.
2. Identifica arquitectura actual, módulos, integraciones, responsables, decisiones
   implícitas, riesgos, deuda documental y fuentes contradictorias.
3. Clasifica la información:
   - vigente y debe migrarse;
   - histórica pero necesaria para entender decisiones;
   - obsoleta o duplicada;
   - incierta y requiere confirmación.
4. No ejecutes Graphify ni cambies archivos durante el inventario.

FASE 2 — PROPUESTA Y CONFIRMACIÓN
5. Presenta un resumen del estado real y un plan de migración proporcional.
6. Formula juntas las preguntas necesarias para resolver contradicciones o decisiones
   materiales. No adivines responsables, estados, IDs de Notion ni arquitectura.
7. Muestra qué contenido crearás, consolidarás, enlazarás o marcarás como obsoleto.
   No borres documentación existente sin autorización.

FASE 3 — MIGRACIÓN APROBADA
8. Crea o actualiza AGENTS.md para exigir documentación de decisiones, actualización
   de Obsidian, protección de secretos y confirmación antes de registrar actividades.
9. Consolida en Obsidian una nota de proyecto con propósito vigente, alcance, estado,
   arquitectura, decisiones, riesgos, repositorios y próximos pasos. Enlázala con
   [[Sistema de Trazabilidad]], [[Notion]], [[Obsidian]] y [[Graphify]].
10. Crea notas de decisión solo para decisiones todavía relevantes. Conserva contexto
    histórico mínimo cuando explique el estado actual; no migres ruido ni bitácoras
    obsoletas.
11. En Notion, verifica destinos por data_source_id. Para el cierre crea una fila nueva
    en `Proyectos` con Nombre=carpeta raíz, Fecha sesión, Reto o compromiso, Resuelto,
    Resumen, Versión, Tag Git y Commit Git. Nunca actualices una fila global ni
    dedupliques por nombre. Para actividades usa: Titulo=actividad, Category=categoría,
    Date Reported=fecha/hora, Horas=horas invertidas, Descripcion=detalle y
    Status=estado, relacionando `Proyecto` con la fila de sesión aplicable. No importes
    actividades ni horas anteriores.
12. Para Graphify, define raíz, exclusiones y política de actualización. Si ya existe
    un grafo, consúltalo antes de proponer una reconstrucción. No ejecutes extract,
    update, watch ni instales hooks sin autorización.
13. Preserva cambios locales y convenciones válidas. Añade verificaciones proporcionales
    y evita reescrituras masivas no justificadas.
14. Al cerrar, actualiza Obsidian y Graphify si corresponde, crea un tag Git anotado e
    inmutable y carga automáticamente una fila nueva de sesión en Notion. La primera
    versión es `V1.0`; en sesiones posteriores propone el siguiente número.

SEGURIDAD
- Nunca muestres, documentes, copies ni versiones secretos.
- No pases tokens por argumentos ni vuelques requests o variables completas.
- Propón variables de entorno o gestor de secretos para credenciales existentes.
- Señala secretos posiblemente versionados sin revelar su contenido y recomienda
  rotación cuando corresponda.

ENTREGA
- Inventario y decisiones de migración.
- Archivos creados, modificados, consolidados o declarados obsoletos.
- Contexto vigente incorporado a Obsidian.
- Registros propuestos y, solo si se confirmaron, creados en Notion.
- Reto acordado, resultado, nueva fila de sesión y tag Git de la versión.
- Estrategia de Graphify sin ejecución.
- Riesgos detectados, verificaciones y deuda pendiente.
- Próximos pasos sin reconstrucción histórica.
```
