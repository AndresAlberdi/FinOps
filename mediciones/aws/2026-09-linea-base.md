# AWS — línea base de costos (cuenta de la demo de SeguroLoTengo, terminada en 8663)

| Versión | Fecha | Fuente |
|---|---|---|
| 0.2 | 2026-10-11 | Relectura del 2026-10-04 con el mismo rol, ya con septiembre cerrado y octubre parcial (1 al 3). **Corrige la v0.1: septiembre es 5,30 y no 4,96** (la lectura del 1/10 salió con los últimos días sin cerrar). Sin créditos ni impuestos en septiembre ni octubre (agrupado por tipo de registro: solo «Usage»; «Tax» 0) |
| 0.1 | 2026-10-01 | Cost Explorer (`ce:GetCostAndUsage`), con el rol `finops-lectura` asumido por `Andres_Alberdi_1`. Costo bruto sin impuestos ni créditos (`UnblendedCost`), USD. Datos crudos en `datos/aws/` (no versionado) |

## Costo por servicio

| Servicio | Agosto 2026 | Septiembre 2026 | Octubre 1–3 |
|---|---|---|---|
| AWS Amplify | 0,00 | **4,49** (v0.1: 4,17) | 0,99 |
| AWS Secrets Manager | 0,00 | 0,59 (v0.1: 0,57) | 0,10 |
| Amazon Rekognition | 0,00 | 0,16 | 0,00 |
| Amazon DynamoDB | 0,00 | 0,03 | < 0,01 |
| AWS Transfer Family | 0,00 | 0,03 | **0,04** |
| AWS Cost Explorer | 0,00 | 0,00 | 0,03 (las consultas de esta lectura) |
| Amazon S3 y otros | 0,00 | < 0,01 | < 0,01 |
| **Total** | **0,00** | **5,30** | **1,17** |

Septiembre, por día: media 0,18 USD. **Octubre va al doble: 0,39 USD por día** (1,17 en tres días), sobre todo Amplify (0,33 por día: la rama de staging de Bancard y la entrega de SeguroLoTengo). A este ritmo octubre ronda los 12 USD (extrapolación).

## Qué dice y qué no

- **Es una cuenta pequeña:** menos de USD 5 al mes. No hay una palanca de ahorro de importancia aquí; el valor de esta línea base es detectar saltos.
- **Agosto en cero:** sin uso (no hay créditos aplicados en ningún mes: la cuenta paga lo que consume). Septiembre es el primer mes con cargo real. Por eso solo hay **un** ciclo comparable, no dos; no se puede calcular una media de tres meses todavía.
- **AWS Transfer Family: vigilar.** Costó 0,03 USD en septiembre y **0,04 en solo tres días de octubre**, más que todo septiembre. Equivale a pocos minutos de servidor encendido (verificar tarifa en la página oficial de AWS), así que el servidor SFTP sigue apagado salvo pruebas; ese servicio se factura por hora mientras esté activo. Si el servidor SFTP de la integración con Alianza se deja encendido todo el mes, el costo de octubre sería mucho mayor. Se anota para la revisión mensual; no se propone ningún cambio sin hablar con segurolotengo-demo.
- **AWS Secrets Manager** (0,57): se factura por secreto y por mes; es un costo fijo esperado.
- **Alcance:** una sola cuenta de AWS, la que ve el rol. Si hay otras (por ejemplo la de firma F2), faltan.

## Costo de la recolección
Cost Explorer a USD 0,01 por solicitud (https://aws.amazon.com/aws-cost-management/aws-cost-explorer/pricing/, consultada el 2026-09-30): 3 solicitudes el 1/10 y 5 el 4/10 (la última, tipo de registro): **USD 0,08**.

## Siguiente paso
Repetir la lectura el primer día hábil de cada mes (`docs/02` §4) y marcar como anomalía cualquier mes que supere en más de 20 % la media de los tres anteriores, cuando existan.
