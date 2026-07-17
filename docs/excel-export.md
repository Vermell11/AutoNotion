# Exportación de Notion a Excel

El comando es de solo lectura:

```bash
python3 scripts/notion.py export-excel
python3 scripts/notion.py export-excel --page-id <PAGE_ID>
python3 scripts/notion.py export-excel --page-id <PAGE_ID> --include-content
python3 scripts/exportExcel.py
```

Sin `--page-id` exporta todas las fuentes visibles para la conexión. Con página,
recorre sus bloques descendientes, identifica cada `child_database`, obtiene sus data
sources y pagina todas las filas.

El libro se crea en `public/output/`, que está excluido de Git. Incluye:

- `Índice`: fuente, hoja, filas, columnas e identificadores;
- una hoja por data source, con nombres únicos;
- metadatos de página y todas las propiedades del esquema;
- tipos legibles para texto, números, fechas, estados, personas, fórmulas, rollups y
  relaciones;
- opcionalmente `_Contenido`, con el texto del cuerpo de cada página.

Las relaciones se conservan como IDs. Resolver títulos implicaría una solicitud por
página relacionada y se añadirá solo si una necesidad real justifica ese costo.

`scripts/exportExcel.py` es el acceso directo sin argumentos: usa la página principal
`388bc5d6-9357-8046-bc4f-d8f1e6405c0b`, incluye contenido y escribe en
`public/output/`.

Notion limita una consulta de data source a 10 000 resultados. El cliente recorre la
paginación disponible, pero una fuente mayor requiere partición por filtros.
