# Google Cloud — línea base de la cuenta de facturación C (terminada en 5DBD7A)

| Versión | Fecha | Estado |
|---|---|---|
| 1.0 | 2026-10-04 | **Septiembre completo** (export con datos hasta el 2026-10-03). Sustituye a la v0.2 provisional |

Fuente: exportación de facturación a BigQuery (costo de uso estándar), dataset `US` multirregional del proyecto dedicado `finops-ecosistema-c-4831`. Costo bruto en USD; la cuenta no muestra créditos. Datos crudos en `datos/gcp/` (no versionado). Cuenta de Google de esta cuenta de facturación: la «C» del inventario de SeguridadGeneral. Verificado también con la pantalla de Facturación que envió Andres el 2026-10-04: gasto de los últimos 30 días, USD 25.

## Septiembre 2026

| Proyecto | Servicio | Costo bruto (USD) | Créditos | Neto |
|---|---|---|---|---|
| `novuchatdemo` | **Gemini API** | **24,91** | 0 | **24,91** |
| `gen-lang-client-…6525` (autogenerado, «Default Gemini Project») | — | 0,00 | — | 0,00 |
| `encuentramebo` | — | 0,00 | — | 0,00 |

Los datos de Gemini cubren 23 días de septiembre; los demás días no hubo uso facturable.

### De dónde salen los 24,91

| Tramo | USD | Qué es |
|---|---|---|
| 29 y 30 de septiembre | **21,74** | 11,30 el día 29 y 10,44 el día 30: las baterías de pruebas y el concurso de Bellido de NovuChat. Corrieron con la credencial de **producción** (`novuchatdemo`), no con la de pruebas |
| Resto (21 días con uso) | 3,17 | Unos 0,15 por día |

Por modelo (SKU de tokens): `gemini 3.5 flash-lite` 9,25 (el modelo en uso; 6,61 en esos dos días), **`gemini 3.5 flash` 9,19** (8,66 en esos dos días) y **`gemini 3.8 flash` 6,47** (todo el 30/09). Es decir: **los dos modelos no-lite, que NovuChat no usa en producción, explican 15,66 de los 24,91**, y solo se usaron en las pruebas.

## Lo que se corrige y lo que se cierra

- **Hipótesis refutada:** el export **no oculta** el consumo prepago de Gemini. Mostraba 24,91 USD para septiembre mientras la reconstrucción desde n8n daba 1,1 a 2,7: la diferencia son los flujos temporales de las baterías y del concurso, que n8n ya borró. La sospecha de la v0.2 («el consumo prepago podría no aparecer») queda **descartada**.
- **Error de la v0.1 (ya corregido en la v0.2) sigue retirado:** «Gemini se detuvo el 5/09» fue un artefacto de carga incompleta.
- **`novuchat-pruebas`** es el proyecto `gen-lang-client-…1744` y tiene la **facturación inhabilitada**: no puede facturar y por eso no figura en el export (verificado con la pantalla de Proyectos que envió Andres). `encuentramebo-1` también tiene la facturación inhabilitada.

## Octubre (parcial, 1 al 3)

0,21 USD (0,19; 0,01; 0,02 por día, en hora UTC). La consola de Facturación muestra USD 0,03 para el 1–4 de octubre porque agrupa por hora del Pacífico y parte del 1 de octubre UTC cae en el 30 de septiembre.

**El pronóstico de la consola (USD 169, +573 % frente a septiembre) no es gasto:** las barras diarias de USD 4,3 a 6,7 son el «Costo previsto» de Google. Su nivel inicial coincide con el promedio de los últimos cinco días, que incluye el 29 y el 30 de septiembre ((11,30 + 10,44 + 0,19 + 0,01 + 0,02) / 5 ≈ 4,4). Es una inferencia; el algoritmo de Google no está verificado aquí. Debe bajar cuando esos días salgan de su ventana.

## Qué dice y qué no

- **El gasto es de un solo proyecto, `novuchatdemo`, y de un solo servicio.** La cuenta C no tiene costo fijo.
- **La línea base «normal» sin las pruebas es de unos 3,17 USD al mes** (unos 0,15 por día de uso), cifra que depende de cuánto tráfico real tengan los clientes de NovuChat.
- **No hay tope duro:** el único límite es el saldo prepago de AI Studio. Decisiones pendientes de Andres: un presupuesto con alertas en esta cuenta y la recarga automática con límite mensual.
- **No hay serie histórica:** sin segundo ciclo ni media de tres meses no hay base para el umbral de anomalía del 20 %.
- **No verificado:** el saldo inicial y el uso de Google AI Studio (pantalla que solo ve Andres), para saber qué parte del prepago compró Andres el 30/09 (USD 5) frente a lo consumido.

## Costo de la recolección
Consultas de 17 a 160 KB, facturadas al mínimo de 10 MiB cada una, dentro del primer TiB gratuito al mes (https://cloud.google.com/bigquery/pricing, vía catálogo de precios, 2026-09-30). **USD 0,00.**
