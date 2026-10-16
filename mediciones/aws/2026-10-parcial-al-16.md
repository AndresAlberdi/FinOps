# AWS — costo parcial de octubre 2026 (1 al 16) frente a septiembre

| Versión | Fecha | Fuente |
|---|---|---|
| 0.1 | 2026-10-16 | Cost Explorer (`ce:GetCostAndUsage`), rol `finops-lectura` asumido desde el perfil `finops` (solo lectura). Cuenta terminada en 8663. Costo bruto, métrica `UnblendedCost`, USD, agrupado por servicio. Ventana de octubre marcada por AWS como estimada. Datos crudos en `datos/aws/` (no versionado) |

Comparación justa: septiembre 1 al 16 frente a octubre 1 al 16 (mismo número de días). La línea base de septiembre completo (USD 5,30) está en `mediciones/aws/2026-09-linea-base.md`.

## Totales

| Período | Costo (USD) | Promedio por día (USD) |
|---|---|---|
| Septiembre 1 al 16 | 3,52 | 0,22 |
| Octubre 1 al 16 | **8,56** | 0,54 |
| Variación | +5,04 (+143 %) | +0,32 por día |

La variación es un salto de uso, no de tarifa: los días 12 al 16 de octubre suman unos 5,2 de los 8,56 del período (Amplify, WAF y Transfer Family; ver la tabla de tramos).

## Costo por servicio

| Servicio | Sep 1–16 | Oct 1–16 | Variación | Nota |
|---|---|---|---|---|
| AWS Amplify | 3,12 | 6,10 | +2,97 (+95 %) | 4,03 solo del 12 al 16 de octubre |
| AWS WAF | 0,00 | 1,09 | nuevo | Aparece el 12 de octubre (ver hallazgo) |
| AWS Secrets Manager | 0,22 | 0,63 | +0,41 | Costo fijo por secreto |
| Amazon Rekognition | 0,16 | 0,30 | +0,14 | |
| AWS Transfer Family | 0,00 | 0,27 | nuevo en la ventana | En septiembre completo fue 0,03 (cargo posterior al día 16) |
| AWS Cost Explorer | 0,00 | 0,07 | +0,07 | Incluye consultas de lecturas anteriores de octubre |
| Amazon DynamoDB | 0,02 | 0,08 | +0,06 | |
| Amazon S3 | 0,00 | 0,01 | +0,01 | |
| Amazon SES | 0,00 | 0,00 | — | 0,0002 en septiembre; sin cargo en octubre |
| Textract, SNS, KMS, Glue, CloudWatch, impuestos | 0,00 | 0,00 | — | Sin cargo en la ventana |
| **Total** | **3,52** | **8,56** | **+5,04** | |

## Amplify y Transfer Family por tramo

| Tramo | Amplify (USD) | Transfer Family (USD) |
|---|---|---|
| Oct 1 al 3 | 1,04 | 0,04 |
| Oct 4 al 11 | 1,03 | 0,14 |
| Oct 12 al 16 | 4,03 | 0,09 |
| **Oct 1 al 16** | **6,10** | **0,27** |

- Amplify: en octubre 1 al 3 la cifra revisada es 1,04 frente a 0,99 de la línea base v0.2 (revisión de la estimación de AWS, +0,05). No cambia la conclusión.
- Amplify pasó de 0,13 por día (4 al 11) a 0,81 por día (12 al 16), unas seis veces más.
- Transfer Family: 0,27 en 16 días, frente a 0,03 de todo septiembre. El servidor SFTP se factura por hora (verificar tarifa oficial); conviene confirmar si quedó encendido (ver hallazgo).

## Hallazgo: servicio nuevo sin dueño identificado (AWS WAF)

- Cargo de WAF desde el 12 de octubre: 1,09 USD en cinco días. Corresponde a un Web ACL de uso «Global» (alcance de CloudFront según el tipo de uso), con reglas y solicitudes.
- Coincide con el tramo de aumento de Amplify (12 al 16). Es una hipótesis de correlación, no una conclusión: no se identificó el recurso ni su dueño.
- WAF es un control del estándar (`docs/03-guardarrailes.md` §1): no se propone quitarlo. Se pide confirmar a la sesión dueña del proyecto que el recurso es esperado. No se siguió recolectando ni se consultaron los recursos.

## Huecos de datos

- Octubre llega hasta el día 16; los días 17 al 31 no están medidos.
- Septiembre 17 al 30 no se volvió a leer: se usa el total de la línea base (5,30).
- Una sola cuenta (terminada en 8663). Otras cuentas del inventario (por ejemplo, firma F2) no están en el alcance del rol consultado.
- No se agrupó por tipo de registro en esta lectura. No aparecen importes negativos (créditos) en los grupos; impuestos en 0.
- Cifras de octubre con la marca de estimación de AWS: pueden cambiar en las próximas lecturas.

## Costo de la recolección

- Solicitudes a Cost Explorer en esta lectura: **4** (una por servicio mensual octubre, una mensual de septiembre 1 al 16, una diaria de Transfer Family y Amplify, una diaria de AWS WAF por tipo de uso). A USD 0,01 cada una: **USD 0,04**.
- Las llamadas de identidad (`sts get-caller-identity`, `sts assume-role`) no tienen costo.
- Ninguna operación de escritura o de modificación.

## Siguiente paso

- Confirmar con el dueño de la cuenta el recurso WAF y el servidor SFTP de Transfer Family.
- Repetir la lectura del 1 de noviembre (`docs/02` §4) con octubre cerrado y comparar contra septiembre (5,30) y contra la media de los meses anteriores cuando existan.
