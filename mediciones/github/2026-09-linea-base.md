# GitHub — línea base de costos (septiembre 2026)

| Versión | Fecha | Estado |
|---|---|---|
| 0.2 | 2026-10-01 | Estimación de minutos + **verificación con las pantallas de Facturación que envió Andres el 2026-10-01** |

## Cuentas y repositorios

| Cuenta | Repos públicos | Repos privados |
|---|---|---|
| `AndresAlberdi` (general) | 17 | `SeguridadGeneral` (activo), `Gemini-CLI` (sin ejecuciones desde hace un año) |
| `segurolotengopy` (Pro, según el inventario de SeguridadGeneral) | 9 | `ProyectosGeneral`, `SeguroLoTengoDemo`, `WhatsAppModular` (los tres activos) |

**GitHub Actions es gratis en repositorios públicos con ejecutores estándar** (documentación oficial de GitHub, 2026-10-01). El gasto posible está solo en los 5 privados. Cuota incluida por mes en repositorios privados: **Free 2.000 minutos y 500 MB; Pro 3.000 minutos y 1 GB**; pasada la cuota, Linux de 2 núcleos cuesta **USD 0,006 por minuto** (https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions, 2026-10-01).

## Minutos de Actions en septiembre (estimados)

Método: duración de cada trabajo (`/actions/runs/{id}/jobs`), redondeada hacia arriba por trabajo. El endpoint oficial de tiempos devuelve ceros y no sirve. `scripts/github/minutos_actions.py` lo repite cada mes. Se descartan los trabajos de más de 6 horas, que no pueden existir (cuatro ejecuciones de Dependabot en `SeguroLoTengoDemo` figuraban con exactamente 24 horas: **5.761 minutos falsos**, que habrían dado un excedente fantasma de USD 34).

| Repositorio | Ejecuciones | CI y demás (min) | Dependabot (min) | Total (min) |
|---|---|---|---|---|
| `SeguridadGeneral` (cuenta general) | 98 | 189 | 0 | **189** (9 % de 2.000) |
| `ProyectosGeneral` | 57 | 398 | 27 | 425 |
| `SeguroLoTengoDemo` | 471 | 1.806 | 60 | 1.866 |
| `WhatsAppModular` | 573 | 546 | 121 | 667 |
| **`segurolotengopy` (Pro)** | 1.101 | **2.750** | 208 | **2.958 = 98,6 % de 3.000** |

## Qué dice y qué no

- **Excedente en septiembre: 0 minutos, USD 0,** pero por muy poco: **entre el 92 % y el 99 % de la cuota gratuita**. Cada 1.000 minutos de más cuestan USD 6.
- **Octubre probablemente la supere:** `SeguroLoTengoDemo` entrega el 1/10 y está en plena actividad. El costo esperado es de unos pocos dólares, no una cifra grande.
- **Riesgo operativo, mayor que el de costo:** si la cuenta tiene el límite de gasto de Actions en USD 0 (lo habitual por defecto), **al agotar la cuota los trabajos dejan de correr y el CI se bloquea.** Eso no se ve desde la API con el acceso actual.
- **Palancas revisadas, sin recomendación:** (a) CI duplicado (push más pull request en la misma rama): **no existe**; los tres repositorios ya disparan solo en PR y en `main`. (b) Ejecuciones canceladas: casi nulas (concurrencia ya usada). (c) Dependabot es el 7 % del total (208 min): agrupar actualizaciones ahorraría poco y **Dependabot es un control de seguridad** (`docs/03` §1): no se toca. **No hay ahorro de importancia en GitHub Actions hoy.**
- **Seguridad avanzada (GHAS):** los campos no aparecen en ningún repositorio privado, lo que indica que no está activada (verificar). Se cobra por usuario activo, por lo que conviene confirmarlo.
- **Costo fijo:** la suscripción del plan Pro de `segurolotengopy` y el plan real de `AndresAlberdi` no se pueden leer: los endpoints de facturación de GitHub exigen el permiso `user`, que los tokens actuales no tienen. Tarifa del plan Pro: verificar en la página de precios de GitHub.

## Verificado por Andres en Facturación (capturas del 2026-10-01)

| Dato | `segurolotengopy` | `AndresAlberdi` |
|---|---|---|
| Plan | **GitHub Pro, USD 4,00 al mes** | GitHub Free, USD 0; Copilot Free, USD 0 |
| Uso medido bruto, octubre al 1/10 | USD 13,56 | USD 22,41 |
| Descuentos por uso incluido y repositorios públicos | USD 12,64 (el resto lo cubre la cuota de Actions) | USD 22,41 (todo) |
| **Facturable de Actions** | **USD 0** | **USD 0** |
| Minutos de Actions incluidos usados en octubre (al 1/10) | **65 de 3.000** | — |
| Almacenamiento de Actions | 0 GB de 2 GB | — |
| **Presupuestos de Actions** | **USD 0 con «detener el uso» activado** | **USD 0 con «detener el uso» activado** |
| Pagos pendientes | Ninguno | Ninguno |

- **El costo fijo de GitHub es USD 4,00 al mes** (el plan Pro de `segurolotengopy`). Las cifras brutas (en septiembre el gráfico llegó a ~USD 138 en `segurolotengopy` y ~USD 60 en `AndresAlberdi`) **no son costo**: son uso medido que los descuentos cubren, sobre todo los repositorios públicos, que son gratis.
- **El riesgo operativo quedó confirmado.** Ambas cuentas tienen el presupuesto de Actions en USD 0 con «detener el uso»: **al agotar los 3.000 minutos incluidos, los trabajos de los repositorios privados dejan de correr y el CI se bloquea.** En septiembre `segurolotengopy` usó ~2.958 minutos (estimado), a 1,4 % del tope; octubre arrancó con 65 minutos al 1/10, pero `SeguroLoTengoDemo` entrega ese día.
- **Recomendación (decide Andres, es un ajuste de Facturación suyo):** subir el presupuesto de **Actions de `segurolotengopy`** de USD 0 a un tope pequeño, por ejemplo **USD 10** (unos 1.600 minutos extra a USD 0,006), manteniendo «detener el uso». El costo máximo queda acotado y se evita el bloqueo. `AndresAlberdi` usa el 9 % de su cuota: no hace falta.
- **Pendiente de verificación:** los minutos exactos de septiembre. En Facturación → **Uso** → período «Último mes», filtro por producto «Actions», figura la cantidad de minutos; contrastarla con la estimación de ~2.958.

## Qué falta (lo puede ver solo Andres)

_(Los puntos 1 y 3 de abajo quedaron respondidos arriba; queda el cuadro de minutos de septiembre.)_

En **cada cuenta**, Configuración → **Facturación y planes → Uso**: anotar (1) el plan, (2) los minutos de Actions usados en septiembre y su costo, (3) el **límite de gasto / presupuesto de Actions** (si es USD 0, subirlo a un tope pequeño evita que el CI se detenga). Con eso se cierra la estimación. Alternativa sin pantallas: un token con el permiso mínimo de facturación, que no se pide ahora.

## Costo de la recolección
Unas 3.500 solicitudes a la API de GitHub, sin costo; dentro del límite de tasa.

## Siguiente paso
Repetir el primer día hábil de cada mes con `python3 scripts/github/minutos_actions.py --mes AAAA-MM --cuota 3000` (Pro) o `2000` (Free), y marcar anomalía si un mes supera en más de 20 % la media de los tres anteriores.

## Lectura del 2026-10-04 (pantalla de Facturación → Uso de `segurolotengopy`)

| Mes | Bruto | Facturado | Minutos de Actions |
|---|---|---|---|
| Agosto | USD 17,70 | USD 0 | — |
| Septiembre | USD 138,93 | USD 0 | — |
| Octubre (1 al 4) | USD 62,89 | USD 0 | 10.478 (Linux) |

El bruto incluye los repositorios públicos (gratuitos) y por eso es mucho mayor que los 2.958 minutos estimados para los privados; lo **facturado** es cero. No se pudo separar cuántos minutos son de repositorios privados (haría falta el informe «Get usage report», por repositorio). **El presupuesto de Actions de `segurolotengopy` se subió de USD 0 a USD 10 el 2026-10-02** por orden de Andres (con «detener el uso» y alertas activas): la recomendación de arriba quedó cumplida.
