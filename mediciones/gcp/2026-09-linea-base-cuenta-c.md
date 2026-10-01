# Google Cloud — línea base de la cuenta de facturación C (terminada en 5DBD7A)

| Versión | Fecha | Estado |
|---|---|---|
| 0.2 | 2026-10-01 | **PROVISIONAL: los datos del export están incompletos** (el llenado inicial sigue en curso). Corrige la v0.1 |

Fuente: exportación de facturación a BigQuery (costo de uso estándar), dataset `US` multirregional del proyecto dedicado `finops-ecosistema-c-4831`. Costo bruto en USD. Datos crudos en `datos/gcp/` (no versionado). La cuenta factura 3 proyectos: `novuchatdemo`, `gen-lang-client-0705436525` (autogenerado por la consola de Gemini) y `encuentramebo`.

## Corrección de la v0.1 (error mío)

La v0.1 decía que «el gasto de Gemini se detuvo el 5 de septiembre». **Era falso.** La tabla llegaba hasta el 5/09 solo porque el llenado inicial del export no había terminado: Google avisa que la carga retroactiva puede tardar **hasta cinco días**. Una hora después la misma consulta llegaba al 10/09 y ya mostraba el doble de gasto. Una tabla incompleta no permite concluir que un gasto paró. La conclusión se retira.

## Lo que se sabe al 2026-10-01 (parcial)

| Mes | Proyecto | Servicio | Costo bruto (USD) | Datos hasta |
|---|---|---|---|---|
| 2026-09 | `novuchatdemo` | **Gemini API** | **1,1582** | 10 de septiembre |
| 2026-09 | tres proyectos | Cloud Logging | 0,00 | 1 de septiembre |
| 2026-08 | (nivel de factura) | Invoice | 0,0039 | 1 de agosto |

- **El total de septiembre es un piso, no una cifra:** faltan los días 11 a 30, que incluyen la semana del 29/09 en que NovuChat informó que se agotó el crédito prepago de Gemini (error 402).
- **Aún no se puede hablar de un hueco del consumo prepago.** Primero hay que dejar terminar el llenado. Esa hipótesis (NovuChat y la sesión de Gemini) se retoma después, comparando con el saldo y el uso de Google AI Studio.
- **No hay segundo ciclo ni media de tres meses**: sin base para el umbral de anomalía del 20 %.
- **Octubre** aparecerá cuando termine la carga diaria.

## Siguiente paso
Volver a leer la tabla **a partir del 2026-10-06** (cinco días después de activar el export), confirmar que `MAX(usage_start_time)` llegue a septiembre completo y recién entonces fijar la línea base. Comprobación barata: `SELECT MAX(DATE(usage_start_time)), MAX(export_time)`.

## Costo de la recolección
Consultas de 1,5 a 160 KB, facturadas al mínimo de 10 MiB cada una: dentro del primer TiB gratuito al mes (https://cloud.google.com/bigquery/pricing, vía catálogo de precios, 2026-09-30). **USD 0,00.**
