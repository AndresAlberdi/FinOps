# 00 · Alcance y principios

| Versión | Fecha | Estado |
|---|---|---|
| 0.1 | 2026-09-28 | Borrador inicial; se completa en el Bloque 1 del prompt de arranque |

## 1. Objetivo

Reducir el costo total del ecosistema (suscripciones, consumo en nubes, mensajería, IA y herramientas) de forma **medible y reversible**, manteniendo o mejorando funcionalidad, calidad y postura de seguridad. El éxito se mide en costo mensual real frente a la línea base, con cero regresiones atribuibles a una optimización.

## 2. Alcance

| Dominio | Qué entra | Unidad de costo principal |
|---|---|---|
| IA — Claude / Anthropic | Plan Max, créditos de uso, API y Console, Claude Code multiagente | Tokens por modelo; USD de créditos por mes |
| IA — Google (Gemini / Vertex AI) | Claves de Gemini, Vertex AI en los proyectos que lo usan | Tokens o caracteres por modelo |
| AWS | Cuentas y regiones en uso (SeguroLoTengo, firma F2, otros) | USD por servicio y etiqueta |
| Google Cloud y Firebase | Los proyectos de las tres cuentas de Google del inventario | USD por proyecto y SKU |
| OCI | n8n autoalojado y lo que comparta la máquina | Horas de cómputo, almacenamiento, egreso |
| n8n | Ejecuciones, flujos y su consumo de APIs de terceros | Ejecuciones por mes; llamadas a APIs pagas |
| Meta — WhatsApp Cloud API | Conversaciones o mensajes por categoría y número | Mensajes o conversaciones facturables |
| GitHub | Planes, licencias GHAS, minutos y almacenamiento de Actions | USD por committer activo; minutos |
| Otros | Dominios, correo, Lovable, SaaS de diseño y los que aparezcan | USD por suscripción |

Fuera de alcance: decisiones de precio de venta de los productos, contabilidad y facturación a clientes, y cualquier cambio de arquitectura que no tenga el costo como motivo principal (se deriva al proyecto dueño).

## 3. Principios

1. **Primero visibilidad, después optimización.** Sin línea base por proveedor no se propone ninguna palanca.
2. **Eliminar desperdicio antes que negociar precio.** Recursos huérfanos, proyectos sin uso, duplicados y sobredimensionamiento van antes que compromisos de uso o cambios de plan.
3. **El costo se mide en la unidad del negocio.** Además del USD total, cada producto se mide por su unidad (por conversación, por firma, por comprobante, por tarea de agente).
4. **Reversibilidad.** Se prefieren cambios que se deshacen en minutos; los compromisos a largo plazo (planes anuales, reservas) exigen dos meses de medición estable.
5. **Seguridad y calidad son restricciones, no variables.** Ver `03-guardarrailes.md`.
6. **Una fuente de verdad por dato.** Cuentas y proyectos: `~/SeguridadGeneral/01-seguridad/10-inventario-de-proyectos.md`. Costos de herramientas del pipeline: `~/SeguridadGeneral/00-gobernanza/04-matriz-herramientas-y-costos.md`. Módulos y fichas: `~/Claude-Proyectos/proyectos/`.
