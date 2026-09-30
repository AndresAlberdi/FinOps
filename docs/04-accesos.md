# 04 · Accesos de solo lectura

| Versión | Fecha | Estado |
|---|---|---|
| 0.2 | 2026-09-30 | Políticas preparadas (§2); pendientes de otorgar. Precios y comportamientos con fuente y fecha |

Principios: identidad dedicada al proyecto; solo lectura; federación OIDC/WIF desde GitHub Actions cuando la consulta corra en CI; ninguna clave estática en el repositorio; verificar la cuenta activa antes de operar (`~/SeguridadGeneral/01-seguridad/10-inventario-de-proyectos.md` §3, «Regla que queda»).

| Proveedor | Identidad | Permisos (mínimos) | Quién la otorga | Estado |
|---|---|---|---|---|
| AWS | Rol `finops-lectura` asumible por OIDC | `ce:Get*`, `ce:Describe*`, `ce:List*`, `budgets:View*`, `cur:Describe*`; lectura del bucket del CUR si se habilita | Titular (consola IAM) — Claude prepara la política | Pendiente |
| Google Cloud | Cuenta de servicio `finops-lectura` por WIF | `roles/billing.viewer` en la cuenta de facturación; `roles/bigquery.dataViewer` y `roles/bigquery.jobUser` sobre el dataset del export | Titular (por cada una de las tres cuentas de Google) | Pendiente |
| OCI | Grupo `finops-lectura` | `allow group finops-lectura to read usage-report in tenancy`; `inspect` de recursos | Titular | Pendiente |
| n8n | API key de lectura | Lectura de ejecuciones y flujos (verificar alcances disponibles en la versión instalada) | Titular | Pendiente |
| Meta | Usuario de sistema de solo lectura | `whatsapp_business_management` (lectura de analítica) | Titular | Pendiente |
| Anthropic | Titular / clave de administración de lectura (verificar) | Uso y costo | Titular | Pendiente |
| GitHub | Token de grano fino | Lectura de facturación y de uso de Actions (verificar alcance) | Titular | Pendiente |

Los valores (ARN, IDs de cuenta de facturación, tokens) se cargan como secretos o variables de GitHub, o en el gestor de secretos de la nube; nunca en archivos versionados.

## 2. Políticas preparadas y qué debe conocer quien las otorga

Ninguna está otorgada. Cada fila dice qué se necesita, qué cuesta consultarlo y qué se pierde si se demora. Las tarifas y comportamientos se consultaron el 2026-09-30 en las páginas oficiales citadas; lo no confirmado lleva «(verificar)».

### 2.1 AWS — rol `finops-lectura` por OIDC

- **Permiso (solo lectura):** `ce:Get*`, `ce:Describe*`, `ce:List*`, `budgets:ViewBudget`, `budgets:DescribeBudgetActionsForAccount`, `cur:DescribeReportDefinitions`. Contrastar la lista contra la referencia de autorización de IAM para Cost Explorer antes de otorgar (verificar: la consulta automática de esa página no devolvió la tabla).
- **Confianza:** proveedor OIDC de GitHub, limitado a este repositorio y a la rama `main`; sin claves estáticas (`docs/03` §1.6).
- **Costo de consultar:** USD 0,01 por solicitud a la API de Cost Explorer, sin nivel gratuito para la API (https://aws.amazon.com/aws-cost-management/aws-cost-explorer/pricing/, 2026-09-30). Una línea base mensual por servicio cuesta decenas de solicitudes, es decir, centavos; la recolección debe agrupar por día y servicio en pocas llamadas y **declarar cuántas hizo**.
- **Se necesita en:** cada cuenta de AWS del inventario (SeguroLoTengoDemo y firma F2; verificar cuántas y cuáles).

### 2.2 Google Cloud — cuenta de servicio `finops-lectura` por WIF (por cada una de las tres cuentas)

- **Permisos:** `roles/billing.viewer` en la cuenta de facturación; `roles/bigquery.dataViewer` y `roles/bigquery.jobUser` sobre el dataset de la exportación.
- **Lo urgente es activar la exportación de facturación a BigQuery, hoy sin datos.** Según la documentación oficial (https://docs.cloud.google.com/billing/docs/how-to/export-data-bigquery, 2026-09-30): en un conjunto de datos **multirregional (US o UE)** la exportación incluye los datos desde el inicio del mes anterior a la primera activación, y el llenado inicial puede tardar **hasta cinco días**; en un conjunto **regional**, solo hay datos desde la fecha de activación, sin retroactivo.
- **Consecuencia:** con un dataset regional (la preferencia de Andres es `us-east1`, sin multirregional) cada día de demora es un día menos de línea base, y los ciclos anteriores hay que bajarlos a mano como CSV desde la consola de facturación; con multirregional `US` el retroactivo es automático. Decide Andres (`ESTADO.md`). Sin exportación no hay dos ciclos completos que comparar.
- **Quién activa la exportación:** un administrador de la cuenta de facturación (rol exacto: verificar en la página citada; el resumen automático no lo devolvió). No es una acción de este proyecto.
- **Costo de consultar y guardar (BigQuery, USD, catálogo de precios de Google, 2026-09-30):** las consultas cuestan 6,25 por TiB con el primer TiB del mes gratis, igual en `US` y en `us-east1`. El almacenamiento activo tiene los primeros 10 GiB gratis; después 0,02 por GiB-mes en `US` multirregional y 0,023 en `us-east1`. **La exportación de facturación pesa megabytes: queda dentro de la cuota gratuita en ambas opciones.** La multirregional no cuesta más que la regional.

### 2.3 OCI, n8n, Meta, Anthropic y GitHub

| Proveedor | Identidad y permiso | Qué hay que verificar antes de pedirlo |
|---|---|---|
| OCI | Grupo `finops-lectura`; lectura de informes de uso y `inspect` de recursos | La política de lectura de informes de uso exige una declaración entre tenencias; confirmar el texto exacto en la documentación oficial de OCI (verificar) |
| n8n | Clave de API de lectura | Qué alcances ofrece la versión instalada (verificar) |
| Meta | Usuario de sistema con `whatsapp_business_management`, solo lectura | Que la analítica de precios (`pricing_analytics`) siga vigente (verificar) |
| Anthropic | La cuenta del titular (plan) y, si existen claves de API, la Admin API de uso y costo | Si hay consumo de API real; si no, este proveedor se mide solo con `get_usage` (ya activo) |
| GitHub | Token de grano fino con lectura de facturación y uso de Actions | Qué alcance expone la facturación de cada cuenta (verificar) |

### 2.4 Orden de pedido a Andres

1. **Google Cloud — activar la exportación multirregional en las tres cuentas.** Es lo que más pesa y no admite demora.
2. AWS — el rol de lectura (§2.1).
3. El resto, en el orden de §2.3, cuando haya una línea base utilizable de los dos primeros.
