# 06 · Control de costos por negocio

| Versión | Fecha | Estado |
|---|---|---|
| 0.1 | 2026-10-02 | Plan aprobado por Andres el 2026-10-02 |
| 0.2 | 2026-10-02 | Mapa de la §3 completado con las respuestas de las cuatro sesiones; falta la decisión de Andres sobre lo «por asignar» |

## 1. Requisito y decisión de diseño

PRETSO, Hipatia, NovuChat y SeguroLoTengo son **negocios independientes**: cada uno debe ver su propio costo y llevar su propio control, además del consolidado del ecosistema.

**Decisión:** un solo FinOps (este proyecto) con **una vista por negocio**, no cuatro proyectos de FinOps. Motivo: cuatro proyectos multiplicarían credenciales, accesos y cuota de Claude, que es el mayor costo conocido del ecosistema. Cada negocio recibe su estado mensual y su presupuesto; las palancas las ejecuta la sesión de cada proyecto, como en `CLAUDE.md` (invariante 4).

## 2. Qué es «medido» y qué es «asignado»

- **Directo (medido):** el proveedor ya separa el costo por proyecto, cuenta, WABA o repositorio (Google por proyecto, Meta por WABA, GitHub por repositorio, AWS por cuenta).
- **Asignado (por regla):** el costo es compartido (plan de Claude, GitHub Pro, la VM de OCI con n8n). Se reparte con una regla escrita y se rotula «asignado». No cuenta como ahorro medido (invariante 8).
- **Sin dueño:** lo que ningún negocio reclama queda en «Otros» hasta que Andres decida. Nunca se reparte en silencio.

## 3. Mapa proyecto/servicio → negocio (v0.2)

Fuentes: lectura en solo lectura de los proyectos de Google y su facturación (2026-10-02) y las respuestas de las sesiones de PRETSO, Hipatia, SeguroLoTengo y NovuChat del mismo día. Cuentas de facturación por sus últimos 4 caracteres. «(verificar)» = sin confirmar.

| Negocio | Google Cloud (proyecto → cuenta de facturación) | AWS, Meta, GitHub y otros |
|---|---|---|
| **NovuChat** | `novuchat-demo` (consola), `novuchat-site`, `novuchatstaging` → …3EC8. `novuchat-admin-dev` y `novuchat-admin-prod`: sin facturación (su dueño, verificar). `novuchatdemo` (Gemini de producción) en la cuenta C. `novuchat-pruebas` (Gemini de pruebas; gastó las baterías del 30/09 y el 01/10): **no figura en ninguna exportación; verificar** si es el proyecto autogenerado de la cuenta C | Meta: WABA de Bellido (…3951; la tarjeta está cargada en esa WABA) y de NovuChat (…1048). GitHub: `NovuChat` y `novuchat-site` (públicos); `ManejoQRSimple` y `OnboardingGenerico` (verificar). Dominio `novuchat.site`. n8n: flujos por cliente |
| **PRETSO** | `pretso-prod` y `pretso-database` → …5B3F | Sin Meta, n8n, dominios ni Claude API. Repo público `PRETSO` (Actions gratis) |
| **Hipatia** | `hipatia-puntos` (producción) y `hipatia-landing-page` (dueño de la landing: verificar) → …44F7. `puntosnb` (pruebas y pilotos; «PuntosNB» es el nombre histórico del repo) → …3EC8 | Dominio `hipatiabo.com` (costo anual desconocido). Repo público `PuntosNB`. Meta: solo planeado |
| **SeguroLoTengo** | Ninguno | AWS: cuenta …8663 (demo, Amplify, DynamoDB, S3, SES, Textract/Rekognition; Transfer Family y VPN apagados). GitHub: `SeguroLoTengoDemo` (privado) y el plan Pro de `segurolotengopy`. Lovable y Snyk: costo desconocido |
| **Por asignar (decide Andres)** | `whatsappmodular` → …3EC8 (de WhatsApp-Modular); `aab1-*`; `encuentramebo-1` (y la cuenta C con `encuentramebo`); `manejoqrsimple`; `kepler-bolivia`; `snack-laestacion`; `facturadorsiat`; `silsaki-web`; `rag-generico*`; `demoa`/`demob`; otros | WhatsApp-Modular (Meta: AAB1 y WABA compartida con el Demo A), VM de OCI con n8n (comparten NovuChat y WhatsApp-Modular), WABA de Silvana (…4125, «paga Silvana»), WABA de prueba (…8154), Interseguros (dueño no identificado), `ChatbotRAG`, `RAG-Generico`, `FirmadorMasivoCualificado`, `cps-plataforma`, `encuentrame.bo`, `ProyectosGeneral` |

**Hallazgos:**
1. **PRETSO (…5B3F) e Hipatia producción (…44F7) facturan por cuentas que no se exportan hoy** ni lista la identidad de lectura de este proyecto; las propias sesiones tampoco pueden leerlas. Hoy no hay medición de su costo. Hay que averiguar a qué cuenta de Google pertenecen y activar su export a BigQuery (`docs/04`; lo hace Andres desde la consola).
2. **NovuChat e Hipatia (`puntosnb`) comparten la cuenta de facturación …3EC8**, junto con presupuestos mezclados de ambos. La separación se hace por proyecto de Google, no por cuenta; la separación de presupuestos se propone aparte.
3. **El costo de PRETSO en la nube hoy es de centavos**; el riesgo es de visibilidad: `pretso-database`, el sitio en uso, no tiene presupuesto verificado.
4. **El riesgo de SeguroLoTengo** es Transfer Family y la VPN con Alianza si se encienden (se cobran por hora), y el paso a producción; el presupuesto de USD 50 al mes está muy por encima del gasto real de septiembre y no distingue esos servicios.
5. **La VM de OCI la comparten NovuChat y WhatsApp-Modular**, no un solo negocio: la regla de la §4 reparte la cuota gratuita, no dinero.

## 4. Reglas de asignación de lo compartido

| Costo compartido | Regla propuesta | Estado |
|---|---|---|
| Plan de Claude (cuota) | No hay corte por proyecto en `get_usage`. Regla provisional: PR fusionados por negocio en la ventana. Se rotula «asignado». Si algún negocio usa la API de Anthropic con claves propias, ese gasto es directo (Console, por clave). | Por aprobar |
| GitHub Pro de `segurolotengopy` (USD 4 al mes) | Por partes iguales entre los negocios con repositorios privados en esa cuenta. Los minutos de Actions sí se miden por repositorio. | Por aprobar |
| VM de OCI con n8n (USD 0; Always Free) | Se asigna la cuota gratuita, no dinero: por ejecuciones de n8n de cada negocio (verificar que n8n las entregue por flujo). Se vigila el riesgo de que un negocio agote lo gratuito de todos. | Por aprobar |
| Meta, WABA que paga Andres | Directo por WABA. La de Silvana (…4125) se mide etiquetada «paga Silvana». | Aplicable |

## 5. Entregables

1. `mediciones/negocios/<negocio>/<AAAA-MM>-estado.md`: costo directo por proveedor, costo asignado, tendencia frente al mes anterior, alertas y palancas candidatas. Solo cifras agregadas; sin clientes ni identificadores completos (el repositorio es público; invariante 6).
2. Mapa de este documento, versionado y actualizado cuando entre o salga un servicio.
3. Script de solo lectura `scripts/negocios/` que une los exports ya existentes y aplica el mapa; sin credenciales embebidas y con salida solo en `datos/`.
4. Presupuestos y alertas por negocio, propuestos como bloque para la sesión dueña (`propuestas/<proyecto>/`): presupuestos de Google y AWS Budgets; para Meta no existe alerta de gasto, así que es revisión mensual.

## 6. Fases y orden

| Fase | Contenido | Quién | Cuándo |
|---|---|---|---|
| 1 | Mapa completado por las cuatro sesiones (hecho el 2026-10-02); falta la decisión de Andres sobre lo «por asignar» y la cuenta de facturación de PRETSO e Hipatia | Andres | Esta semana |
| 2 | Cortar por negocio las líneas base ya medidas (Google, Meta, GitHub, AWS, OCI), sin accesos nuevos | FinOps | Tras el mapa |
| 3 | Aprobar las reglas de la §4 | Andres | Con la fase 2 |
| 4 | Export de facturación de PRETSO e Hipatia | Andres (consola) y FinOps | Cuando conste la cuenta |
| 5 | Primer estado por negocio: septiembre provisional (Google se cierra el 2026-10-06); primer cierre oficial, octubre, del 1 al 6 de noviembre | FinOps | Octubre–noviembre |
| 6 | Presupuestos y alertas por negocio; palancas por negocio | Sesiones dueñas | Tras dos meses de datos |

## 7. Coordinación

- **NovuChat · Análisis financiero y comercial** aporta los ingresos; FinOps, el costo. El margen se calcula una sola vez.
- **PRETSO** tiene contrato con entrega en octubre: su costo es lo primero que se hace visible.
- Esta tarea toca solo lectura. Ningún cambio en los proyectos de los negocios sin su sesión dueña y el «sí» de Andres.

## 8. Pendiente de decisión de Andres

1. Aprobar las reglas de asignación de la §4.
2. Decidir el destino de «Por asignar»: ¿WhatsApp-Modular y AAB1 son negocios propios? ¿Interseguros pertenece a SeguroLoTengo? ¿Qué hacer con encuentrame.bo, ManejoQRSimple y los demás?
3. Indicar a qué cuenta de Google pertenecen las cuentas de facturación de PRETSO e Hipatia (…5B3F y …44F7) y quién lleva `hipatia-landing-page`.
4. Decir si paga Lovable y Snyk, y el costo anual del dominio `hipatiabo.com`.
