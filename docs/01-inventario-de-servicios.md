# 01 · Inventario de servicios y fuentes de datos de costo

| Versión | Fecha | Estado |
|---|---|---|
| 0.2 | 2026-09-30 | Registro de servicios completado desde las fuentes de SeguridadGeneral y Claude-Proyectos; costos pendientes de acceso |

Este documento dice **de dónde sale el dato de costo** de cada servicio y con qué identidad se lee. Las cuentas y proyectos concretos no se repiten aquí: viven en el inventario de SeguridadGeneral y se citan por su nombre corto. Identificadores, solo por últimos dígitos.

## 1. Fuentes de datos por proveedor

| Proveedor | Fuente de costo (preferida → alternativa) | Granularidad | Acceso de solo lectura requerido | Estado |
|---|---|---|---|---|
| Anthropic — plan Max | `get_usage` de la app (cuota por ventana) → claude.ai → Settings → Usage | Del momento; sin historia | Ninguno adicional | **Activa** (`mediciones/claude/`) |
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

| | |
|---|---|
| Versión | 0.2 · 2026-09-30 |
| Fuentes leídas | `~/SeguridadGeneral/01-seguridad/10-inventario-de-proyectos.md` §3 y §4 (cuentas, proyectos, etapa) y las fichas de `~/Claude-Proyectos/proyectos/` (la mayoría aún son plantillas vacías) |
| Regla | Cuentas de Google por letra (A, B, C), sin correos: la equivalencia vive en el inventario de SeguridadGeneral §3. Proyectos por su nombre; identificadores de facturación por sus últimos dígitos |
| Costo | Toda la columna «Línea base» está **pendiente**: aún no hay acceso de lectura otorgado a ninguna facturación (`docs/04`). Ninguna cifra de esta tabla es un costo |

| Servicio | Proveedor | Proyecto(s) que lo usan | Modalidad | Dueño técnico | Línea base mensual | Fuente (estado) |
|---|---|---|---|---|---|---|
| Plan de suscripción Claude (Max desde 2026-09-30; Pro el 29/09) | Anthropic | Todos (Claude Code en ~20 carpetas, 7 sesiones principales en paralelo) | Suscripción + créditos | Andres | En % de cuota, no en USD: `mediciones/claude/2026-09-linea-base.md` | `get_usage` (**activa**) |
| API / Console de Anthropic | Anthropic | (verificar si alguno usa clave de API) | Consumo | (verificar) | Pendiente | Console → Usage (pendiente de acceso) |
| Gemini (Flash-Lite 3.5 en los asistentes) | Google | NovuChat, ChatBotRAG y otros (verificar); SeguridadGeneral registra **tres claves de Gemini facturables** halladas sin restringir en 2026-08-30 | Consumo por token | NovuChat | Pendiente. NovuChat ya tiene su propio análisis de costos fijos y variables de Gemini (no leído aquí) | Export de facturación de la cuenta B; métricas por clave (pendiente) |
| Google Cloud / Firebase — cuenta A | Google | 14 proyectos: encuentrame.bo, PuntosNB (prod y staging), PRETSO, landings (hipatia, kepler, aab1), demob/snack-laestacion, ManejoQRSimple y otros | Consumo | Andres / cada proyecto | Pendiente | Export a BigQuery de la facturación (pendiente de acceso) |
| Google Cloud / Firebase — cuenta B | Google | NovuChat (admin dev y prod) | Consumo | NovuChat | Pendiente | Ídem |
| Google Cloud / Firebase — cuenta C | Google | 7 proyectos (incluye cuatro con nombre autogenerado que nadie revisa) | Consumo | (verificar) | Pendiente | Ídem |
| AWS | Amazon | SeguroLoTengoDemo (despliegue en Amplify, verificar); firma F2 (verificar) | Consumo | segurolotengo-demo | Pendiente | Cost Explorer (pendiente de acceso) |
| OCI — VM de n8n | Oracle | n8n autoalojado; WhatsApp-Modular (fase 0 en VM, verificar si comparte máquina) | Consumo | n8n-oci | Pendiente | Usage API (pendiente de acceso) |
| n8n (ejecuciones) | n8n (autoalojado) | NovuChat (flujos de los clientes) | Sin licencia; costo = VM + APIs que llama | NovuChat | Pendiente | API de n8n, lectura (pendiente) |
| WhatsApp Cloud API | Meta | WhatsApp-Modular (OTP de SeguroLoTengo), NovuChat (asistentes por cliente) | Consumo por mensaje y categoría | WhatsApp-Modular / NovuChat | Pendiente | WhatsApp Manager → Insights (pendiente) |
| GitHub | GitHub | Dos cuentas: Pro (7 repos) y General (14 repos, más este) | Suscripción (Pro) + GHAS en modo B | Andres | Pendiente | Facturación de cada cuenta (pendiente) |
| Dominios, correo, Lovable y otros SaaS | Varios | novuchat.site, dominios de PRETSO y SLT (verificar), diseño en Lovable (slt-diseno-lovable) | Suscripción | Andres | Pendiente | Facturas del correo del titular (Gmail, lectura; pendiente) |

### Hallazgos de costo ya visibles en el inventario (sin medir; son candidatos del Bloque 3)

Vienen de SeguridadGeneral y su decisión de borrado es de esa sesión, no de esta.

1. **Nueve recursos marcados «a borrar»** en GCP (DemoA, versiones descartadas de PRETSO, `pagosqrtrabajito`, `etf-investimento-sim`, `kepler-stem`, `snak-laestacion` y «My First Project»): dejan de facturar solo si tenían facturación asociada. No se sabe cuánto; hay que leer el export. Borrar exige confirmar con el dueño y respaldo previo (`docs/03` §2).
2. **Tres claves de Gemini sin restringir**: además de un riesgo de seguridad, una clave filtrada es gasto directo. La restricción la decide SeguridadGeneral.
3. **Cuatro proyectos de GCP con nombre autogenerado** creados por consolas: candidatos a proyecto huérfano.
4. **Este repositorio figura como `FinOpsEcosistema`** en el inventario de SeguridadGeneral (fila de la cuenta general); el repositorio real se llama `FinOps`. Corrección para esa sesión.
