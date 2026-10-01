# GitHub — línea base de costos (septiembre 2026)

| Versión | Fecha | Estado |
|---|---|---|
| 0.1 | 2026-10-01 | **Estimación** desde la API de Actions; el cierre exacto está en Facturación (ver «Qué falta») |

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

## Qué falta (lo puede ver solo Andres, en dos pantallas)

En **cada cuenta**, Configuración → **Facturación y planes → Uso**: anotar (1) el plan, (2) los minutos de Actions usados en septiembre y su costo, (3) el **límite de gasto / presupuesto de Actions** (si es USD 0, subirlo a un tope pequeño evita que el CI se detenga). Con eso se cierra la estimación. Alternativa sin pantallas: un token con el permiso mínimo de facturación, que no se pide ahora.

## Costo de la recolección
Unas 3.500 solicitudes a la API de GitHub, sin costo; dentro del límite de tasa.

## Siguiente paso
Repetir el primer día hábil de cada mes con `python3 scripts/github/minutos_actions.py --mes AAAA-MM --cuota 3000` (Pro) o `2000` (Free), y marcar anomalía si un mes supera en más de 20 % la media de los tres anteriores.
