# Estado de costos por negocio — septiembre 2026

| Versión | Fecha | Estado |
|---|---|---|
| 0.1 | 2026-10-02 | Provisional: Google incompleto. **Su cifra de NovuChat (USD 2,82 neto) era errónea por el export incompleto** |
| 0.2 | 2026-10-04 | **Septiembre cerrado en Google** (export completo hasta el 30/09). NovuChat pasa de unos USD 2,82 a **unos USD 24,92 neto**. Sigue sin medición PRETSO e Hipatia producción |

Cifras en USD, agregadas; cuentas por sus últimos 4 caracteres; datos crudos en `datos/` (no versionado). «**Medido**» = lo informa el proveedor por proyecto, cuenta, WABA o repositorio. «**Asignado**» = reparto de un costo compartido con una regla de `docs/06` §4, **todavía por aprobar**; no cuenta como medido.

## 1. Cobertura de los datos (qué tan completo es este corte)

| Fuente | Llega hasta | Estado |
|---|---|---|
| Google, cuenta principal (…3EC8) | 2026-10-03 | **Septiembre completo** |
| Google, cuenta C | 2026-10-03 | **Septiembre completo** |
| Google, cuentas …5B3F (PRETSO) y …44F7 (Hipatia producción y landing) | — | **Sin medición:** no se exportan hoy (`docs/06` §3, hallazgo 2) |
| AWS (…8663) | 2026-09-30 | Completo |
| Meta (WABA) | 2026-09-30 | Completo (vía `costos:meta` de WhatsApp-Modular); costo real solo en la WABA …2820 |
| GitHub Actions | 2026-09-30 | Completo (estimado por trabajos) |
| OCI | 2026-09-30 | Completo (USD 0) |
| Claude (cuota) | — | No se corta por negocio (§4) |

## 2. Resumen por negocio

| Negocio | Directo medido (bruto) | Créditos de Google | Directo neto | Asignado (regla por aprobar) | Cobertura |
|---|---|---|---|---|---|
| NovuChat | **35,10** (Google 35,09; Meta 0,01 estimado) | −10,19 | **24,92** | — | Google completo |
| SeguroLoTengo | **4,99** (AWS 4,96; Meta OTP 0,03) | — | **4,99** | GitHub Pro 2,00 | Completa |
| AAB1 / WhatsApp-Modular | **0,17** (Google) | −0,17 | **0,00** | GitHub Pro 2,00 | Google completo |
| Hipatia | **0,04** (solo `puntosnb`) | −0,04 | **0,00** | — | **Producción sin medir** |
| PRETSO | **sin medición** (cuenta …5B3F no exportada) | — | — | — | Sin dato |
| Encuéntrame.BO | **0,00** (0,0033 bruto) | −0,00 | **0,00** | — | Google completo |
| ManejoQRSimple | **0,00** (sin facturación) | — | **0,00** | — | Integración con Banco Económico sin medir |
| Comunes | **0,00** (cargo «Invoice» 0,0025; Actions dentro de la cuota; OCI 0) | — | **0,00** | — | Completa, salvo Claude |
| **Total medido** | **40,31** | **−10,40** | **29,91** | 4,00 | |

**El gasto neto de septiembre es de unos USD 30, y 24,91 son Gemini** (cuenta C, NovuChat): 21,74 en dos días (29 y 30/09: baterías de pruebas y concurso de Bellido, con credencial de producción y modelos no-lite) y 3,17 en el resto del mes. Los créditos de Google solo existen en la cuenta principal (cubren todo su bruto de 10,40). Si esos créditos vencen o tienen tope, el costo de esa cuenta pasa del neto al bruto (unos 10 a 18 USD al mes).

## 3. Detalle por negocio

### NovuChat
| Proveedor | Concepto | Bruto | Créditos | Neto | Tipo |
|---|---|---|---|---|---|
| Google (principal) | `novuchat-demo`: Cloud Run Functions 7,72 (incluye la instancia mínima, ~0,54 por día desde el 17/09); Secret Manager 0,94 | 8,65 | −8,66 | 0,00 | Medido |
| Google (principal) | `novuchat-site`: Vertex AI 0,96; Secret Manager 0,15; Cloud Run Functions 0,02 | 1,12 | −1,12 | 0,00 | Medido |
| Google (principal) | `novuchatstaging`: Secret Manager 0,27; Cloud Run Functions 0,14 | 0,41 | −0,41 | 0,00 | Medido |
| Google (cuenta C) | `novuchatdemo`: **Gemini API**, 21,74 en el 29 y 30/09 y 3,17 en el resto | 24,91 | 0,00 | **24,91** | Medido |
| Meta | WABA …1048 (NovuChat), …3951 (Bellido), …7545 (Platinum), …4125 (Silvana, «paga Silvana»), …8154 (prueba): 0,0113 estimado de la …1048; el resto, servicio gratis | 0,01 | — | 0,01 | Estimado |
| OCI / n8n | Cuota gratuita compartida con WhatsApp-Modular | 0,00 | — | 0,00 | Medido |

**Observaciones:**
- **El consumo de Gemini de septiembre ya está completo y es medido, no estimado:** USD 24,91. De ellos, 15,66 son de los modelos no-lite (`gemini 3.5 flash` 9,19 y `gemini 3.8 flash` 6,47), usados solo en pruebas. El modelo en uso, `3.5 flash-lite`, costó 9,25. El export **sí** muestra el consumo prepago (la sospecha contraria quedó refutada; ver `mediciones/gcp/2026-09-linea-base-cuenta-c.md`).
- **El «fijo de plataforma ≈ USD 22 al mes» de NovuChat queda explicado:** unos 16 USD al mes son la instancia mínima de la función de `novuchat-demo` (0,54 por día, desde el 17/09); hoy los créditos la cubren. Lo demás del fijo estimado (Secret Manager, staging, dominio) suma unos 2 a 3 USD al mes medidos.
- **El pronóstico de USD 169 de la consola no es gasto:** es el «costo previsto» de Google, que extrapola el 29 y 30/09.
- **El margen que NovuChat estimó (USD 16,7 al mes por cliente) no incluye este gasto de pruebas ni el costo de las baterías;** son costo de desarrollo, no de operación por cliente.

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
| Google (principal) | `whatsappmodular` (Secret Manager 0,14) y `aab1-landing` (0,03) | 0,17 | −0,17 | 0,00 | Medido |
| Meta | Costo del OTP de la WABA …2820: se carga a SeguroLoTengo | 0,00 | — | 0,00 | Cargo entre unidades |
| GitHub | `WhatsAppModular`: 667 minutos de Actions (22 % de la cuota) | 0,00 | — | 0,00 | Estimado |
| GitHub | Plan Pro, parte de la unidad | 2,00 | — | 2,00 | Asignado |
| OCI | Parte de la cuota gratuita de la VM con n8n | 0,00 | — | 0,00 | Medido |

### Hipatia
| Proveedor | Concepto | Bruto | Créditos | Neto | Tipo |
|---|---|---|---|---|---|
| Google (principal) | `puntosnb` (pruebas y pilotos): Cloud Run Functions 0,04 | 0,04 | −0,04 | 0,00 | Medido |
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
- **Google de septiembre está cerrado** (v0.2); queda confirmar el 06/10 que Google no reexpresó cifras, lo que la rutina ya hace.
- **Dependencias de decisiones de Andres:** reglas de asignación (§2, columna «Asignado»), cuenta de Google de …5B3F y …44F7, dueño de `OnboardingGenerico` y de la WABA …1573.
- **Meta:** costo real solo en …2820; el resto, estimado por volumen con tarifas de Bolivia. El cierre exacto lo da el CSV de Facturación de Meta, que baja Andres.

## 5. Costo de la recolección

Consultas de Google de 17 KB a 5,5 MB, dentro del primer TiB gratuito al mes: **USD 0,00**.
