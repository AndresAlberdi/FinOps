# Google Cloud — línea base de la cuenta de facturación principal (terminada en 603EC8)

| Versión | Fecha | Estado |
|---|---|---|
| 1.0 | 2026-10-04 | **Septiembre completo** (export con datos hasta el 2026-10-03). Sustituye a la v0.1 provisional |

Fuente: exportación de facturación a BigQuery (costo de uso estándar), dataset `billing_export` en `US` del proyecto `novuchatstaging` (el tope de 5 proyectos por cuenta de facturación impidió uno dedicado). La cuenta factura 5 proyectos: `novuchat-demo`, `novuchat-site`, `novuchatstaging`, `puntosnb` y `whatsappmodular`; el export registra además `aab1-landing` y `encuentramebo-1`. Costo bruto en USD; datos crudos en `datos/gcp/` (no versionado).

## Septiembre 2026

| Mes | Costo bruto (USD) | Créditos (USD) | Neto (USD) |
|---|---|---|---|
| 2026-09 | **10,40** | **−10,40** | **0,00** |

**Los créditos cubren el 100 % del gasto bruto.** Mientras duren, esta cuenta no paga nada.

### Por proyecto

| Proyecto | Negocio (`docs/06`) | Bruto | Servicios principales |
|---|---|---|---|
| `novuchat-demo` | NovuChat | 8,65 | Cloud Run Functions 7,72; Secret Manager 0,94 |
| `novuchat-site` | NovuChat | 1,12 | Vertex AI 0,96 (hasta el 23/09); Secret Manager 0,15; Cloud Run Functions 0,02 |
| `novuchatstaging` | NovuChat | 0,41 | Secret Manager 0,27; Cloud Run Functions 0,14 |
| `whatsappmodular` | AAB1 / WhatsApp-Modular | 0,14 | Secret Manager |
| `puntosnb` | Hipatia | 0,04 | Cloud Run Functions |
| `aab1-landing` | AAB1 / WhatsApp-Modular | 0,03 | Secret Manager |
| `encuentramebo-1` | Encuéntrame.BO | 0,00 | Cloud Run Functions (3 al 7/09) |
| (cargo de factura) | Comunes | 0,00 | «Invoice» |

### El costo fijo: una instancia mínima

El gasto más grande es el SKU «Cloud Run functions **Min-Instance** CPU / Memory (request-based billing) in us-east1» de `novuchat-demo`: **USD 0,54 por día, constante desde el 17/09** (el día 17 fue parcial), unos **USD 16 al mes**. Coincide con el «fijo ≈ USD 22 al mes» que estima NovuChat (unos 16 de la instancia mínima). Es **costo fijo**: se paga haya o no uso. La instancia mínima evita el arranque en frío de la consola; apagarla exige que NovuChat pruebe latencia y arranque en frío (no se propone sin esa prueba). Más pequeño: la CPU de `novuchatstaging`, unos 0,04 por día.

### Qué son los créditos

| Crédito | Tipo | Septiembre (USD) |
|---|---|---|
| Promoción mensual («CREDIT_TYPE_MONTHLY») | PROMOTION | −5,18 |
| «CPU Time (2nd Gen)» | DISCOUNT (capa gratuita) | −4,32 |
| «Memory Time (2nd Gen)» | DISCOUNT (capa gratuita) | −0,90 |

**El neto es cero por dos razones distintas:** unos 5,22 son la capa gratuita de CPU y memoria de segunda generación (descuento que no vence) y unos 5,18 son una promoción mensual. **No se pudo verificar** el tope ni el vencimiento de la promoción (la pantalla Facturación → Créditos solo la ve Andres).

## Octubre (parcial, 1 al 3)

Bruto 1,73 USD (0,69; 0,63; 0,42 por día en hora UTC), todo cubierto por créditos. De ellos, 1,48 son la instancia mínima de `novuchat-demo`. Si el ritmo se mantiene (unos 0,6 por día), octubre ronda los 18 USD brutos: **más que los 10,40 de septiembre**, porque la instancia mínima estuvo todo el mes. Si la promoción tiene un tope menor, el neto dejaría de ser cero.

## Qué dice y qué no

- **El 98 % del bruto es de NovuChat** (10,18 de 10,40).
- **No hay costo medido de PRETSO ni de Hipatia producción:** sus proyectos facturan por otras cuentas (…5B3F y …44F7) que no se exportan hoy (`docs/06` §3).
- **No hay serie histórica:** sin segundo ciclo ni media de tres meses no hay base para el umbral de anomalía del 20 %.
- **Dependencia:** si la promoción mensual termina o tiene tope, el costo neto pasa de 0 a lo que hoy es bruto (unos 10 a 18 USD al mes).

## Costo de la recolección
Consultas de 0,8 a 5,5 MB, facturadas por bytes procesados, dentro del primer TiB gratuito al mes (https://cloud.google.com/bigquery/pricing, vía catálogo de precios, 2026-09-30). **USD 0,00.**
