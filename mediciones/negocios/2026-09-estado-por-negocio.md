# Estado de costos por negocio — septiembre 2026 (provisional)

| Versión | Fecha | Estado |
|---|---|---|
| 0.1 | 2026-10-02 | **PROVISIONAL.** Primer corte por negocio con el mapa de `docs/06-costos-por-negocio.md` v0.3. Google incompleto (ver §1); el cierre de septiembre se rehace a partir del 2026-10-06 |

Cifras en USD, agregadas; cuentas por sus últimos 4 caracteres; datos crudos en `datos/` (no versionado). «**Medido**» = lo informa el proveedor por proyecto, cuenta, WABA o repositorio. «**Asignado**» = reparto de un costo compartido con una regla de `docs/06` §4, **todavía por aprobar**; no cuenta como medido.

## 1. Cobertura de los datos (qué tan completo es este corte)

| Fuente | Llega hasta | Estado |
|---|---|---|
| Google, cuenta principal (…3EC8) | 2026-09-21 | Incompleto: llenado inicial en curso |
| Google, cuenta C | 2026-09-27 | Incompleto: llenado inicial en curso |
| Google, cuentas …5B3F (PRETSO) y …44F7 (Hipatia producción y landing) | — | **Sin medición:** no se exportan hoy (`docs/06` §3, hallazgo 2) |
| AWS (…8663) | 2026-09-30 | Completo |
| Meta (WABA) | 2026-09-30 | Completo (vía `costos:meta` de WhatsApp-Modular); costo real solo en la WABA …2820 |
| GitHub Actions | 2026-09-30 | Completo (estimado por trabajos) |
| OCI | 2026-09-30 | Completo (USD 0) |
| Claude (cuota) | — | No se corta por negocio (§4) |

## 2. Resumen por negocio

| Negocio | Directo medido (bruto) | Créditos de Google | Directo neto | Asignado (regla por aprobar) | Cobertura |
|---|---|---|---|---|---|
| NovuChat | **6,33** (Google 6,32; Meta 0,01 estimado) | −3,51 | **2,82** | — | Google parcial |
| SeguroLoTengo | **4,99** (AWS 4,96; Meta OTP 0,03) | — | **4,99** | GitHub Pro 2,00 | Completa |
| AAB1 / WhatsApp-Modular | **0,06** (Google) | −0,06 | **0,00** | GitHub Pro 2,00 | Google parcial |
| Hipatia | **0,03** (solo `puntosnb`) | −0,03 | **0,00** | — | **Producción sin medir** |
| PRETSO | **sin medición** (cuenta …5B3F no exportada) | — | — | — | Sin dato |
| Encuéntrame.BO | **0,00** (0,0033 bruto) | −0,00 | **0,00** | — | Google parcial |
| ManejoQRSimple | **0,00** (sin facturación) | — | **0,00** | — | Integración con Banco Económico sin medir |
| Comunes | **0,00** (Actions dentro de la cuota; OCI 0) | — | **0,00** | — | Completa, salvo Claude |
| **Total medido** | **11,41** | **−3,60** | **7,81** | 4,00 | |

Los créditos de Google solo existen en la cuenta principal: la cuenta C (Gemini) no muestra créditos en el export. Si esos créditos vencen, el costo de esa cuenta pasa del neto al bruto.

## 3. Detalle por negocio

### NovuChat
| Proveedor | Concepto | Bruto | Créditos | Neto | Tipo |
|---|---|---|---|---|---|
| Google (principal, hasta el 21/09) | `novuchat-demo`: Cloud Run Functions 2,60; Secret Manager 0,43; Artifact Registry 0,00 | 3,03 | −3,03 | 0,00 | Medido, parcial |
| Google (principal, hasta el 21/09) | `novuchat-site`: Vertex AI 0,38; Secret Manager 0,07; Cloud Run Functions 0,02 | 0,48 | −0,48 | 0,00 | Medido, parcial |
| Google (principal) | `novuchatstaging` | 0,00 | — | 0,00 | Medido |
| Google (cuenta C, hasta el 27/09) | `novuchatdemo`: Gemini API | 2,81 | 0,00 | **2,81** | Medido, parcial; sin créditos visibles |
| Meta | WABA …1048 (NovuChat), …3951 (Bellido), …7545 (Platinum), …4125 (Silvana, «paga Silvana»), …8154 (prueba): 0,0113 estimado de la …1048; el resto, servicio gratis | 0,01 | — | 0,01 | Estimado |
| OCI / n8n | Cuota gratuita compartida con WhatsApp-Modular | 0,00 | — | 0,00 | Medido |

**Observaciones:**
- **El consumo de Gemini es el único gasto neto relevante y todavía no está completo:** la cuenta C llega al 27/09 y no incluye el crédito prepago de AI Studio si este se descuenta por fuera del export (a verificar el 06/10 con el saldo que solo ve Andres). El `novuchat-pruebas` de las baterías no figura en ninguna exportación.
- **El «fijo de plataforma ≈ USD 22 al mes» que estima NovuChat no se ve en el export:** el gasto bruto de Google de NovuChat **sin Gemini** es 3,51 hasta el 21/09 (unos 5 al mes si se extrapola de forma lineal, solo como orden de magnitud) y no aparece el servicio «Cloud Run» con instancia mínima. Puede deberse a que producción aún no está desplegada o a datos incompletos: **verificar con NovuChat al cierre del 06/10**, antes de usar la cifra de 22 en cualquier decisión.

### SeguroLoTengo
| Proveedor | Concepto | USD | Tipo |
|---|---|---|---|
| AWS (…8663) | Amplify 4,17; Secrets Manager 0,57; Rekognition 0,16; DynamoDB 0,03; Transfer Family 0,03 | 4,96 | Medido |
| Meta | OTP: 3 mensajes de autenticación de la WABA …2820 (cargo entre unidades, `docs/06` §3 hallazgo 7) | 0,03 | Medido (real) |
| Meta | WABA de Interseguros (…1573): 1 mensaje de servicio, gratis (dueño por confirmar) | 0,00 | Medido |
| GitHub | `SeguroLoTengoDemo`: 1.866 minutos de Actions (62 % de la cuota de 3.000 de la cuenta); dentro de la cuota | 0,00 | Estimado |
| GitHub | Plan Pro de `segurolotengopy` (USD 4,00 al mes), parte de SeguroLoTengo | 2,00 | Asignado |
| Google | Ninguno | 0,00 | — |

**Observación:** AWS Transfer Family ya costó 0,03 y se factura por hora; encendido todo el mes costaría mucho más. No existe alerta específica sobre ese servicio (el presupuesto de USD 50 al mes está por encima del gasto real y no lo distingue).

### AAB1 / WhatsApp-Modular
| Proveedor | Concepto | Bruto | Créditos | Neto | Tipo |
|---|---|---|---|---|---|
| Google (principal, hasta el 21/09) | `whatsappmodular` (Secret Manager 0,04) y `aab1-landing` (0,02) | 0,06 | −0,06 | 0,00 | Medido, parcial |
| Meta | Costo del OTP de la WABA …2820: se carga a SeguroLoTengo | 0,00 | — | 0,00 | Cargo entre unidades |
| GitHub | `WhatsAppModular`: 667 minutos de Actions (22 % de la cuota) | 0,00 | — | 0,00 | Estimado |
| GitHub | Plan Pro, parte de la unidad | 2,00 | — | 2,00 | Asignado |
| OCI | Parte de la cuota gratuita de la VM con n8n | 0,00 | — | 0,00 | Medido |

### Hipatia
| Proveedor | Concepto | Bruto | Créditos | Neto | Tipo |
|---|---|---|---|---|---|
| Google (principal, hasta el 21/09) | `puntosnb` (pruebas y pilotos): Cloud Run Functions 0,03 | 0,03 | −0,03 | 0,00 | Medido, parcial |
| Google (…44F7) | `hipatia-puntos` (producción) y `hipatia-landing-page` | — | — | — | **Sin medición** |
| Dominio | `hipatiabo.com` | — | — | — | Desconocido |

**Observación:** el plan Blaze exige Cloud Functions; con 22 funciones por proyecto el costo real de producción puede ser mayor que el de pruebas y hoy no se ve.

### PRETSO
Sin medición: sus dos proyectos facturan por la cuenta …5B3F, que no se exporta. Según su sesión el costo en la nube es de centavos (Firestore con 563 documentos, sin funciones, sin máquinas) y `pretso-database`, el sitio en uso, no tiene presupuesto verificado. Lo primero que hay que hacer visible por el contrato de octubre.

### Encuéntrame.BO y ManejoQRSimple
Sin facturación activa en Google; costo del mes: 0,0033 (Cloud Run Functions de `encuentramebo-1`, cubierto por créditos). La integración de ManejoQRSimple con Banco Económico puede tener comisiones; no hay dato.

### Comunes
Actions de `ProyectosGeneral` (425 minutos) y `SeguridadGeneral` (189 minutos, cuenta general): dentro de la cuota, USD 0. **La cuota de 3.000 minutos de `segurolotengopy` es una sola y la comparten SeguroLoTengo, AAB1 / WhatsApp-Modular y Comunes: septiembre usó 2.958 (98,6 %)**; si un negocio la agota, bloquea el CI de los demás. OCI: USD 0. La cuota de Claude no se expresa en dólares (§4).

## 4. Lo que este corte no puede decir

- **Claude:** la cuota semanal es una sola y no hay corte por negocio. Regla provisional de `docs/06` §4 (por pull requests fusionados), por aprobar. La cifra que falta en todos los negocios son las horas de Claude por cliente.
- **Comparar con septiembre completo:** el 06/10 se relee el export de Google; las cifras de Google de este documento pueden subir.
- **Dependencias de decisiones de Andres:** reglas de asignación (§2, columna «Asignado»), cuenta de Google de …5B3F y …44F7, dueño de `OnboardingGenerico` y de la WABA …1573.
- **Meta:** costo real solo en …2820; el resto, estimado por volumen con tarifas de Bolivia. El cierre exacto lo da el CSV de Facturación de Meta, que baja Andres.

## 5. Costo de la recolección

Dos consultas de Google sobre 17–990 KB, facturadas al mínimo de 10 MiB cada una, dentro del primer TiB gratuito al mes: **USD 0,00**.
