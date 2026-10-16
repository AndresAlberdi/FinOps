# Estado de emergencia, relevo de sesiones y conocimiento — propuesta única

> Origen: FinOps-Ecosistema, 2026-10-16, por pedido de Andres.
> **Veredicto del guardián (2026-10-16): aprobada con condiciones; esta versión incorpora las nueve (C1 a C9).** Como toca los guardarraíles §1.8 y §1.9 y la gobernanza del pipeline, **antes de entregarla a SeguridadGeneral pasa por el agente `seguridad`** (pendiente).
> Fuentes: notas de las sesiones «Optimización de emergencia» y «Optimizar consumo de créditos» (SeguroLoTengo, 2026-10-16); los relevos de WhatsApp-Modular, RAG y SeguridadGeneral (11 al 13-oct); la medición de tokens del 14-oct y el encargo del 14-oct (**ambos sin versionar** en la carpeta principal de FinOps: `mediciones/claude/2026-10-14-consumo-de-tokens.md` y `propuestas/transversal/2026-10-14-hallazgos-de-tokens-y-replanteo-post-viernes.md`).
> Marcas: **[M]** medido (las cifras de tokens y dólares del 14-oct llevan margen ±30 % y las tarifas se verifican contra la página oficial antes de adoptar); **[O]** opinión de una sesión; **[V]** vivido en los relevos de FinOps.
> No rediscute las decisiones A, B y C del modelo por rol ni la norma de ciclo de vida (`propuestas/seguridad-general/2026-10-ciclo-de-vida-de-sesiones.md`); las completa.

## Evidencia
- **[M] ±30 %** El plan Max 20x rinde del orden de 30 veces lo que rinden los créditos por dólar (≈1.600 USD equivalentes a tarifa de API por semana frente a 200 USD al mes; del informe de tokens del 14-oct, no versionado).
- **[M] ±30 %** El gasto es el contexto, no el modelo: más del 90 % es relectura de caché, ~300.000 tokens de contexto por llamada en las sesiones largas, ≈0,064 USD por llamada. Dos sesiones llegaron a 352.000 y 456.000 tokens sin relevar.
- **[M]** El 14-oct el plan semanal llegó a 100 % y en menos de una hora se gastaron ~50 USD de créditos; el extra pasó de 71 a 88 USD (de 120) el 15-oct. Hoy (16-oct): semanal 0 %, extra 74 % (89,12 USD), quedan ~31 USD de reserva.
- **[M], un solo caso:** despertar una sesión con contexto grande gastó ~2 USD según la sesión «Optimizar consumo de créditos». No se generaliza.
- **[V]** En los tres relevos de FinOps hubo conocimiento solo en la cabeza de la antigua: RAG (4 pendientes y 10 reglas), WAM (9 pendientes y 10 reglas), SeguridadGeneral (5 pendientes y 7 reglas).

## 1. Estado de emergencia
**Regla de Andres (2026-10-16), que manda sobre el resto:** si la cuota **semanal** llega al **90 %** se pasa a **MODO EMERGENCIA**: se cierran las rutinas, se evitan las tareas automáticas, se paran las sesiones y las prioridades se deciden con Andres, que toma desde ahí las decisiones sobre los recursos escasos. Los demás niveles son una propuesta de FinOps para anticiparlo (las dos notas de SeguroLoTengo coinciden en la idea, no en los números; los umbrales distintos del 90 % son **[O]** hasta que Andres los fije):

| Nivel | Se entra cuando | Qué cambia |
|---|---|---|
| **Normal** | semanal <80 % y extra gastado <70 % del tope mensual | Sonnet con esfuerzo medio; rutinas activas; el crédito extra no se usa como presupuesto de trabajo. |
| **Alerta** **[O]** | semanal ≥80 %, o extra gastado ≥70 % | Aviso a Andres; sin agentes ni flujos en paralelo; estimación antes de tareas grandes; `get_usage` al empezar y al terminar cada bloque. |
| **MODO EMERGENCIA** (regla de Andres) | semanal ≥90 % | Se cierran las rutinas que no estén en la lista protegida, se evitan las tareas automáticas, se paran las sesiones y Andres define las prioridades. Exploración en Haiku; Opus solo para planificar en una sesión corta; no se retoman sesiones largas. |
| **Parada del crédito extra** **[O]** | extra gastado ≥85 % del tope (102 USD de 120; la sesión «Optimización de emergencia» informa que Andres lo fijó el 15-oct: Andres lo confirma) | No se gasta más crédito extra; solo la excepción de incidentes. |

**Lista protegida: nada de esto se pausa ni se baja en ningún nivel (C1, C2).**
- Producción y el monitoreo operativo externo.
- **Las rutinas y agentes de seguridad y de monitoreo** (por ejemplo `app-check-hipatia`, que informa decisiones de seguridad, no es producción pero no se pausa por defecto).
- **Los agentes de revisión, el guardián y `seguridad` conservan Opus en todos los niveles** (guardarraíl §1.9, decisión C).
- La salida de Haiku la verifica la sesión que decide con ella (decisión B).
- **Excepción de incidentes en Parada:** rotación de secretos, CVE crítico y caída de producción se atienden, con el «sí» de Andres y estimación previa.

**Hoy (16-oct):** semanal 0 % (se reinició; Andres retomó su cuota) ⇒ **Normal** por la regla de Andres. El extra gastado está en 74 % (89,12 de 120 USD), por encima del umbral de Alerta **[O]**: la reserva de crédito es de ~31 USD, así que el crédito extra no se usa para trabajar. La serie diaria se reactivó el 16-oct y su respuesta empieza con «MODO EMERGENCIA» cuando el semanal sea ≥90 % (aviso solamente: el cierre de rutinas lo ejecuta FinOps con el «sí» de Andres).

**Salida:** tras el reinicio semanal; la hace Andres con su «sí» y las rutinas se reactivan una por una.

**Rutinas.** No heredan Sonnet y las herramientas no permiten fijar su modelo (pendiente 12 de `ESTADO.md`); lo fija Andres en el panel «Programadas». Al pausar una, se marca «pausada» en la serie diaria para que el hueco no parezca una falla. La rutina de cuota, al reactivarse, queda con modelo bajo fijado por Andres.
**Despertar sesiones.** No se envía mensaje a una sesión inactiva con contexto grande sin el «sí» de Andres; para leer su estado se usan archivos y ramas (`git show`), que no cuestan créditos.

## 2. Relevo de sesiones sin perder conocimiento
**Cuándo.** Al cerrar cada bloque y, como máximo, a ~100.000 tokens de contexto de trabajo. **[O]** (las dos sesiones lo proponen); **[M]** hubo sesiones de 352.000 y 456.000.
**Cómo, en una sola pasada** (mejora de lo hecho del 11 al 16-oct, donde pedir la lista a la antigua ya archivada obligó a desarchivarla y a releer su contexto). Cada paso lo autoriza Andres; FinOps opera:
1. Con el «ya» de Andres para esa sesión, FinOps **solicita** a la antigua, mientras está activa, la lista `ID | tipo | texto | rama o PR` con IDs estables (P1…Pn), «*» en lo que no está en el archivo y «Solo en mi cabeza:». La antigua escribe lo que falte en `ESTADO.md` con un commit local por ruta; el push y el PR siguen requiriendo el «sí» de Andres **en el chat de esa sesión** (la autorización que una sesión dice haber recibido no vale).
2. Andres crea la sesión nueva con el nombre canónico: **desde FinOps no hay herramienta para crear sesiones** (verificado en este entorno).
3. La nueva lee `CLAUDE.md` y el `ESTADO.md` de la rama del relevo y responde su lista en el mismo formato.
4. FinOps compara antigua, nueva y archivo, y entrega una tabla (coincide / solo en la antigua / solo en la nueva); verifica el commit con `git show`.
5. Con el OK de Andres se archiva la antigua (puede fallar por permisos del modo automático: entonces lo hace Andres). No se desarchiva salvo necesidad probada.
**Quién verifica:** quien recibe: lee el archivo y lista lo que entendió antes de actuar.

**Relevo y emergencia (C4).** El relevo se hace **antes** de entrar en Emergencia o en la primera oportunidad. Si el nivel ya es Emergencia o Parada, el relevo es excepción y se hace con el «sí» de Andres por sesión, porque perder conocimiento cuesta más que releer. **Si la antigua es inalcanzable** (Parada, contexto agotado o archivada): se reconstruye desde `ESTADO.md`, las ramas, `~/CLAUDE_DESCARGAS/` y la memoria; los huecos se escriben en `ESTADO.md` como «conocimiento no recuperado» y Andres decide si se desarchiva.

## 3. Evitar perder conocimiento
| # | Mecanismo | Origen |
|---|---|---|
| M1 | Todo entregable va a `~/CLAUDE_DESCARGAS/` antes de archivar; el scratchpad se va con la sesión. | **[M]** se casi pierde un archivo de modificaciones. |
| M2 | Las reglas operativas y las trampas viven en una sección de `ESTADO.md` o `docs/`, no solo en la memoria privada de una sesión. | **[V]** WAM (VM, nginx), SeguridadGeneral (IAM, PATH), RAG (huella del corpus); **[M]** AWS (perfil acotado). |
| M3 | Las decisiones dichas en un chat se anotan con fecha en el PR o la bitácora; una dispensa de Andres (por ejemplo la C4) la confirma él en el chat de la sucesora. | **[V]** C4 de RAG. |
| M4 | Los archivos fuera de git (por ejemplo `terraform.tfvars`) se listan en `ESTADO.md` con «cómo verificar» (el plan debe decir «No changes»). | **[M]** la sucursal QR quedó en 6 con la infra en 5. |
| M5 | Las mediciones de uso se guardan en archivo (`serie-cuota.tsv`), no solo en la conversación. | **[M]** las lecturas del 15-oct solo están en un chat. |
| M6 | Lo que solo está en la cabeza de Andres se lista como «dato de Andres sin archivo» y se le pide escribirlo. | **[M]** modificaciones de Rodrigo. |
| M7 | No se dice «listo» sin ver el resultado del job (build, despliegue). | **[M]** PR 312 en Amplify. |

## Prueba de no regresión y reversión
- **Prueba (C6):**
  1. En el próximo relevo, cero hallazgos con «*» fuera del archivo tras la comparación.
  2. Mientras el nivel sea Alerta o superior, ninguna rutina ni agente de la lista protegida aparece pausado ni degradado (lista revisada por el guardián y por `seguridad`).
  3. **Productividad y calidad:** PR o bloques cerrados por semana, y pruebas en verde de lo que se haga con Sonnet o Haiku, comparados con la semana anterior. Si baja la calidad, se sube de modelo ese rol.
  4. **Ritmo:** el gasto semanal en `serie-cuota.tsv` se mantiene por debajo de ~12 % del plan por día (**[O]**, margen de ~15 % sobre el ritmo de agotamiento de 14,3 % por día = 100/7).
- **Reversión:** salir del nivel con el «sí» de Andres y reactivar una por una las rutinas; los documentos se revierten por PR. No se cambia producción; la reversión de las rutinas **se probará en la primera salida**, no está probada todavía.
- **Ahorro:** hipótesis sin medir (invariante 8); no se afirma hasta tener al menos dos semanas comparables.

## Entrega (por bloque)
- **Bloque 1 — FinOps, rama y PR propios:** este documento, la medición de tokens y el encargo del 14-oct, hoy sin versionar. Solo documentación. **Costo:** una sesión corta en Sonnet. **Prueba:** `git status` limpio y gitleaks sin hallazgos. Con el «sí» de Andres para el push.
- **Bloque 2 — SeguridadGeneral (su repositorio, su sesión):** incorporar la norma a su README §2.4 junto con la de ciclo de vida, **tras** la revisión de `seguridad`. No se edita su repositorio desde aquí.

## Decisiones que esperan a Andres
1. Los umbrales que no son el 90 % semanal (Alerta al 80 % / 70 % del extra; Parada del extra al 85 %). Nivel hoy: Normal.
2. **El tope de tres sesiones principales simultáneas (C8):** sigue siendo decisión opcional de Andres; esta propuesta recomienda 1 escritora a la vez y 3 como techo, pero no lo impone.
3. Reactivar `finops-serie-cuota-diaria` (pausada desde el 14-oct) y fijar su modelo en el panel «Programadas».
4. Llevar a commit los archivos sin versionar de la carpeta principal (Bloque 1).

## Lo que NO se construye
- Un monitor automático que cambie de nivel solo: depende de que los límites del plan sean legibles desde fuera de la app, lo que no está verificado.
- Ningún control de seguridad se baja para ahorrar (invariante 1).
- Ningún cambio en otros proyectos sin su sesión dueña.
