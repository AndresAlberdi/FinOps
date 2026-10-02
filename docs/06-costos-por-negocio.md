# 06 · Control de costos por negocio

| Versión | Fecha | Estado |
|---|---|---|
| 0.1 | 2026-10-02 | Plan aprobado por Andres el 2026-10-02 |
| 0.2 | 2026-10-02 | Mapa de la §3 completado con las respuestas de las cuatro sesiones |
| 0.3 | 2026-10-02 | Lo «por asignar» resuelto con los valores por defecto que Andres aceptó el 2026-10-02: quinto negocio «AAB1 / WhatsApp-Modular», Encuéntrame.BO y ManejoQRSimple como negocios propios, y una categoría «Comunes» |

## 1. Requisito y decisión de diseño

PRETSO, Hipatia, NovuChat y SeguroLoTengo son **negocios independientes**: cada uno debe ver su propio costo y llevar su propio control, además del consolidado del ecosistema. Desde la v0.3 se suman «AAB1 / WhatsApp-Modular», Encuéntrame.BO y ManejoQRSimple como unidades propias y una categoría «Comunes» (§3).

**Decisión:** un solo FinOps (este proyecto) con **una vista por negocio**, no cuatro proyectos de FinOps. Motivo: cuatro proyectos multiplicarían credenciales, accesos y cuota de Claude, que es el mayor costo conocido del ecosistema. Cada negocio recibe su estado mensual y su presupuesto; las palancas las ejecuta la sesión de cada proyecto, como en `CLAUDE.md` (invariante 4).

## 2. Qué es «medido» y qué es «asignado»

- **Directo (medido):** el proveedor ya separa el costo por proyecto, cuenta, WABA o repositorio (Google por proyecto, Meta por WABA, GitHub por repositorio, AWS por cuenta).
- **Asignado (por regla):** el costo es compartido (plan de Claude, GitHub Pro, la VM de OCI con n8n). Se reparte con una regla escrita y se rotula «asignado». No cuenta como ahorro medido (invariante 8).
- **Sin dueño:** lo que ningún negocio reclama queda en «Otros» hasta que Andres decida. Nunca se reparte en silencio.

## 3. Mapa proyecto/servicio → negocio (v0.3)

Fuentes: lectura en solo lectura de los proyectos de Google y su facturación (2026-10-02); respuestas de las sesiones de PRETSO, Hipatia, SeguroLoTengo y NovuChat del mismo día; fichas de Claude-Proyectos (`proyectos/`) e inventario de SeguridadGeneral (§3 y §4). Cuentas de facturación por sus últimos 4 caracteres. «(verificar)» = sin confirmar.

| Unidad | Google Cloud (proyecto → cuenta de facturación) | AWS, Meta, GitHub y otros |
|---|---|---|
| **NovuChat** | `novuchat-demo` (consola), `novuchat-site`, `novuchatstaging` → …3EC8. `novuchat-admin-dev` y `novuchat-admin-prod`: sin facturación. `novuchatdemo` (Gemini de producción) en la cuenta C. `novuchat-pruebas` (Gemini de pruebas): **no figura en ninguna exportación; verificar** si es el proyecto autogenerado de la cuenta C | Meta: WABA de Bellido (…3951; tarjeta cargada en esa WABA), de NovuChat (…1048), de Clínica Platinum (…7545, demo), de Silvana (…4125, rotulada «paga Silvana») y de prueba (…8154). GitHub: `NovuChat` y `novuchat-site` (públicos). Dominio `novuchat.site`. n8n: flujos por cliente |
| **PRETSO** | `pretso-prod` y `pretso-database` → …5B3F | Sin Meta, n8n, dominios ni Claude API. Repo público `PRETSO` (Actions gratis) |
| **Hipatia** | `hipatia-puntos` (producción) y `hipatia-landing-page` (dueño de la landing: verificar) → …44F7. `puntosnb` (pruebas y pilotos; «PuntosNB» es el nombre histórico del repo) → …3EC8 | Dominio `hipatiabo.com` (costo anual desconocido). Repo público `PuntosNB`. Meta: solo planeado |
| **SeguroLoTengo** | Ninguno | AWS: cuenta …8663 (demo; Amplify, DynamoDB, S3, SES, Textract/Rekognition; Transfer Family y VPN apagados). Meta: costo del OTP (mensajes de autenticación de la WABA …2820) y WABA de Interseguros (…1573; verificar). GitHub: `SeguroLoTengoDemo` (privado), el plan Pro de `segurolotengopy` (compartido, §4) y los repos de firmas (`FirmadorMasivoCualificado`, `Firmas-NoCualificadas`, `cps-plataforma`; verificar). Lovable y Snyk: costo desconocido |
| **AAB1 / WhatsApp-Modular** (nuevo) | `whatsappmodular` → …3EC8; `aab1-dev`, `aab1-landing` y `aab1-receptor`: sin facturación | Proveedor tecnológico ante Meta; receptor de clientes. Meta: WABA `…2820` (AAB1; su costo de OTP se carga a SeguroLoTengo). GitHub: `WhatsAppModular` (privado). Parte de la VM de OCI con n8n (§4) |
| **Encuéntrame.BO** (nuevo) | `encuentramebo-1` (producción): sin facturación; `encuentramebo` (cuenta C): costo cero | Repo `encuentrame.bo` (cuenta `segurolotengopy`). Costo hoy: cero |
| **ManejoQRSimple** (nuevo) | `manejoqrsimple`: sin facturación | Repo `ManejoQRSimple` (cuenta `segurolotengopy`). Integración con Banco Económico: comisiones y costos de la integración, desconocidos (verificar) |
| **Comunes** | `proyectosgeneral-d35a4`, `sg-wif-prueba-…`: sin facturación | Plan de Claude, GitHub Pro, VM de OCI con n8n (cuota gratuita compartida), `RAG-Generico`, `ChatBotRAG`, `OnboardingGenerico` (hasta que Andres confirme su dueño), repos de gobierno (`SeguridadGeneral`, `Claude-Proyectos`, `FinOps`, `ProyectosGeneral`) |
| **Sin costo hoy** (se asigna al facturar) | `kepler-bolivia`, `snack-laestacion`, `demob-…`, `demoa-…`, `virtual-steam-demo`, `silsaki-web`, `facturadorsiat`, `pruebas-mj`, `rag-generico*`: todos sin facturación | WABA `…8189` (huérfana, en dirhams, sin líneas): revisar saldo y cerrar |

**Hallazgos:**
1. **De los 28 proyectos de Google visibles, solo 9 tienen facturación activa.** El costo de Google de los otros 19 es cero; su asignación puede esperar al día en que facturen.
2. **PRETSO (…5B3F) e Hipatia producción (…44F7) facturan por cuentas que no se exportan hoy** ni lista la identidad de lectura de este proyecto; las propias sesiones tampoco pueden leerlas. Hay que averiguar a qué cuenta de Google pertenecen y activar su export a BigQuery (`docs/04`; lo hace Andres desde la consola).
3. **NovuChat, Hipatia (`puntosnb`) y WhatsApp-Modular comparten la cuenta de facturación …3EC8**, con presupuestos mezclados. La separación se hace por proyecto de Google, no por cuenta; separar presupuestos se propone aparte.
4. **El costo de PRETSO en la nube hoy es de centavos**; el riesgo es de visibilidad: `pretso-database`, el sitio en uso, no tiene presupuesto verificado.
5. **El riesgo de SeguroLoTengo** es Transfer Family y la VPN con Alianza si se encienden (se cobran por hora) y el paso a producción; el presupuesto de USD 50 al mes está muy por encima del gasto real de septiembre y no distingue esos servicios.
6. **La VM de OCI la comparten NovuChat y WhatsApp-Modular:** la regla de la §4 reparte la cuota gratuita, no dinero.
7. **Cargo entre unidades:** el OTP lo sirve la plataforma de AAB1 / WhatsApp-Modular pero lo usa SeguroLoTengo; su costo de Meta (USD 0,03 en septiembre) se carga a SeguroLoTengo y el resto de la plataforma queda en AAB1 / WhatsApp-Modular.

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
| 1 | Mapa completado (v0.3, 2026-10-02); falta la cuenta de facturación de PRETSO e Hipatia | Andres | Esta semana |
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

Resuelto el 2026-10-02 (valores por defecto aceptados): quinto negocio «AAB1 / WhatsApp-Modular» con el OTP cargado a SeguroLoTengo; Encuéntrame.BO y ManejoQRSimple como unidades propias; repos de firmas con SeguroLoTengo; `OnboardingGenerico` en «Comunes» hasta confirmar dueño.

Abierto:
1. Aprobar las reglas de asignación de la §4.
2. Indicar a qué cuenta de Google pertenecen las cuentas de facturación de PRETSO e Hipatia (…5B3F y …44F7) y quién lleva `hipatia-landing-page`.
3. Decir si paga Lovable y Snyk, y el costo anual del dominio `hipatiabo.com`.
4. Confirmar el dueño de `OnboardingGenerico` y de la WABA de Interseguros (…1573).
