# Norma de ciclo de vida de sesiones de Claude Code — propuesta para SeguridadGeneral

> Origen: FinOps-Ecosistema, 2026-10-11. Para la sesión de **SeguridadGeneral**, dueña de
> `04-claude-code/README.md` §2.4 y de `CLAUDE.md.template`.
> **Veredicto del guardián (2026-10-11): aprobada con condiciones; esta versión incorpora S1 a S5.**
> Las decisiones A, B y C del modelo por rol no se rediscuten; este bloque cubre lo que no cubren.

## Evidencia (de `mediciones/claude/2026-10-inventario-de-sesiones.md`, 2026-10-10)
- 53 sesiones sin archivar; 14 principales con hasta 52 días de vida; 12 piden relevo.
- 24 de las 39 «cerrar ya» son **ejecuciones de rutinas o sesiones vacías**; ninguna se archiva sola.
- **Las rutinas no heredan Sonnet:** corren en Opus (esfuerzo medio) o Fable. Las herramientas de rutinas no permiten fijar su modelo (`ESTADO.md` de FinOps, pendiente 12; comprobado al crear la rutina diaria de cuota, que corrió en Opus 5.5).
- 2 principales en Opus (RAG-Generico y Análisis financiero de NovuChat) y 3 cuyo modelo cambió respecto del de arranque (Constructora/Operadora y Análisis financiero de NovuChat, y FinOps).
- Cuota semanal de Andres: 57 % a unas 46 h de iniciada la semana (lectura del 2026-10-11 06:11 UTC; la semana renueva el 16/10 08:00 UTC). **A ese ritmo se agotaría hacia el 12/10 (extrapolación, no medición).** Que las sesiones largas sean la causa **no está medido**; es la hipótesis principal, por mecanismo documentado: cada turno relee el contexto y cada `/model` lo relee sin caché (revisión externa del 29/09 §3.2, con documentación oficial).

## Cambio propuesto (README §2.4 y `CLAUDE.md.template`)
1. **Una sesión por bloque de trabajo.** Al cerrar el bloque: `ESTADO.md` al día y relevo (sesión nueva que lee solo `CLAUDE.md` y `ESTADO.md`).
2. **Se refuerza lo vigente en §2.4: no alternar `/model` dentro de una sesión.** Si hace falta otro modelo: sesión nueva o subagente con su `model` fijado. No rediscute la decisión A.
3. **Toda sesión creada por otra sesión declara su modelo y se cierra al terminar.**
4. **Toda rutina programada declara su modelo según la decisión B:** Haiku solo si otro verifica su salida; Sonnet si decide. **Las rutinas que informan decisiones de seguridad (por ejemplo, `app-check-hipatia`, que informa sobre App Check) conservan el modelo que fije el agente `seguridad`.** Si la herramienta no permite fijar el modelo, la persona lo fija en el panel de rutinas y queda anotado en el `ESTADO.md` del proyecto. Una rutina no deja sesiones sin archivar.
5. **Las coordinadoras (Claude-Proyectos, SeguridadGeneral, FinOps) se abren a demanda** y se comunican por `ESTADO.md` e `informes/`, no en vivo.
6. **Tope de tres sesiones principales simultáneas: decisión de Andres, opcional**, mientras la cuota semanal sea la restricción. Restringe la capacidad de trabajo: por eso la medición incluye los bloques o PR cerrados por semana, para detectar si la productividad baja.
7. **Inventario mensual de sesiones** (metadatos con `get_session`), a cargo de FinOps.

## Prueba de no regresión y reversión
- **Prueba:** ningún avance fuera de `ESTADO.md` o de un PR al cerrar una sesión; se verifica reabriendo desde cero.
- **Medición:** serie diaria de cuota, inventario mensual y PR cerrados por semana; no se declara ahorro con menos de dos semanas comparables.
- **Reversión:** son reglas de proceso, sin cambios de código; se retiran editando la norma. Las sesiones se archivan, no se borran.

## Controles de `docs/03` que toca
Ninguno de los de §1.1 a §1.8. La regla 4 **no baja de modelo a ningún agente de revisión o seguridad ni a ninguna rutina de seguridad** (§1.9 y decisiones B y C vigentes).

## Costo
Una edición de `README.md` y de `CLAUDE.md.template`. **Adoptar la plantilla en cada proyecto edita su `CLAUDE.md` e invalida la caché una vez por proyecto**; se hace en un solo PR por proyecto.

## Lo que NO se propone
- Cerrar sesiones por tiempo de forma automática.
- Bajar revisores o `seguridad` de Opus (decisión C vigente).
