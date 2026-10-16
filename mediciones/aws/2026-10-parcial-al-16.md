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


## Detalle por tipo de uso (2026-10-16)

| Campo | Valor |
|---|---|
| Fuente | Cost Explorer (`ce:GetCostAndUsage`), rol `finops-lectura` de la cuenta terminada en 8663, solo lectura. Consulta del 2026-10-16 |
| Período | 1 al 16 de octubre (fin exclusivo 17). Diaria, agrupada por tipo de uso (USAGE_TYPE). Métrica `UnblendedCost`, USD. Ventana marcada por AWS como estimada |
| Crudos (no versionados) | `datos/aws/ce-2026-10-01a16-transfer-por-tipo-uso-diaria.json`, `datos/aws/ce-2026-10-01a16-amplify-por-tipo-uso-diaria.json` y `datos/aws/ce-2026-10-diaria-waf-por-tipo-uso.json` (este último de la lectura anterior, reutilizado) |

### a) AWS Transfer Family: cobro por hora o por archivo/GB

Total: 0,271 USD (coincide con los 0,27 de la tabla de servicios).

| Tipo de uso | USD | Parte |
|---|---|---|
| `SFTPConnectorCall-StartDirectoryListing` | 0,193 | 71 % |
| `SFTPConnectorCall-StartFileTransferResults` | 0,044 | 16 % |
| `SFTPConnectorCall-SendFilePath`, `-StartRemoteMove` y `-RetrieveFilePath` | 0,011 cada uno | 4 % cada uno |
| `SFTPConnector-RetrieveBytes` y `-SendBytes` | 0,001 | 0,3 % |

- Por hora (tipos «Hours»): **0 USD**. En la ventana no aparece ningún tipo de uso con horas.
- Por GB transferido: **0,001 USD** (bytes del conector).
- Por operación: **0,270 USD** (llamadas del conector SFTP, 99,7 %).
- Días con cargo: 2, 6, 7, 13 y 14 de octubre.
- Corrección: la nota de la sección «Amplify y Transfer Family por tramo» (servidor SFTP facturado por hora) no se sostiene para esta ventana. No hay evidencia de un servidor encendido facturado por horas; el cargo proviene de llamadas del conector, es decir, de actividad. El flujo que las origina lo debe identificar la sesión dueña.

### b) AWS WAF: composición (1,094 USD)

Sin consulta nueva: se sumó el archivo diario por tipo de uso de la lectura anterior (1 al 16 de octubre).

| Tipo de uso | USD | Parte |
|---|---|---|
| `Global-RuleV2` (reglas) | 0,552 | 50 % |
| `Global-WebACLV2` (ACL web) | 0,536 | 49 % |
| `Global-RequestV2-Tier0` (solicitudes) | 0,006 | 0,6 % |

- ACL y reglas suman 99 %; las solicitudes pesan menos de 1 %. El cargo es, por tanto, de cuotas por ACL y por regla, no de tráfico (verificar frente a la tarifa oficial de AWS WAF).
- Inicia el 12 de octubre. Del 13 al 15, el cargo diario de la ACL es 0,161 USD (5/31 de una cuota mensual prorrateada en 31 días) y el de reglas varía entre 0,136 y 0,194 USD (verificar).
- Alcance «Global» (CloudFront), como en la lectura anterior.

### c) AWS Amplify: qué explica el salto del 12 al 16

| Tipo de uso | 1 al 11 oct (USD) | 12 al 16 oct (USD) | Total 1 al 16 (USD) | Parte del 12 al 16 |
|---|---|---|---|---|
| `BuildDuration` (minutos de compilación) | 2,045 | 2,326 | 4,370 | 58 % |
| `AmplifyWAF` (protección WAF gestionada desde Amplify) | 0,000 | 1,606 | 1,606 | 40 % |
| Cómputo SSR (`HostingComputeRequestDuration` y `HostingComputeRequestCount`) | 0,019 | 0,091 | 0,110 | 2 % |
| Ancho de banda y almacenamiento (`DataTransferOut` y `DataStorage`) | 0,002 | 0,009 | 0,011 | 0,2 % |
| **Total** | **2,066** | **4,033** | **6,098** | 100 % |

- Builds: pico el 12 de octubre (1,16 USD), luego 0,56 (13), 0,38 (14), 0,08 (15) y 0,14 (16, día parcial). Es el componente principal del salto. Cost Explorer no muestra el número de compilaciones ni la rama (verificar en la consola de Amplify, sesión dueña).
- `AmplifyWAF`: 0,074 el 12 (parcial), 0,484 diarios del 13 al 15 (múltiplo de 5/31, es decir, cuota fija diaria) y 0,081 el 16 (parcial). No es consumo de tráfico.
- SSR y transferencia de datos: marginales (2 % y 0,2 %). El ancho de banda no explica el salto.
- Vínculo con AWS WAF: ambas líneas empiezan el 12 de octubre. Hipótesis no confirmada: la protección WAF que Amplify activa crea la ACL Global que se factura en la línea de AWS WAF. Si se confirma, WAF y Amplify juntos suman 2,70 USD (cerca de 32 % del total de octubre parcial). Confirmar con la sesión dueña y con la página de precios de Amplify (verificar).

### Huecos de datos

- Los días 17 al 31 de octubre no están medidos; el 16 es día parcial; la ventana está marcada como estimada por AWS.
- Cost Explorer no entregó desglose por recurso, aplicación ni rama: no se identificó la aplicación de Amplify ni el servidor SFTP.
- Tarifas de AmplifyWAF, AWS WAF y del conector SFTP no verificadas contra la fuente oficial en esta lectura (verificar).
- Una sola cuenta (terminada en 8663).

### Costo de la recolección

- Solicitudes nuevas a Cost Explorer: **2** (Transfer Family diaria por tipo de uso y Amplify diaria por tipo de uso). Costo: USD 0,02.
- AWS WAF: 0 solicitudes nuevas; se reutilizó el archivo diario por tipo de uso ya existente.
- Acumulado con la lectura anterior (declarada en 4 solicitudes): 6 solicitudes, USD 0,06.
- Llamadas STS (identidad y asunción de rol): sin costo. Ninguna operación de escritura.

### Siguiente paso

- Sesión dueña de la cuenta (SeguroLoTengoDemo, verificar): confirmar si la protección WAF de Amplify activada el 12 de octubre es la esperada, y cuántas compilaciones se dispararon del 12 al 14.
- Confirmar qué flujo llama al conector SFTP (listados y transferencias).
- Repetir la lectura el 1 de noviembre, con octubre cerrado.

## Dueños y decisiones (2026-10-16)
- **Respuesta de la sesión de SeguroLoTengo** (de su documentación, sin consultar Cost Explorer): el WAF (`slt-demo-web-acl`, CloudFront/global) es suyo y esperado, asociado a la app Amplify de la demo desde el 12-oct, con 6 reglas y un costo estimado de USD 9–11 al mes. Transfer Family es un **conector SFTP** hacia el servidor de Alianza (creado el 13-oct), no un servidor propio encendido. El salto de Amplify del 12-oct se debe al dominio propio con tráfico de operadores y a las ramas `staging` y `pruebas` con muchos builds.
- **Verificado en Cost Explorer por tipo de uso:** Transfer Family **no cobra por hora** (0 USD); cobra por operación (0,270 USD, de ellos 0,193 por listados del conector) y por GB (0,001). Coincide con la hipótesis de SeguroLoTengo. Amplify del 12 al 16-oct: builds 58 % y un cargo **AmplifyWAF de 1,606 USD (40 %)**, además del WAF propiamente dicho.
- **Lo que no cuadra con la estimación de SeguroLoTengo:** WAF (1,094) más AmplifyWAF (1,606) suman 2,70 USD en 5 días, un ritmo de ~0,54 USD por día (~16 USD al mes), por encima de los USD 9–11 que SeguroLoTengo estimó. La estimación probablemente no incluía el cargo de Amplify por la integración del firewall. **Tarifas por verificar en la página oficial de AWS** (ver invariante 7).
- **Decisión de Andres (2026-10-16):** aprueba el costo del WAF. El WAF es un control protegido y FinOps no propone recortarlo; queda por comunicar a SeguroLoTengo que el ritmo observado es mayor que el estimado.
- **Palanca candidata (no es propuesta formal):** apagar la rama `pruebas` (`pruebas_rama_habilitada=false` por Terraform) al terminar las pruebas de Rodrigo reduce builds, que son el 58 % del salto de Amplify. Requiere su prueba de no regresión y su reversión, y la autorización de Andres.
