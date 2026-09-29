# 04 · Accesos de solo lectura

| Versión | Fecha | Estado |
|---|---|---|
| 0.1 | 2026-09-28 | Propuesta; cada acceso se otorga en el Bloque 1 con autorización del titular |

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
