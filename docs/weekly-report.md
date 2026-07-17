# Informe semanal PDF

`scripts/reporteSemanal.py` consulta de solo lectura la fuente configurada como
`Base de datos de trabajo` y crea:

```text
public/output/reporte-semanal-AAAA-MM-DD-al-AAAA-MM-DD.pdf
```

## Ejecución

```bash
python3 -m pip install -e .
python3 scripts/reporteSemanal.py
```

La semana se calcula de lunes a domingo usando la fecha local de ejecución. El PDF
incluye portada con indicadores y comparación contra el periodo previo, distribución
por tipo de trabajo (Reuniones/Desarrollo/Gestión), horas por módulo y por día,
avances ordenados por horas, asuntos abiertos (incluidos los de hasta 90 días atrás)
y detalle completo de actividades. El ámbito `trabajo` excluye actividades con
`Category` o `Modulo` igual a `Personal`.

## Propiedades

Los nombres se leen de `[activities]` en `config/notion.toml`. Son obligatorias
`Titulo` y `Date Reported`; las demás propiedades pueden estar vacías.

El reporte no escribe en Notion ni utiliza IA para inventar conclusiones. Las
relaciones de proyecto no se resuelven todavía: `Modulo` y `Category` representan los
frentes visibles. Las actividades sin horas se contabilizan con `0`.

## Diseño

El formato es 16:9 con tema claro ejecutivo: fondo blanco, texto tinta, franja
superior azul/cian, tarjetas con borde sutil, gráficas sobre pistas grises y pills
de color por estado en la tabla. No usa fotografías ni fuentes externas para
mantener el generador pequeño y portable.
