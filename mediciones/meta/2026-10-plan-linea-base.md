# Meta WhatsApp Cloud API — plan de línea base

| Versión | Fecha | Estado |
|---|---|---|
| 0.1 | 2026-10-01 | Plan y herramienta listos; falta el token de solo lectura y la lista de cuentas (WABA) |

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

## Qué hace falta de Andres (pasos que solo una persona puede dar en Meta)

1. En **Meta Business Suite → Configuración del negocio → Usuarios → Usuarios del sistema**: crear un usuario de sistema `finops-lectura` con rol de empleado (no administrador).
2. **Asignarle las cuentas de WhatsApp (WABA)** con acceso parcial de solo lectura, una por una. Hay que hacerlo en **cada portafolio** que tenga cuentas.
3. **Generar un token** con el permiso `whatsapp_business_management` (verificar si la analítica de precios exige también `whatsapp_business_messaging`). Preferir **caducidad de 60 días** a «nunca», con rotación.
4. Guardar el token con `scripts/meta/guardar_token.sh` (Claude lo lanza en una pestaña de su terminal y Andres lo pega en el prompt oculto).
5. Pasar la lista de IDs de WABA (por mensaje, no en archivos versionados) para `datos/meta/wabas.txt`.

## Lo que respondió NovuChat (2026-10-01, solo lectura de su respuesta)

- **El objeto `pricing` del webhook de estado NO se guarda:** NovuChat descarta los acuses de estado. La conciliación mensaje a mensaje no es posible con lo que se guarda hoy; **`pricing_analytics` es la fuente real.**
- **Cuentas (WABA), sin cifras exactas:** una compartida con WhatsApp-Modular (la del Demo A, con las apps `NovuChat-Demo-A` y `Demo SeguroLo Tengo`), una propia `NovuChat` (chat interno y Demo B), **una de Bellido en el portafolio de su doctor** (el doctor aún no aceptó ser administrador; hay una app y una WABA huérfanas) y una de demo (Platinum). Los alias y el número exacto viven en un archivo local que ninguna sesión lee; los tiene la sesión de cartera o Andres.
- **Meta no ofrece alerta de gasto para Cloud API** (verificado por Andres en pantalla el 30/09). Por eso `pricing_analytics` es el **único** control de gasto disponible y justifica la revisión mensual.
- **Riesgo de cobertura:** la WABA de Bellido está en el portafolio de otra persona. Un usuario de sistema creado en el portafolio de Andres **no la verá** salvo que el doctor comparta el acceso. Se anota para decidirlo con el contrato de Bellido («quién paga Meta», pendiente de su cliente).
- **Estimación por inquilino:** solo existe la tarifa de referencia (0,0113 USD por mensaje saliente de Bolivia desde el 01/10); la de cartera, con bolsas de prueba de 20 mensajes para Bellido y 100 para Platinum, no está escrita.

## Límites y riesgos

- **Cuántas WABA y en qué portafolios:** desconocido; se pidió el inventario a WhatsApp-Modular y a NovuChat. Sin él no se puede decir si un solo token alcanza a todas.
- **Mensajes de marketing y los de autenticación** (OTP de SeguroLoTengo) también cuestan: la categoría de autenticación va aparte; se medirán por separado.
- **No usar los tokens de otros proyectos:** son de cada sesión y tienen más alcance del necesario (`docs/03` §1 y principio de mínimo privilegio).
- **Costo de consultar:** la Graph API no cobra por llamada; hay límites de tasa (verificar).

## Siguiente paso
Con el token y la lista de WABA: `python3 scripts/meta/pricing_analytics.py --mes 2026-10` el primer día hábil de noviembre, y conciliar contra la factura de Meta y contra la estimación de NovuChat.
