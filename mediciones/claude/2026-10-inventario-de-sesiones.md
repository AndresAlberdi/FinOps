# Claude — inventario de sesiones abiertas (2026-10-10)

| Versión | Fecha | Estado |
|---|---|---|
| 0.1 | 2026-10-10 | Tarea 2a de la auditoría de cuota (`propuestas/transversal/2026-10-cuota-estabilidad-y-delegacion.md`): solo metadatos con `get_session`; ningún contenido de conversación |

Lectura: 2026-10-10 17:17 UTC. Sin identificadores de sesión (solo título y fechas). El listado de la app se corta en 50 entradas; hay al menos dos más antiguas (las dos «Trivy…» del 1/09). **Este documento no cierra ni modifica ninguna sesión.**

## 1. Resultado

| Clasificación | Sesiones | Criterio (de la auditoría) |
|---|---|---|
| **Cerrar ya** | **39** | Inactiva más de 48 h, creada por otra sesión sin tarea viva, ejecución de una rutina o sesión vacía |
| **Cerrar con relevo** | **12** | Más de 7 días de vida, modelo cambiado después de creada, o principal en Opus |
| **Conservar** | **2** | Creada esta semana, en Sonnet desde el arranque, con bloque en curso |

**Tres hallazgos que la auditoría no tenía:**
1. **39 de las 53 sesiones (74 %) son «cerrar ya», y 24 de ellas son ejecuciones de rutinas** (17 de Hipatia, 5 más de otras tareas y 2 vacías de «Remote control»). Ninguna rutina archiva su sesión al terminar.
2. **Las rutinas no heredan Sonnet.** La de Hipatia corre en **Opus** (esfuerzo medio), la de Bellido en Opus de 1 millón y la mía del 6/10 corrió en **Fable**. La palanca A (sesión principal en Sonnet) no las cubre. Cada ejecución de Hipatia dura unos 30 segundos, así que su costo por vez es probablemente pequeño; **no está medido**.
3. **Una sesión inactiva no gasta cuota.** El costo aparece cuando se reanuda una sesión vieja (relee su contexto) o mientras está en marcha. Por eso archivar las inactivas sirve para que nadie las reanude por costumbre; el ahorro real viene del relevo de las que se siguen usando.

## 2. Principales en uso (14): relevo o conservar

| Sesión | Proyecto | Creada | Edad (días) | Última actividad | Modelo | Clase | Motivo |
|---|---|---|---|---|---|---|---|
| WhatsApp Modular Sesion Principal | WhatsApp-Modular | 2026-08-19 | 52.1 | 2026-10-10 16:14 | sonnet-5-5 | Relevo | 52 días · la más antigua |
| RAG-Generico Sesion General | ChatBotRAG | 2026-09-06 | 34.5 | 2026-10-10 16:19 | opus-5 | Relevo | 34 días **y principal en Opus** |
| SeguridadGeneral Sesión Principal | SeguridadGeneral | 2026-09-12 | 28.5 | 2026-10-09 08:07 | sonnet-5-5 | Relevo | 28 días |
| SeguroLoTengo Sesion Principal | segurolotengo-demo | 2026-09-22 | 18.1 | 2026-10-10 17:16 | sonnet-5-5 | Relevo | más de 7 días; **en marcha: no tocar hasta que Andres diga que terminó** · en marcha |
| Integración Bancard y normativa | segurolotengo-demo | 2026-09-22 | 18.0 | 2026-10-10 03:23 | sonnet-5-5 | Relevo | 18 días |
| Firma CPC y emisión de pólizas con Alianza | segurolotengo-demo | 2026-09-24 | 15.9 | 2026-10-10 03:56 | sonnet-5-5 | Relevo | 16 días |
| NovuChat Sesion Principal | NovuChat | 2026-09-25 | 15.0 | 2026-10-10 16:12 | sonnet-5-5 | Relevo | 15 días |
| NovuChat Sesion Constructora/Operadora | NovuChat | 2026-09-25 | 14.9 | 2026-10-10 12:17 | sonnet-5-5 | Relevo | 15 días **y modelo cambiado después de creada** · era opus-5-5 el 29/09 |
| NovuChat Sesion Cartera de clientes | NovuChat | 2026-09-27 | 13.6 | 2026-10-10 16:12 | sonnet-5-5 | Relevo | 13 días |
| Novuchat Análisis financiero y comercial | NovuChat | 2026-09-29 | 11.6 | 2026-10-10 01:53 | opus-5-5 | Relevo | 11 días, **principal en Opus y modelo cambiado** · era sonnet-5-5 el 29/09 |
| Finops y Optimización Sesion Principal (esta) | FinOps-Ecosistema | 2026-09-29 | 11.6 | 2026-10-10 17:16 | sonnet-5-5 | Relevo | 11 días y modelo cambiado; se cierra la última · arrancó en Opus; contexto de 404.000 tokens |
| Novuchat rearquitectura | NovuChat | 2026-10-01 | 9.1 | 2026-10-10 17:16 | sonnet-5-5 | Relevo | más de 7 días; en marcha · en marcha |
| Novuchat chat | NovuChat | 2026-10-03 | 6.9 | 2026-10-10 17:15 | sonnet-5-5 | Conservar | 6,9 días, en uso; confirmar qué pasó con su PR cerrado · PR cerrado sin fusionar |
| WAM investigaciones y soluciones Meta | WhatsApp-Modular | 2026-10-09 | 1.5 | 2026-10-10 05:44 | sonnet-5-5 | Conservar | 1 día, Sonnet desde el arranque |

## 3. Cerrar ya (39)

| Sesión | Proyecto | Creada | Última actividad | Modelo | Nota | Motivo |
|---|---|---|---|---|---|---|
| Sitio comercial novuchat.site | Novuchat-site | 2026-09-02 | 2026-10-07 21:55 | sonnet-5-5 |  | inactiva 2,8 días; 38 de vida |
| Evaluación TeCNIa 2026 | MejoraContinua-Control | 2026-10-06 | 2026-10-06 04:13 | fable-5-1 |  | inactiva 4,5 días |
| Mejora Continua y Control: inicialización | MejoraContinua-Control | 2026-10-05 | 2026-10-05 16:24 | sonnet-5-5 | PR #1 abierto | inactiva 5 días; **confirmar antes que su PR abierto no tiene trabajo pendiente** |
| Cobrador contrato para consumidores | ManejoQRSimple | 2026-09-19 | 2026-10-03 23:49 | sonnet-5-5 |  | inactiva 6,7 días |
| PRETSO Sesion Principal | PRETSO | 2026-09-25 | 2026-10-03 19:49 | sonnet-5-5 | contrato con entrega en octubre | inactiva 6,9 días; **comprobar que su ESTADO.md está al día antes de archivar** |
| ProyectosClaude Sesion Principal | Claude-Proyectos | 2026-09-21 | 2026-10-03 18:48 | sonnet-5-5 | PR #1 cerrado sin fusionar | inactiva 6,9 días; confirmar su PR cerrado |
| FNC repositorio main | Firmas-NoCualificadas | 2026-09-02 | 2026-10-03 18:23 | sonnet-5-5 |  | inactiva 6,9 días |
| Hipatia repositorio local y hardening | Hipatia | 2026-09-19 | 2026-10-03 18:23 | sonnet-5-5 |  | inactiva 6,9 días |
| Encuentrame Sesion Principal | Encuentrame.BO | 2026-08-20 | 2026-10-03 18:23 | sonnet-5-5 |  | inactiva 6,9 días; 51 de vida |
| Onboarding genérico: revisión y validación | Onboarding-Generico | 2026-08-22 | 2026-10-03 18:23 | sonnet-5-5 |  | inactiva 6,9 días; 49 de vida |
| Pendientes en ManejoQRSimple | ManejoQRSimple | 2026-09-20 | 2026-10-03 18:22 | sonnet-5-5 |  | inactiva 6,9 días |
| Hacer determinista el test de llave equivocada AES | ManejoQRSimple | 2026-10-01 | 2026-10-03 18:22 | sonnet-5-5 | creada por «Pendientes en ManejoQRSimple» (`parentSessionId`) | hija de otra sesión, PR fusionado |
| Sistema de Aprendizaje recomendaciones | Sistema_Aprendizaje | 2026-10-03 | 2026-10-03 18:20 | fable-5-1 | vivió 1 minuto | inactiva 6,9 días |
| Remote control (carpeta temporal) | scratch | 2026-10-10 | 2026-10-10 05:04 | opus-5-5 | vivió 3 segundos; vacía | sin contenido |
| Remote control (worktree de WhatsApp-Modular) | WhatsApp-Modular | 2026-10-09 | 2026-10-09 20:32 | sonnet-5-5 | vivió 7 segundos; vacía | sin contenido |
| FinOps: releer el export de facturación (6 de octubre) | FinOps-Ecosistema | 2026-10-06 | 2026-10-06 13:03 | fable-5-1 | tarea programada `finops-releer-…`; corrió en Fable | ejecución de rutina terminada |
| Recordatorio: pedir al Dr. Bellido lo que falta de octubre | NovuChat | 2026-09-28 | 2026-09-28 14:41 | opus-5-5 [1m] | tarea programada | ejecución de rutina terminada |
| App Check Hipatia — control cada 12 h (23/09) | Hipatia | 2026-09-23 | 2026-09-23 01:06 | opus-5 [1m] | tarea programada `appcheck-hipatia` | ejecución de rutina terminada |
| Reintento del reparto al socio (AAB1) ×2 | WhatsApp-Modular | 2026-09-20 | 2026-09-20 14:14 | opus-5 [1m] | tarea programada `reintento-socio-aab1` | ejecuciones de rutina terminadas |
| App Check Hipatia: ¿ya se puede exigir? ×17 (2 al 10/10, dos por día) | Hipatia | 2026-10-02 | 2026-10-10 13:08 | opus-5-5, esfuerzo medio (muestra: la primera y la última) | tarea programada `app-check-hipatia`; cada una vivió unos 30 segundos | 17 ejecuciones de una rutina, **todas en Opus** |
| Trivy vencen excepciones libssl3 ×2 (1/09) | WhatsApp-Modular | 2026-09-01 | 2026-09-01 19:48 | (no leído) | fuera del tope de 50 del listado | inactivas desde el 1/09 |

## 4. Modelos de las sesiones principales

14 principales: 11 en Sonnet, 2 en Opus (RAG-Generico y Análisis financiero de NovuChat) y 1 (esta) que arrancó en Opus y pasó a Sonnet. Fable aparece en 3 sesiones cortas (TeCNIa, Sistema de Aprendizaje y la rutina del 6/10); el plan marca 9 % en la ventana semanal de Fable.

## 5. Límites

- Solo metadatos; no se leyó ningún transcript.
- No se midió el costo de ninguna sesión: la hipótesis «las sesiones largas gastan la cuota» sigue sin medir. Lo que sí dice este inventario es **cuáles son**.
- «Cerrar ya» es una clasificación, no una orden: archivar lo decide cada sesión dueña con Andres, tras comprobar su `ESTADO.md`.
