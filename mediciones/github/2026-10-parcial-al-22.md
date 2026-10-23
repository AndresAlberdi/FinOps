# GitHub Actions — estimación de minutos de octubre (1 al 22)

| Versión | Fecha de consulta (UTC) | Estado |
|---|---|---|
| 0.1 | 2026-10-23 (06:47 a 07:xx UTC, aprox.) | **ESTIMACIÓN** [estimación]. La cifra exacta la ve Andres en Facturación y planes → Uso de cada cuenta |

**Período:** 2026-10-01 a 2026-10-22 (día de corte pedido: 22 de octubre). **Salvedad:** el script `scripts/github/minutos_actions.py` consulta el mes completo (`created=2026-10-01..2026-10-31`) y no admite fecha de corte; la cifra incluye las ejecuciones creadas hasta el momento de la consulta (23 de octubre UTC, parcial). Hueco declarado, no corregido.
**Fuente:** API REST de GitHub (`gh api`, solo GET) mediante `scripts/github/minutos_actions.py` (sin modificar). Cuota de 3.000 min para `segurolotengopy` (Pro). Datos crudos y salida en `datos/github/` (no versionados): `datos/github/repos.txt` y `datos/github/salida-2026-10-al-22.txt`.
**Reglas de cálculo del script:** minutos por trabajo redondeados hacia arriba; trabajos de más de 6 horas descartados como artefacto; repositorios públicos no facturan y no se consultaron.

## 1. Totales por dueño (repositorios privados)

| Dueño | Repositorios privados consultados | Minutos facturables estimados [estimación] | % de la cuota |
|---|---|---|---|
| `segurolotengopy` (Pro, 3.000 min compartidos) | 3 (`SeguroLoTengoDemo`, `WhatsAppModular`, `ProyectosGeneral`) | **3.623** (CI y demás 3.537 más Dependabot 86, ver detalle) | **120,8 %** |
| `AndresAlberdi` (Free, 2.000 min) | 4 (`Gemini-CLI`, `Mejora-Continua-y-Control`, `SeguridadGeneral`, `Sistema_Aprendizaje`) | **0** | 0 % |
| `aab1-website` (organización, plan propio) | 2 (`FacturadorSIAT`, `AAB1empresaAI`) | **0** | no consume la cuota personal |

Nota de cálculo: el script informa dos cifras por repositorio (sin Dependabot y con Dependabot). El total de referencia es el de la columna «con Dependabot» (3.623); sin Dependabot la suma es 3.537.

### Detalle por repositorio (`segurolotengopy`)

| Repositorio | Ejecuciones (API) | Minutos sin Dependabot | Minutos con Dependabot |
|---|---|---|---|
| `SeguroLoTengoDemo` (privado) | 1.000 (**tope posible, ver §4**) | 3.103 | 3.103 |
| `WhatsAppModular` (privado) | 289 | 340 | 402 |
| `ProyectosGeneral` (privado) | 26 | 94 | 118 |
| **Total** | **1.315** | **3.537** | **3.623** |

[estimación] Total de referencia de la salida del script: 3.623 min.

## 2. Comparación con el parcial al 16 y ritmo

| | Octubre 1 al 16 (parcial anterior) | Octubre 1 al 22 (esta medición) |
|---|---|---|
| `segurolotengopy`, minutos [estimación] | 2.054 | **3.623** |
| % de la cuota de 3.000 | 68,5 % | 120,8 % |
| Incremento desde el 16 | — | +1.569 min en 6 días (~260 min/día [estimación]) |

El ritmo entre el 16 y el 22 es mayor que el de los días 10 al 15 (210 min/día en la medición anterior). Con este ritmo, la cuota gratuita ya está excedida desde la semana actual.

## 3. Presupuesto de USD 10 de Actions

- Excedente sobre la cuota al corte de la consulta: 3.623 − 3.000 = **623 min** [estimación].
- Costo del excedente con la tarifa de referencia de la línea base (USD 0,006 por minuto; fuente GitHub consultada el 2026-10-01, **verificar** en la página oficial de precios de Actions antes de decidir): **≈ USD 3,74** [estimación].
- Margen restante del presupuesto de USD 10: ≈ USD 6,26, es decir, **≈ 1.043 min** [estimación].
- Con el ritmo observado (~260 min/día) el presupuesto se agotaría hacia el **26 de octubre** [estimación]. Con el ritmo medio de la semana, hacia finales de octubre. Al agotarse, los trabajos de los repositorios privados dejan de correr: **riesgo operativo para SeguroLoTengoDemo y WhatsAppModular**.

## 4. Huecos, márgenes y contraste pendiente

1. **Corte al 22 no exacto:** el script consulta el mes completo; la cifra llega hasta el 23 de octubre UTC (parcial). Para el corte exacto hace falta ajustar el rango de fechas del script (queda como mejora, sin modificar aquí).
2. **Posible tope de 1.000 ejecuciones en `SeguroLoTengoDemo`:** la API devolvió exactamente 1.000 ejecuciones, el mismo tope observado en `NovuChat` en el parcial anterior. Si es un límite de paginación y no el total real, los minutos de este repositorio están **subestimados** y el excedente real es mayor. **Verificar** con la pantalla de Uso de Actions de la cuenta (cifra exacta). [estimación]
3. **Margen:** no medido. Es una estimación por trabajo, sin reintentos (la API devuelve solo el último intento) y puede diferir de la facturación real.
4. **Contraste pendiente:** la captura de Facturación del día 1 mostró 65 min incluidos, frente a una estimación de 182 min para ese día (contraste ya registrado en el parcial del 16). La diferencia sigue sin explicar.
5. **Repositorios públicos** (no facturan) no se consultaron en esta medición.
6. **Cuotas de las organizaciones:** la organización `aab1-website` no tuvo ejecuciones privadas en la ventana consultada (0 min). Plan y cuota propios no verificados (verificar).

## 5. Pendiente para Andres

- Leer en Facturación y planes → Uso de `segurolotengopy` los minutos de Actions incluidos usados hasta hoy y anotarlos aquí como contraste. Con esa cifra se confirma si el presupuesto de USD 10 alcanza hasta fin de mes.
- Decidir si se revisa el consumo de `SeguroLoTengoDemo` (ramas de pruebas y builds) antes de que se agote el presupuesto. Ningún ajuste se ejecuta sin su autorización.

## 6. Costo de la recolección

USD 0. Solo solicitudes GET a la API de GitHub; del orden de 1.500 solicitudes (estimación), dentro del límite de tasa. Ningún servicio de pago. Identidades verificadas antes de consultar: `AndresAlberdi` (config `gh-andres`) y `segurolotengopy` (config por defecto).
