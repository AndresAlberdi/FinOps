# AWS — línea base de costos (cuenta de la demo de SeguroLoTengo, terminada en 8663)

| Versión | Fecha | Fuente |
|---|---|---|
| 0.1 | 2026-10-01 | Cost Explorer (`ce:GetCostAndUsage`), con el rol `finops-lectura` asumido por `Andres_Alberdi_1`. Costo bruto sin impuestos ni créditos (`UnblendedCost`), USD. Datos crudos en `datos/aws/` (no versionado) |

## Costo por servicio

| Servicio | Agosto 2026 | Septiembre 2026 |
|---|---|---|
| AWS Amplify | 0,00 | **4,17** |
| AWS Secrets Manager | 0,00 | 0,57 |
| Amazon Rekognition | 0,00 | 0,16 |
| Amazon DynamoDB | 0,00 | 0,03 |
| AWS Transfer Family | 0,00 | 0,03 |
| Amazon S3 y otros | 0,00 | < 0,01 |
| **Total** | **0,00** | **4,96** |

Septiembre, por día: media 0,17 USD; el día más caro fue el 1 de septiembre (1,40 USD).

## Qué dice y qué no

- **Es una cuenta pequeña:** menos de USD 5 al mes. No hay una palanca de ahorro de importancia aquí; el valor de esta línea base es detectar saltos.
- **Agosto en cero:** probablemente el plan gratuito o créditos de la cuenta (verificar en la facturación de AWS). Septiembre es el primer mes con cargo real. Por eso solo hay **un** ciclo comparable, no dos; no se puede calcular una media de tres meses todavía.
- **AWS Transfer Family: vigilar.** Costó 0,03 USD, pero ese servicio se factura por hora mientras el servidor esté activo (verificar tarifa en la página oficial de AWS). Si el servidor SFTP de la integración con Alianza se deja encendido todo el mes, el costo de octubre sería mucho mayor. Se anota para la revisión mensual; no se propone ningún cambio sin hablar con segurolotengo-demo.
- **AWS Secrets Manager** (0,57): se factura por secreto y por mes; es un costo fijo esperado.
- **Alcance:** una sola cuenta de AWS, la que ve el rol. Si hay otras (por ejemplo la de firma F2), faltan.

## Costo de la recolección
3 solicitudes a Cost Explorer a USD 0,01 cada una (https://aws.amazon.com/aws-cost-management/aws-cost-explorer/pricing/, consultada el 2026-09-30): **USD 0,03**.

## Siguiente paso
Repetir la lectura el primer día hábil de cada mes (`docs/02` §4) y marcar como anomalía cualquier mes que supere en más de 20 % la media de los tres anteriores, cuando existan.
