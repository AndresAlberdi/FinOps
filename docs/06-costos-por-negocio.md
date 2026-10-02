# 06 · Control de costos por negocio

| Versión | Fecha | Estado |
|---|---|---|
| 0.1 | 2026-10-02 | Plan aprobado por Andres el 2026-10-02; el mapa de la §3 es preliminar y lo completan las sesiones de cada negocio |

## 1. Requisito y decisión de diseño

PRETSO, Hipatia, NovuChat y SeguroLoTengo son **negocios independientes**: cada uno debe ver su propio costo y llevar su propio control, además del consolidado del ecosistema.

**Decisión:** un solo FinOps (este proyecto) con **una vista por negocio**, no cuatro proyectos de FinOps. Motivo: cuatro proyectos multiplicarían credenciales, accesos y cuota de Claude, que es el mayor costo conocido del ecosistema. Cada negocio recibe su estado mensual y su presupuesto; las palancas las ejecuta la sesión de cada proyecto, como en `CLAUDE.md` (invariante 4).

## 2. Qué es «medido» y qué es «asignado»

- **Directo (medido):** el proveedor ya separa el costo por proyecto, cuenta, WABA o repositorio (Google por proyecto, Meta por WABA, GitHub por repositorio, AWS por cuenta).
- **Asignado (por regla):** el costo es compartido (plan de Claude, GitHub Pro, la VM de OCI con n8n). Se reparte con una regla escrita y se rotula «asignado». No cuenta como ahorro medido (invariante 8).
- **Sin dueño:** lo que ningún negocio reclama queda en «Otros» hasta que Andres decida. Nunca se reparte en silencio.

## 3. Mapa proyecto/servicio → negocio (preliminar)

Fuente: lectura en solo lectura de los proyectos de Google y de su facturación (2026-10-02). Las cuentas de facturación se citan por sus últimos 4 caracteres. «(verificar)» = lo confirma la sesión del negocio.

| Negocio | Google Cloud (proyecto → cuenta de facturación) | Otros servicios conocidos |
|---|---|---|
| NovuChat | `novuchat-demo`, `novuchat-site`, `novuchatstaging` → …3EC8 (con facturación); `novuchat-admin-dev` y `novuchat-admin-prod` sin facturación; `novuchatdemo` (Gemini) en la cuenta C | Meta: WABA de clientes que paga Andres (verificar cuáles); n8n en la VM de OCI |
| PRETSO | `pretso-prod`, `pretso-database` → …5B3F | Dominios (verificar) |
| Hipatia | `hipatia-landing-page`, `hipatia-puntos` → …44F7 | Verificar |
| SeguroLoTengo | Verificar (la demo corre en AWS) | AWS: cuenta de la demo (terminada en 8663); GitHub Pro de `segurolotengopy` (compartido, §4) |
| Por asignar (Andres decide) | `whatsappmodular` y `puntosnb` → …3EC8; `aab1-*`; `encuentramebo-1`; `manejoqrsimple`; `kepler-bolivia`; `snack-laestacion`; `facturadorsiat`; `silsaki-web`; `rag-generico*`; demás | WhatsApp-Modular y AAB1 (socio); ManejoQRSimple; Firmas-NoCualificadas; ChatBotRAG |

**Hallazgo:** PRETSO (…5B3F) e Hipatia (…44F7) facturan por cuentas de facturación que **no son las dos que se exportan hoy** (…3EC8 y la de la cuenta C) y que **la identidad de lectura de este proyecto no lista**. Hoy no hay medición de su costo. Hay que averiguar con Andres a qué cuenta de Google pertenecen y activar su export de facturación a BigQuery, como en `docs/04` (lo activa Andres desde la consola; solo lo puede hacer quien administre esa cuenta de facturación).

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
| 1 | Completar y aprobar el mapa; identificar la cuenta de facturación de PRETSO e Hipatia | Sesiones de los cuatro negocios + Andres | Esta semana |
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
2. Decidir el destino de «Por asignar» (WhatsApp-Modular, AAB1, PuntosNB y los demás).
3. Indicar a qué cuenta de Google pertenecen las cuentas de facturación de PRETSO e Hipatia.
