# 01 · Inventario de servicios y fuentes de datos de costo

| Versión | Fecha | Estado |
|---|---|---|
| 0.1 | 2026-09-28 | Estructura; las filas se completan y verifican en el Bloque 1 |

Este documento dice **de dónde sale el dato de costo** de cada servicio y con qué identidad se lee. Las cuentas y proyectos concretos no se repiten aquí: viven en el inventario de SeguridadGeneral y se citan por su nombre corto. Identificadores, solo por últimos dígitos.

## 1. Fuentes de datos por proveedor

| Proveedor | Fuente de costo (preferida → alternativa) | Granularidad | Acceso de solo lectura requerido | Estado |
|---|---|---|---|---|
| Anthropic — plan Max | claude.ai → Settings → Usage (sesión, semana, créditos de uso) | Diaria | Cuenta del titular (lectura en pantalla) | Pendiente |
| Anthropic — API/Console | Console → Usage y Cost; Admin API de uso y costos (verificar disponibilidad) | Diaria por modelo | Clave de administración de solo lectura, si existe (verificar) | Pendiente |
| Claude Code | `/usage` y `/cost` en sesión; registro de tokens por sesión | Por sesión | Local | Pendiente |
| AWS | Cost Explorer (API `ce:GetCostAndUsage`) → Cost and Usage Report (CUR 2.0) en S3 | Diaria por servicio y etiqueta | Rol con `ce:Get*`, `ce:Describe*`, `budgets:View*` por OIDC | Pendiente |
| Google Cloud / Firebase | Exportación de facturación a BigQuery → informes de Billing en consola | Diaria por proyecto y SKU | `roles/billing.viewer` + `roles/bigquery.dataViewer` sobre el dataset | Pendiente |
| Gemini / Vertex AI | Mismo export de facturación (SKU de Vertex/Gemini) + métricas de uso del proyecto | Diaria | Incluido en la fila anterior | Pendiente |
| OCI | Usage API / Cost Analysis → informes de costo en Object Storage | Diaria por compartment | Política `read usage-report` / `inspect` en la tenencia | Pendiente |
| n8n | Historial de ejecuciones (API pública de n8n, lectura) + costo de la VM en OCI | Por ejecución | API key de n8n con alcance de lectura (verificar alcances) | Pendiente |
| Meta — WhatsApp | WhatsApp Manager → Insights de costos; Graph API `pricing_analytics` / `conversation_analytics` (verificar vigencia) | Diaria por categoría y número | Token de usuario de sistema con `whatsapp_business_management` (solo lectura) | Pendiente |
| GitHub | Facturación de la cuenta/organización; API de uso de Actions | Mensual / diaria | Token de grano fino con lectura de facturación (verificar alcance) | Pendiente |
| Suscripciones SaaS | Facturas del correo del titular (Gmail) | Mensual | Conector de Gmail, lectura | Pendiente |

## 2. Registro de servicios

Una fila por servicio contratado. Se completa en el Bloque 1 desde las fuentes de §1 y desde las fichas de `~/Claude-Proyectos/proyectos/`.

| Servicio | Proveedor | Proyecto(s) que lo usan | Modalidad (suscripción / consumo / compromiso) | Dueño técnico | Costo mensual de línea base | Fuente |
|---|---|---|---|---|---|---|
| | | | | | | |
