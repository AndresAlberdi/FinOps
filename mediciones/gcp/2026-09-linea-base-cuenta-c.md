# Google Cloud — línea base de la cuenta de facturación C (terminada en 5DBD7A)

| Versión | Fecha | Fuente |
|---|---|---|
| 0.1 | 2026-10-01 | Exportación de facturación a BigQuery (costo de uso estándar), dataset `US` multirregional del proyecto dedicado `finops-ecosistema-c-4831`. Costo bruto en USD, sin impuestos. Datos crudos en `datos/gcp/` (no versionado) |

La cuenta C factura 3 proyectos: `novuchatdemo`, `gen-lang-client-0705436525` (autogenerado por la consola de Gemini) y `encuentramebo`.

## Costo por mes y servicio

| Mes | Proyecto | Servicio | Costo bruto (USD) | Créditos (USD) | Días con datos |
|---|---|---|---|---|---|
| 2026-08 | (nivel de factura) | Invoice | 0,0039 | 0,00 | 1 de agosto |
| 2026-09 | `novuchatdemo` | **Gemini API** | **0,5305** | 0,00 | 1 a 5 de septiembre |
| 2026-09 | `novuchatdemo`, `gen-lang-client-0705436525`, `encuentramebo` | Cloud Logging | 0,00 | 0,00 | 1 de septiembre |
| | | **Total septiembre** | **0,53** | **0,00** | |

## Qué dice y qué no

- **Es una cuenta casi sin gasto:** USD 0,53 en septiembre. No hay una palanca de ahorro de importancia aquí; el valor está en detectar saltos.
- **Todo el gasto fue Gemini en `novuchatdemo`, y se detuvo el 5 de septiembre.** No hay cargos posteriores. Es coherente con un uso de pruebas o demostración.
- **`gen-lang-client-0705436525` no tuvo costo.** Es el proyecto autogenerado con una clave de Gemini sin restringir que SeguridadGeneral marcó como riesgo; hoy no cuesta, pero una clave filtrada se puede usar sin límite: es un riesgo de seguridad, no de costo actual.
- **Retroactivo:** el dataset es multirregional, así que trae datos desde el 1 de septiembre (más una línea de agosto a nivel de factura, de monto despreciable; verificar su naturaleza). **No hay todavía un segundo ciclo completo:** septiembre es el primero. No se puede calcular una media de tres meses ni un umbral de anomalía del 20 %.
- **Sin cifras de octubre:** el export se activó el 1 de octubre; la exportación diaria las irá agregando.
- **No incluye** la cuenta de facturación principal (5 proyectos), cuyo export está conectado pero sin tabla todavía, ni AWS (`mediciones/aws/`).

## Costo de la recolección
2 consultas a BigQuery (una simulación y una real) sobre 1,5 KB de datos; BigQuery facturó el mínimo de 10 MiB, muy por debajo del primer TiB gratuito al mes (https://cloud.google.com/bigquery/pricing, vía catálogo de precios, consultado el 2026-09-30). **USD 0,00.**

## Siguiente paso
Esperar la tabla de la cuenta principal y, con las dos, consolidar Google en una sola línea base. Repetir la lectura el primer día hábil de cada mes (`docs/02` §4).
