# Vigilancia periódica de OCI en GitHub Actions (solo lectura)

| Versión | Fecha | Estado |
|---|---|---|
| 0.3 | 2026-11-07 | Incorpora las condiciones del guardián y del agente `seguridad` (ambos: aprobada con condiciones). Pendiente: OK de Andres para cada escritura |

## Objetivo
Avisar a Andres antes de que OCI cobre, sin depender de su laptop (política del 11/10/2026). Costo: cero. No cambia ningún recurso de OCI.

## Hallazgo nuevo que cambia el umbral del bucket
La página oficial de Always Free (docs.oracle.com, «Always Free Resources», consultada 2026-11-07) da **20 GB** de Object Storage a una cuenta Always Free pura, pero **10 GB de Standard** a una cuenta de pago o con créditos. La línea base concluyó que la cuenta es Pay As You Go (verificar). Si es así, el tope gratuito del bucket es **10 GB, no 20**, y a 326 MiB diarios se alcanza en semanas. El costo de pasarse sigue siendo de centavos, pero el aviso debe ir a **8 GiB**. Confirmar el tipo de cuenta es el primer paso. Los límites de cómputo sí coinciden con la línea base: 1.500 OCPU-h y 9.000 GB-h al mes (misma fuente).

**Resolución (2026-11-07):** Andres indica que la cuenta es Always Free pura, así que el tope es 20 GB y el aviso queda en 15 GiB. Queda una discrepancia: la línea base vio límites de pago en la CLI (núcleos en 100, no 0). La primera ejecución lee los límites reales de la tenencia (`limits`, solo lectura) y, si resultan de pago, el umbral baja a 8 GiB sin más trámite.

## Qué se vigila y cuándo se avisa
| Medida | Aviso | Frecuencia | Fuente (solo lectura) |
|---|---|---|---|
| Costo del mes | > 0,00 USD | semanal | Usage API (con retraso; verificar) |
| Cómputo A1 | proyección del mes > 100 % de 1.500 OCPU-h / 9.000 GB-h | semanal | Usage API |
| Object Storage | ≥ 15 GiB (tope de 20 GB; Andres confirmó el 2026-11-07 que la cuenta es Always Free pura) | **diaria** | `approximateSize` del bucket |
| Memoria de la VM | p95 de 7 días < 21 % | **diaria** | Monitoring, `MemoryUtilization` |
| Disco de arranque | total > 150 GB | semanal | Core, lectura |

La regla de recuperación (CPU p95, red y memoria < 20 % durante 7 días en A1) está en la misma página de Oracle; **no dice si aplica a Pay As You Go (verificar con Oracle)**. Un aviso semanal llegaría tarde para una ventana de 7 días: por eso es diario.

## Dónde corre y por qué es gratis
Repositorio `AndresAlberdi/FinOps`, **público**: los ejecutores estándar de GitHub son gratuitos en repositorios públicos y no descuentan la cuota compartida (GitHub Docs, «About billing for GitHub Actions», 2026-11-07). Si el repositorio pasa a privado, se reevalúa. Disparadores: solo `schedule` y `workflow_dispatch`. Prohibido `pull_request_target` y cualquier disparador de forks.

## Autenticación sin llaves estáticas
Federación de identidad de carga de trabajo de OCI: el trabajo presenta el token OIDC de GitHub (`id-token: write`) y recibe un token de sesión corto, ligado a un usuario de servicio. Fuentes (2026-11-07): Oracle A-Team, «GitHub Actions + OCI: a guide to secure OIDC token exchange»; blog de Oracle sobre «Workload Identity Federation». Comando exacto de la CLI: **(verificar)** antes de escribir el script.

Condiciones de seguridad (del guardián):
1. **Política IAM mínima.** Solo `read usage-report`, `read metrics`, `read buckets` (basta para `approximateSize`) e `inspect` de instancias y volúmenes **limitado al compartimento**, no a la tenencia. **Sin `read objects`**: los objetos del bucket de respaldos contienen la base de datos de n8n.
2. **Mapeo estricto.** `sub` exacto `repo:AndresAlberdi/FinOps:ref:refs/heads/main`, más `aud` y emisor fijados; sin comodines. Entorno protegido de GitHub si es viable. Protección de rama en `main` y acciones fijadas por SHA.
3. **Sin fugas en el registro público.** Salida de la CLI a `/dev/null` o a un archivo no publicado; sin `set -x`; sin artefactos; `::add-mask::` para todo valor derivado. Los identificadores (OCID, espacio de nombres, bucket) van como secretos o variables del repositorio, nunca en el YAML. El resumen publica solo porcentajes.
4. Si la federación no fuera viable, alternativa peor: llave de API de solo lectura como secreto, rotada cada trimestre, solo con decisión de Andres.

Condiciones adicionales del agente `seguridad` (fuente: SeguridadGeneral, `01-seguridad/02-identidad-federada-oidc.md`, §2.3 y §3.2):
5. **Formato del `sub`.** Con un Environment de GitHub el `sub` pasa a `repo:AndresAlberdi/FinOps:environment:<nombre>` y la regla de `refs/heads/main` deja de coincidir. Se usa un Environment dedicado, limitado a `main`, con regla `eq` exacta y la variante inmutable con `repository_id`. No se copia el `sw "repo:…@"` del ejemplo del estándar (demasiado amplio).
6. **Secreto estático residual.** El `client_secret` de la aplicación confidencial va como secreto del Environment (no del repositorio) y se rota cada 90 días.
7. **`usage-report` solo se concede sobre la tenencia**: excepción justificada a la condición 1. No se otorga `usage-reports` (CSV de costos).
8. **Instancias y volúmenes:** `inspect instances` e `inspect volume-family` (incluye discos de arranque); ningún `read` sobre instancias.
9. **Token de sesión:** `::add-mask::` al token y la respuesta de `curl` nunca va al registro.
10. **Registro público:** solo «superado / no superado» por medida, sin montos en USD (invariante 6).
11. **Pipeline:** actualizar `.devsecops.yml` (hoy `proveedor: ninguno`; será el primer workflow del repositorio con credenciales de nube), comprobar que `.github/CODEOWNERS` cubre `.github/workflows/` y exigir aprobación para workflows de colaboradores externos.
12. **Por verificar:** nombre vigente del recurso de la Usage API en las políticas de Oracle y sintaxis del filtro de impersonación.

## Desviaciones del script respecto de este diseño (revisión de código, 2026-11-07)
- **Cómputo:** se mide la configuración de las instancias A1 (≤ 2 OCPU y 12 GB), no una proyección de horas de la Usage API: es determinista y cualquier exceso se cobra. Alcance: un compartimento, sin subcompartimentos.
- **Disco:** el tope gratuito de 200 GB suma discos de arranque y volúmenes de bloque; el aviso se activa por encima de 150 GB entre ambos.
- **Memoria:** se pide el p95 diario de 7 días (MQL no admite intervalo de 7d) de todas las series; el máximo de los p95 diarios aproxima el p95 de la ventana. A confirmar en la primera ejecución manual.
- **Costo:** por día, sumando solo montos positivos; `null` o respuesta ilegible es «sin medir», nunca OK.
- **Lectura de `limits`** (tipo real de cuenta): queda como paso manual de la primera ejecución, no del script.
- **Pendientes de seguridad:** `.devsecops.yml` sigue con `proveedor: ninguno` (condición 11), y el Environment `oci-lectura` debe crearse limitado a `main`. Identificadores como secretos del Environment, no como `vars`.

## Aviso y latido
- **Aviso:** el trabajo termina en error al superar un umbral; el correo de fallo de GitHub llega al titular (a quién llega exactamente un trabajo programado: **verificar** con una prueba). Canal distinto de n8n.
- **Latido (condición del guardián):** un resumen semanal no alerta por su ausencia, así que hace falta un monitor externo gratuito de latido (por ejemplo, un servicio de *heartbeat* con aviso por correo si el trabajo no le escribe en 36 h). El proveedor y su límite gratuito se verifican con fecha antes de elegirlo; hasta entonces, revisión manual de la última ejecución en cada cierre mensual. Los trabajos programados se desactivan tras 60 días sin actividad del repositorio **(verificar)**.

## Prueba de no regresión y reversión
- Primera ejecución a mano: las cifras deben coincidir con la medición de la CLI dentro de ±2 %.
- Forzar un fallo con un umbral artificial y confirmar que el correo llega.
- Reversión: desactivar el workflow y eliminar el usuario de servicio, su política y la confianza en OCI.

## Qué hace Andres (lo único que exige a una persona)
1. Confirmar el tipo de cuenta de OCI (Pay As You Go o Always Free) o renovar la sesión de la CLI para que Claude lo lea.
2. Crear en OCI el usuario de servicio, la política y la confianza (Claude le entrega los valores exactos).
3. Autorizar el PR con el workflow.

## Lo que no se construye
- Alertas por WhatsApp o n8n (comparten falla con lo vigilado).
- Limpieza de la VM o borrado de respaldos: son decisión de sus dueños (ver línea base).
