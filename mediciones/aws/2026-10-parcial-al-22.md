# AWS — octubre parcial al 22 (cuenta …8663, demo)

> Fecha de consulta: 2026-10-23. Fuente: Cost Explorer (`get-cost-and-usage`, `UnblendedCost`, us-east-1) con el rol de solo lectura `finops-lectura` (perfil `finops-lectura`, agregado a `~/.aws/config` el 2026-10-23 con la autorización de Andres; sin credenciales en disco). Solo cifras agregadas; los datos crudos están en `datos/aws/` (ignorado por git). Cost Explorer puede mostrar un desfase de horas.
> Alcance: la cuenta …8663 (demo de SeguroLoTengo, WAF y Amplify). La cuenta de producción de SeguroLoTengo (`slt-produccion`) no se lee con este rol.

## Resumen

| Concepto | Octubre 1–22 | Septiembre 1–22 |
|---|---|---|
| Total | **USD 29,55** | USD 3,93 |
| AWS Amplify | 18,43 | 3,39 |
| AWS WAF | 7,31 | 0,00 |
| Amazon Rekognition | 1,22 | 0,16 |
| AWS Secrets Manager | 1,04 | 0,36 |
| AWS Key Management Service | 0,76 | 0,00 |
| AWS Transfer Family | 0,49 | 0,00 |
| AWS Cost Explorer | 0,13 | 0,00 |
| Otros (DynamoDB, S3, Athena, SES, CloudTrail) | ≈0,15 | ≈0,02 |

Octubre es ≈7,5 veces septiembre en los mismos días. Respecto del corte del 16/10 (USD 8,56), el total se multiplicó por ≈3,5 en seis días.

## Serie diaria (USD)

1/10 0,69 · 2/10 0,40 · 3/10 0,13 · 4/10 0,08 · 5/10 0,18 · 6/10 0,09 · 7/10 0,13 · 8/10 0,33 · 9/10 0,26 · 10/10 0,15 · 11/10 0,39 · **12/10 1,69** · 13/10 1,44 · 14/10 1,32 · 15/10 0,97 · 16/10 1,94 · 17/10 2,29 · 18/10 3,03 · 19/10 3,35 · **20/10 4,74** · 21/10 2,86 · 22/10 3,07.

Hasta el 11/10 el gasto era de ≈0,2 USD/día; desde el 12/10 (alta del WAF) es de 1,3 a 4,7 USD/día.

## Amplify por tipo de uso (12–22/10)

| Tipo de uso | USD | Cantidad |
|---|---|---|
| `BuildDuration` (builds) | 8,18 | ≈818 minutos |
| `AmplifyWAF` | 7,94 | — |
| `HostingComputeRequestDuration` | 0,23 | — |
| Transferencia y almacenamiento | ≈0,02 | — |

Lectura: de los USD 16,4 de Amplify en esos 11 días, **la mitad son builds (≈818 minutos, ≈74 min/día) y la otra mitad es el complemento WAF de Amplify**.

## Hallazgos

1. **El WAF cuesta más de lo aprobado.** El 16/10 Andres decidió mantener el WAF al ritmo observado (~16 USD al mes, ≈0,54 USD/día). Entre el 12 y el 22/10 las dos líneas de WAF suman **USD 15,25** (AWS WAF 7,31 + `AmplifyWAF` 7,94), es decir ≈1,39 USD/día, **≈41 USD al mes**, alrededor de 2,5 veces lo aprobado. **[Pendiente de confirmar]**: si las dos líneas corresponden a dos ACL distintas o a la misma facturada por dos servicios; el rol de lectura no puede listar recursos de WAF ni de Amplify.
2. **Builds de Amplify en la demo:** ≈818 minutos en 11 días. SeguroLoTengo Principal informó que la app de **producción** tuvo 35 builds del 16 al 22/10 (≈175 minutos), por lo que la mayor parte de los 818 minutos viene de las ramas de la **demo** (`main`, `staging`, `pruebas`). Su perfil no puede contarlos; el rol `finops-lectura` tampoco (`amplify:ListApps` denegado).
3. **Rekognition (1,22 USD):** pruebas de Face Liveness (USD 0,015 por sesión).
4. **Secrets Manager y KMS:** suben por las claves y secretos nuevos de las integraciones; son controles de seguridad y no son candidatos a ahorro (guardarraíles §1).

## Palancas candidatas (sin ejecutar)

- **Agrupar los pushes a `pruebas`** y avisar antes de cada uno (propuesta de SeguroLoTengo Principal): menos builds. Reversión: ninguna, es un hábito de trabajo. Prueba: minutos de `BuildDuration` por día antes y después.
- **Apagar o espaciar los builds de `pruebas` al terminar las pruebas de Rodrigo:** decide Andres; requiere su prueba de no regresión y reversión.
- **WAF:** no se propone bajar el WAF (es un control de seguridad, guardarraíles §1); solo **confirmar el costo real** y que no haya un ACL duplicado.

## Limitaciones

- Un solo lector (Cost Explorer); sin acceso a las listas de recursos de Amplify, WAF ni a las ejecuciones de build.
- El efecto de los créditos o descuentos de la cuenta no está reflejado (se usa `UnblendedCost`).
- La cifra de Rekognition de septiembre de 0,16 y la de octubre de 1,22 provienen de la misma fuente; no se verificó contra la factura.
