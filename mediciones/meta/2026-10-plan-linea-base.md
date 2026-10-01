# Meta WhatsApp Cloud API — plan de línea base

| Versión | Fecha | Estado |
|---|---|---|
| 0.2 | 2026-10-01 | Primera línea base de septiembre obtenida vía WhatsApp-Modular; ya no hace falta un token propio de FinOps |

## Por qué este proveedor es distinto

**Desde el 1 de octubre de 2026 los mensajes de servicio (las respuestas del asistente dentro de la ventana de 24 h) pasan a cobrarse.** Hasta septiembre eran gratis. NovuChat ya lo modeló (`NovuChat/Analisis/14-costo-por-conversacion-y-precios.md`, leído en solo lectura): tarifa de «Rest of Latin America» (Bolivia incluida) de 0,0113 USD por mensaje de servicio o de utilidad y 0,0740 por mensaje de marketing; **1.000 mensajes de servicio gratis por número y mes**; los mensajes del cliente final no se cobran. Consecuencia: **no existe línea base previa de costo**. Septiembre ≈ 0 por diseño; **octubre es el primer mes medible**, y es la comparación que NovuChat marca como «la conciliación de fondo» (punto 9 de su §10bis).

## Qué se mide y con qué

| Dato | Fuente | Cómo |
|---|---|---|
| Cargo aproximado y volumen por categoría, tipo de precio y país, por cuenta (WABA) | `pricing_analytics` de la Graph API (`/<WABA>?fields=pricing_analytics…`; dimensiones y métricas según la documentación oficial de Meta, consultada el 2026-10-01) | `scripts/meta/pricing_analytics.py --mes AAAA-MM` |
| Cargo real facturado | Meta Business Suite → Facturación | Lectura manual mensual de Andres, para conciliar |
| Mensaje a mensaje (`billable`, `type`) | Webhook de estado, objeto `pricing` | Lo guarda o no la ingesta de NovuChat; se le consultó |

`COST` en `pricing_analytics` es un cargo **aproximado**: se concilia contra la factura. La estructura exacta de la respuesta y la versión vigente de la Graph API (por defecto `v23.0`) están por verificar con una respuesta real.

## Lo que ya está hecho (sin ninguna credencial)

- **Script de solo lectura**, con el token solo en la cabecera `Authorization` (nunca en la URL ni en pantalla) y los identificadores por sus últimos 4 dígitos; los datos crudos van a `datos/meta/` (ignorado por git).
- **`scripts/meta/guardar_token.sh`:** guarda el token en `datos/meta/token` (permiso 600) desde un prompt oculto; el valor no pasa por el chat.
- **10 pruebas** con respuestas simuladas, incluida la de que el token y el ID completo nunca se imprimen. El guardián de invariantes del proyecto, que analiza los scripts reales, ya detectó y obligó a corregir una ruta no literal en el primero.

## Línea base de septiembre 2026 (primera medición real)

Fuente: comando de solo lectura `npm run costos:meta` de WhatsApp-Modular (PR segurolotengopy/WhatsAppModular#130, pendiente de fusión), corrido el 2026-10-01 con el token de usuario de AAB1 **re-emitido ese día** (cubre las 11 WABA, vence el 2026-11-30). **Ningún token sale de ese proyecto**; a FinOps llegan solo agregados por mensaje. Cifras en USD.

| WABA | Paga | Mensajes en septiembre | Costo | Tipo de cifra |
|---|---|---|---|---|
| …2820 AAB1 (OTP de SeguroLoTengo) | Andres | 5 (3 de autenticación pagados, 2 de servicio gratis) | **0,0339** | **Real** (Meta) |
| …1573 Interseguros | Andres | 1 (servicio, gratis) | 0 | — |
| …7545 Clínica Platinum | Andres | 262 (servicio, gratis) | 0 | — |
| …1048 NovuChat | Andres | 94 (84 de servicio y 4 de utilidad gratis; 1 de utilidad pagado; 5 de servicio a Alemania sin tarifa) | 0,0113 | Estimado |
| …3951 Dr. Bellido | Andres | 214 (servicio, gratis) | 0 | — |
| …4125 NovuChat (Silvana) | **Silvana** | 29 (servicio, utilidad; 6 a EE. UU. sin tarifa) | 0 | — |
| **Total Andres** | | **598** | **0,0565** (real 0,0452; estimado 0,0113) | |
| Total Silvana | | 30 | 0 | |

Octubre, parcial al 1/10 a media mañana: 1 mensaje de autenticación en `…2820` (0,0113 real, una prueba de OTP) y 22 de servicio gratis. Octubre completo se pide el 1/11.

## Qué dice y qué no

- **El costo de Meta es hoy prácticamente cero: USD 0,06 en septiembre.** El volumen es de unos 600 mensajes al mes, casi todos de servicio. Con **1.000 mensajes de servicio gratis por línea y mes** (fuente secundaria; verificar), ninguna línea los alcanza. **No hay una palanca de ahorro de importancia en Meta con este volumen.** Lo único pagado es la autenticación (el OTP) y algún mensaje de utilidad.
- **La palanca de la categoría de plantilla** (utilidad recategorizada a marketing, 6,5 veces más cara) existe, pero hoy afecta a un mensaje al mes: **no se propone nada.** Cobrará sentido si el volumen de NovuChat crece; queda anotada.
- **Meta devuelve el costo real solo para las WABA de la empresa dueña de la app (`…2820`).** Para las otras cinco rechaza el costo (error #10) y deja pedir solo el volumen. Por eso cada cifra va rotulada «real» o «estimado» (volumen por tarifa de Bolivia, **por verificar con la tarjeta de tarifas del WhatsApp Manager**); un país sin tarifa verificada queda «sin tarifa» y no se inventa (Alemania y EE. UU. en este caso). **El cierre exacto de las otras cinco sigue siendo el CSV de Facturación de Meta**, que baja Andres una vez al mes.
- **Un error evitado:** la primera prueba de WhatsApp-Modular salió con 0 puntos porque pidió dimensiones sin `metric_types`; con ambos devuelve datos. El script de FinOps (`scripts/meta/pricing_analytics.py`) ya pide los dos.
- **`…8189` (huérfana, en dirhams, sin líneas):** sigue pendiente revisar su saldo y cerrarla.

## Cómo se mide de aquí en adelante

1. **Primer día hábil de cada mes:** pedir a la sesión de WhatsApp-Modular `npm run costos:meta --mes AAAA-MM` y recibir los agregados por mensaje.
2. **Contraste:** el CSV de Facturación de Meta que baja Andres, para las cinco WABA sin costo real.
3. **El script propio de FinOps** (`scripts/meta/pricing_analytics.py`) queda como respaldo: tendría la misma limitación (costo real solo en la WABA de la app) y exigiría un token propio, que se evita.

## Límites y riesgos

- **Cuántas WABA y en qué portafolios:** desconocido; se pidió el inventario a WhatsApp-Modular y a NovuChat. Sin él no se puede decir si un solo token alcanza a todas.
- **Mensajes de marketing y los de autenticación** (OTP de SeguroLoTengo) también cuestan: la categoría de autenticación va aparte; se medirán por separado.
- **No usar los tokens de otros proyectos:** son de cada sesión y tienen más alcance del necesario (`docs/03` §1 y principio de mínimo privilegio).
- **Costo de consultar:** la Graph API no cobra por llamada; hay límites de tasa (verificar).

## Siguiente paso
Con el token y la lista de WABA: `python3 scripts/meta/pricing_analytics.py --mes 2026-10` el primer día hábil de noviembre, y conciliar contra la factura de Meta y contra la estimación de NovuChat.
