# Google Cloud — octubre parcial (1 al 16-oct) frente a septiembre

| Versión | Fecha | Estado |
|---|---|---|
| 0.1 | 2026-10-16 | Lectura de solo SELECT sobre la exportación de facturación a BigQuery (opción B, US). Datos hasta el 16-oct (la exportación llega con un retraso de hasta un día). Cifras agregadas; los resultados crudos están en `datos/gcp/` (ignorado por git). |

Fuente: exportación a BigQuery de la cuenta principal (…603EC8, dataset `billing_export` del proyecto `novuchatstaging`) y de la cuenta C (…5DBD7A, proyecto dedicado). Consulta: la de septiembre (`datos/gcp/consulta-a.sql` y `consulta-c.sql`) con el filtro `usage_start_time >= 2026-10-01`. Consultada el 2026-10-16.

## Resultado

| Cuenta | Bruto 1–16 oct | Créditos | Neto | Septiembre (completo) |
|---|---|---|---|---|
| Principal (…603EC8) | **18,18** | −18,18 | **0,00** | bruto 10,40, neto 0,00 |
| C (…5DBD7A) | **2,10** | −1,32 | **0,79** | Gemini API 24,91 |

**Lectura.** La cuenta principal lleva en 16 días un bruto 75 % mayor que todo septiembre, pero los créditos aún lo cubren al 100 %. Una extrapolación lineal a mes completo da ~35 USD brutos (**sin medir y que sobreestima**: ~7,4 USD de Vertex AI fueron puntuales, y la instancia fija aporta ~16 USD al mes), y la promoción y la capa gratuita **no tienen tope ni vencimiento verificados** (los ve solo Andres): si se agotan, el gasto pasa a pagarse.

## Cuenta principal — por proyecto (bruto, USD)
| Proyecto | Bruto | Principales servicios |
|---|---|---|
| `novuchat-demo` | 16,56 | Cloud Run Functions 8,51 (la instancia mínima fija ≈0,54/día × 16 ≈ 8,6); **Vertex AI 7,38 (4 al 12-oct)**; Secret Manager 0,65 |
| `novuchatstaging` | 1,10 | Secret Manager 0,65; Cloud Run Functions 0,42 |
| `novuchat-site` | 0,33 | Vertex AI 0,23; Secret Manager 0,09 |
| `whatsappmodular` | 0,16 | Secret Manager |
| `puntosnb` | 0,03 | Cloud Run Functions |

**Hallazgo:** Vertex AI en `novuchat-demo` fue **7,38 USD entre el 4 y el 12-oct**, algo que septiembre no tenía a esa escala. Es compatible con las baterías reales del chat de captación y otras pruebas contra el modelo; no es defecto, pero es el mayor movimiento nuevo. Lo cubren los créditos hoy.

## Cuenta C (Gemini API y RAG) — por proyecto (bruto, USD)
| Proyecto | Bruto | Neto | Servicios |
|---|---|---|---|
| `rag-generico` | 1,32 | 0,00 | Artifact Registry 0,85; Vertex AI 0,44; Cloud Run 0,02 (desde el 10-oct) |
| `novuchatdemo` (Gemini API) | 0,79 | 0,79 | Gemini API, sin crédito (prepago) |

**Gemini API bajó de 24,91 (septiembre) a 0,79 (1–16 oct):** septiembre incluyó las baterías del 29 y 30/09 y el concurso de Bellido; no se repitieron.

## Límites
- La identidad usada fue una **cuenta de usuario del titular** con permiso de trabajos de BigQuery, no la cuenta de servicio de solo lectura `finops-lectura` que prevé `docs/04-accesos.md` (sigue «Pendiente»). Cada consulta fue un SELECT, de unos 0,1 a 5 MB; no se modificó ningún recurso. Se documenta la desviación para decidir si se otorgan los roles de lectura (`roles/bigquery.dataViewer` y `roles/bigquery.jobUser`).
- No cubre PRETSO (…5B3F) ni Hipatia producción (…44F7): esas cuentas no se exportan.
- Sin precios nuevos citados; solo se leyó el costo ya facturado por Google.
