# GitHub Actions — estimación de minutos de octubre (1 al 16)

| Versión | Fecha de consulta (UTC) | Estado |
|---|---|---|
| 0.1 | 2026-10-16 (11:53 UTC) | **ESTIMACIÓN**. La cifra exacta la ve Andres en Facturación y planes → Uso de cada cuenta |

**Período:** 2026-10-01 a 2026-10-16 (día de corte: 16 de octubre, parcial; fechas en UTC).
**Fuente:** API REST de GitHub (`gh api`, solo GET) sobre `actions/runs` y `actions/runs/{id}/jobs`. Método heredado de `scripts/github/minutos_actions.py`, ampliado con multiplicadores por sistema operativo. Datos crudos en `datos/github/` (no versionados).
**Reglas de cálculo:** minutos por trabajo redondeados hacia arriba; Linux x1, Windows x2, macOS x10. Los repositorios públicos y los ejecutores self-hosted no facturan. Los trabajos de más de 6 horas se descartan como artefacto.

## 1. Totales por dueño

| Dueño | Plan y cuota incluida | Ejecuciones (API) | Minutos facturables estimados | % de la cuota |
|---|---|---|---|---|
| `segurolotengopy` | Pro, 3.000 min compartidos | 2.897 (767 privadas; el resto, públicas, no factura) | **2.054** | **68,5 %** |
| `AndresAlberdi` (privados) | Free, 2.000 min | 1.089 (incluye públicas, que no facturan) | **142** | 7,1 % |
| `aab1-website` (organización) | Team, cuota propia (verificar) | 134 | **474** | 15,8 % de 3.000 (verificar) |
| `segurolotengo-diseno` (organización) | Free, cuota propia (verificar) | 0 | **0** | 0 % |

La organización `aab1-website` factura a su propio plan: sus minutos no consumen la cuota de la cuenta personal.

### Cuenta `segurolotengopy` por tipo y por repositorio

| Concepto | Minutos |
|---|---|
| CI en Linux | 1.990 |
| Dependabot (trabajos reales) | 64 |
| **Total facturable estimado** | **2.054** |
| Repositorio `SeguroLoTengoDemo` (privado, 556 ejecuciones) | 1.683 |
| Repositorio `WhatsAppModular` (privado, 192 ejecuciones) | 247 |
| Repositorio `ProyectosGeneral` (privado, 19 ejecuciones) | 124 |
| Trabajos descartados (>6 h, Dependabot cancelado, 1.440 min cada uno, 7 casos) | 10.083 (no se suman) |

En octubre no aparecieron trabajos en Windows ni macOS ni ejecutores de mayor tamaño: todos los trabajos usan `ubuntu-latest` o `dependabot`.

## 2. Comparación con septiembre

| | Septiembre (línea base) | Octubre 1 al 16 |
|---|---|---|
| `segurolotengopy`, minutos | 2.958 (98,6 %) | 2.054 (68,5 %) |
| Ritmo medio por día | 98,6 min/día (30 días) | 128,4 min/día (16 días) |
| Ritmo de los días completos 10 al 15 | — | 209,7 min/día |

El ritmo del período es mayor que el de septiembre. Los días 10 al 15 concentraron más de la mitad del consumo (1.258 de 2.054 min).

### Minutos diarios de `segurolotengopy` (UTC, por fecha de creación de la ejecución)

| Día | 01 | 02 | 03 | 05 | 08 | 09 | 10 | 11 | 12 | 13 | 14 | 15 | 16 (parcial) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Minutos | 182 | 70 | 83 | 98 | 172 | 117 | 105 | 233 | 493 | 268 | 119 | 40 | 74 |

(Los días 4, 6 y 7 no tuvieron minutos facturables.)

## 3. Escenarios de cierre de octubre (no son estimaciones medidas)

La cuota gratuita de `segurolotengopy` es de 3.000 min. El presupuesto de Actions de USD 10, con «detener el uso», cubre 1.666 minutos por encima de la cuota (USD 10 ÷ USD 0,006 por minuto; tarifa de la línea base, con fuente GitHub del 2026-10-01).

| Escenario (16 días restantes sin cambios) | Minutos al 31/10 | % de la cuota | Excedente | Costo estimado |
|---|---|---|---|---|
| Ritmo de septiembre (99 min/día) | ~3.530 | 118 % | ~530 min | ~USD 3 |
| Ritmo medio 1 al 16 (128 min/día) | ~3.980 | 133 % | ~980 min | ~USD 6 |
| Ritmo de los días 10 al 15 (210 min/día) | ~5.200 | 173 % | ~2.200 min | ~USD 13 |

- Con el ritmo medio del período, el presupuesto de USD 10 se agotaría hacia el **5 de noviembre**.
- Con el ritmo de los días 10 al 15, se agotaría hacia el **29 de octubre**. Al agotarse, los trabajos de los repositorios privados dejan de correr (riesgo operativo ya descrito en la línea base).

## 4. Huecos, márgenes y contraste pendiente

1. **Margen:** no medido. Es una estimación por trabajo, sin reintentos de ejecución (la API devuelve solo el último intento), y puede diferir de la facturación real.
2. **Contraste con la lectura del 1 de octubre:** la captura de Facturación de ese día mostró **65 min** de Actions incluidos usados en `segurolotengopy`. La estimación para el día 1 (UTC) es de **182 min**. No concilian; la captura se tomó en hora desconocida del día 1 y la diferencia de zona horaria (UTC frente a Bolivia) no alcanza a explicarla. Es la razón principal para contrastar con la pantalla de Uso antes de decidir.
3. **Repositorio público `NovuChat`:** la API informa 1.595 ejecuciones, pero el listado paginado devolvió 1.000 (tope de la consulta). No factura, así que no afecta la estimación.
4. **Ejecuciones añadidas después de la primera consulta:** 4 en `SeguroLoTengoDemo` y 4 en `WhatsAppModular`, incorporadas en la pasada de agregación.
5. **Ejecuciones en curso:** ninguna al consultar.
6. **Repositorio excluido:** uno de un tercero donde la cuenta `AndresAlberdi` figura como colaboradora (no factura a estas cuentas).
7. **Cuotas de las organizaciones:** los planes se leyeron de la API; las cuotas de 3.000 (Team) y 2.000 (Free) son referencias (verificar).

## 5. Pendiente para Andres

Leer en Facturación y planes → Uso de `segurolotengopy` los minutos de Actions incluidos usados hasta hoy, y anotarlos aquí como contraste. Con esa cifra se decide si el presupuesto de USD 10 basta hasta fin de mes. Ningún ajuste se ejecuta sin su autorización.

## 6. Costo de la recolección

USD 0. Se hicieron del orden de 1.300 solicitudes GET a la API de GitHub, dentro del límite de tasa. Ningún servicio de pago.

## 7. Observación de configuración (sin cambios)

La configuración por defecto de `gh` (`~/.config/gh`) tiene activa la cuenta `segurolotengopy`, mientras que la sesión usa `GH_CONFIG_DIR` apuntando a la cuenta `AndresAlberdi`. Las consultas se hicieron con cada configuración explícita y verificando la identidad antes de consultar. No se cambió ninguna configuración ni se ejecutó `gh auth switch`.
