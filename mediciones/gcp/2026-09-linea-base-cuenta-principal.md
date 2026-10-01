# Google Cloud — línea base de la cuenta de facturación principal (terminada en 603EC8)

| Versión | Fecha | Estado |
|---|---|---|
| 0.1 | 2026-10-01 | **PROVISIONAL: datos incompletos** (el llenado inicial del export sigue en curso) |

Fuente: exportación de facturación a BigQuery (costo de uso estándar), dataset `billing_export` en `US` del proyecto `novuchatstaging` (el tope de 5 proyectos por cuenta de facturación impidió uno dedicado). La cuenta factura 5 proyectos: `novuchat-demo`, `novuchat-site`, `novuchatstaging`, `puntosnb` y `whatsappmodular`; el export también registra algo de `aab1-landing` y `encuentramebo-1`. Costo bruto en USD; datos crudos en `datos/gcp/`.

## Lo que se sabe al 2026-10-01 (parcial: la tabla llega hasta el 6 de septiembre)

| Mes | Costo bruto (USD) | Créditos (USD) | Neto (USD) |
|---|---|---|---|
| 2026-08 | −0,0003 | −0,0001 | −0,0004 |
| 2026-09 (hasta el 6) | 0,2024 | −0,2025 | **−0,0001 ≈ 0** |

- **El gasto bruto parcial es casi todo Vertex AI en `novuchat-site` (0,18, del 2 al 6 de septiembre)** más Cloud Run Functions en `novuchat-demo` y `novuchat-site`. **Está cubierto íntegramente por créditos**: el neto es cero.
- **Los créditos importan:** mientras duren, esta cuenta no paga nada. Hay que saber de qué tipo son (prueba gratuita, promoción, Firebase) y cuándo vencen, porque cuando se agoten el costo pasa de 0 a lo que hoy es bruto. **Pendiente: leer el desglose de créditos** (`credits.name`/`credits.type`) cuando la tabla esté completa.
- **Todo lo demás de la tabla es de centavos o cero**: Artifact Registry, Firebase Hosting, Cloud Storage, Secret Manager, reCAPTCHA, App Engine y Cloud Logging.
- **Aún no se puede concluir nada del mes:** faltan los días 7 a 30.

## Siguiente paso
Releer a partir del 2026-10-06, con la misma comprobación de `MAX(usage_start_time)`, y consolidar con la cuenta C en una sola línea base de Google. Añadir el desglose de créditos.

## Costo de la recolección
Dos consultas (simulación y real) sobre 159 KB, facturadas al mínimo de 10 MiB: **USD 0,00**.
