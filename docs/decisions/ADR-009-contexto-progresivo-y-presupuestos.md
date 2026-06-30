# ADR-009: Contexto progresivo y presupuestos

## Estado

Aceptada el 2026-06-29.

## Contexto

El arranque obligatorio requería aproximadamente 6300 tokens documentales y el cierre
2425. Se leían reglas, resumen, estado y sesión histórica aunque la tarea no los
necesitara; los prompts repetían cerca del 69 % de su contenido.

## Decisión

Adoptar divulgación progresiva:

- contrato y cápsula compactos;
- sesión abierta solo cuando exista;
- Graphify con presupuesto inicial 600 y máximo tres fuentes;
- contexto adicional bajo demanda;
- Ponytail global activado por proyecto, sin copiar la skill;
- sesiones de hasta 500 tokens estimados;
- resumen de Notion de hasta 120 palabras con solo trabajo y resultado;
- pruebas automáticas para presupuestos de arranque, cierre y prompts.

Los documentos extensos siguen siendo canónicos, pero pasan a contexto frío.

## Consecuencias

El objetivo de arranque es ≤1500 tokens estimados y el cierre 800–1100. No se crea un
nuevo servicio ni se modifica el modelo de datos de Notion. La estimación usa
caracteres/4 para evitar una dependencia de tokenización y se trata como límite
conservador, no como conteo exacto de un modelo.
