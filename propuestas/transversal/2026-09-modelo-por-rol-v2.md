# Modelo por rol v2 (Haiku + sesión base Sonnet) — versión compatibilizada

> Para la sesión de **SeguridadGeneral**. Parte de `~/Descargas/instruccion-modelos-por-rol-v2.md`
> (Andres, 2026-09-29) y la ajusta a lo verificado el 2026-09-28 desde FinOps-Ecosistema.
> Las tareas 1 a 6 de ese archivo rigen **con los cambios de este documento**; donde
> difieran, rige este.

## Correcciones al contexto de la v2

1. **La v1 no está confirmada en git en ningún proyecto.** Los 77 archivos (no 48) del
   `manifiesto.tsv`, en 14 carpetas (no 8), están aplicados solo en disco. En
   SeguridadGeneral, el worktree `.claude/worktrees/modelo-por-rol` tiene los archivos
   copiados pero **sin commit ni PR** (rama igual a `main` en `509a5a5`).
2. **Orden obligatorio:** primero cerrar la v1 en SeguridadGeneral (commit, PR y fusión,
   con el bloque `~/FinOps-Ecosistema/propuestas/transversal/2026-09-modelo-por-rol-confirmar.md`);
   **después** la v2 en rama y PR propios (`chore/modelo-por-rol-v2`). No mezclar v1 y v2 en
   el mismo PR del estándar: la v1 es la evidencia de lo aplicado el 28/09.

## Ajustes a las tareas

**Tarea 1 — sesión base en Sonnet.**
- `~/.claude/settings.json` con `"model": "sonnet"`: respaldo previo y lectura del
  archivo antes de escribir. Es configuración de usuario: se hace con el «sí» de Andres
  en el chat de esa sesión. Si el clasificador de permisos lo bloquea, se informa y se le
  pide a Andres solo la aprobación en pantalla, no que lo ejecute.
- Propagación a repositorios: además, que `bootstrap-repo.sh` escriba `"model": "sonnet"`
  en el `.claude/settings.json` **del repositorio** (versionado), para que valga en
  cualquier equipo. Verificar en la documentación oficial de Claude Code la precedencia
  entre el `settings.json` de usuario y el de proyecto, y el efecto del selector de modelo
  de la app de escritorio (verificar).

**Tarea 3 — reasignación.**
- **Nueva carpeta y manifiesto propios:** `04-claude-code/modelos-por-rol-v2/` con
  `manifiesto.tsv` cuyo hash de origen es el **sha256 del archivo v1 actual** en cada
  destino. No sobrescribir `modelos-por-rol-2026-09/` (sus fuentes y respaldos son la
  reversión y la prueba de la v1). Único cambio a `aplicar.sh`: aceptar la carpeta como
  parámetro y un filtro `--proyecto <nombre>`; conservar respaldo y detección de conflictos.
- **Criterio Haiku, por descripción y no por nombre:** pasa a `haiku` el agente que
  *produce* trabajo mecánico (escribir pruebas a partir de un plan, documentación, commits,
  inventarios, recolección de datos). **No pasa a `haiku`** el agente que *decide* si algo
  está bien (compuerta previa a fusionar, criterio de salida, «referencia de verdad»):
  como mínimo `sonnet`. Casos a mirar con cuidado: `qa-testing` (segurolotengo-demo),
  `qa` y `proyectos` (Encuentrame), `qa-integracion` (WhatsApp-Modular).
- **`recolector-costos` (FinOps-Ecosistema) → `haiku`: aceptado.** Lo aplica la sesión
  de FinOps en su propia carpeta; no incluirlo en la distribución.
- **`revisor-codigo` y `code-reviewer` a `sonnet`: requiere decisión explícita.**
  Choca con `~/FinOps-Ecosistema/docs/03-guardarrailes.md` §1.9 y con
  `04-claude-code/README.md` §2.2 (Opus para revisar). Antes de generarlo:
  a) veredicto del agente `seguridad` de SeguridadGeneral;
  b) confirmación de Andres **en el chat de esa sesión**, citando el choque;
  c) si se aprueba, queda como **excepción temporal** con fecha de revisión, en
  `sonnet` (nunca `haiku`), y con dos salvaguardas: todo PR que toque autenticación,
  reglas de acceso, IAM, dependencias, infraestructura, pagos, firma o datos personales
  pasa además por `seguridad` en `opus`; y la vuelta a `opus` se hace con la misma
  herramienta (manifiesto de reversión listo desde el primer día).
- `seguridad`, `seguridad-cumplimiento`, `devsecops`, `planificador`, `guardian-*`,
  `analista-*`: **no se tocan** (siguen en `opus`).

**Tarea 4 — `CLAUDE.md`.** Las dos líneas nuevas van en `CLAUDE.md.template` en esta rama.
En los proyectos, **una sola edición** de `CLAUDE.md` por proyecto que incluya v1 + v2 en
el mismo PR de la sesión dueña (cada edición invalida la caché de contexto).

**Tarea 6 — alcance de la ejecución.** Solo `aplicar.sh --simular` sobre todos los
proyectos (es lectura). La aplicación real en otros proyectos **no la hace
SeguridadGeneral**: cada sesión dueña corre `aplicar.sh --proyecto <suyo>` con el «sí» de
Andres y confirma v1 + v2 en un único PR (regla global: cada sesión escribe en su carpeta).

## Difusión a las sesiones (prioridad acordada)

Andres priorizó **SeguridadGeneral → segurolotengo-demo → NovuChat**; el resto queda en
pausa. SeguridadGeneral entrega, al terminar, un bloque por proyecto prioritario en
`04-claude-code/modelos-por-rol-v2/bloques/<proyecto>.md` (filas del manifiesto, pruebas,
reversión) y se lo indica a Andres con ruta completa y copia en `~/Descargas/`.

## Pruebas y medición
- Simulación: agentes a `haiku`, a `sonnet`, conflictos, sin escrituras.
- En cada proyecto: `cmp` contra la fuente v2; ningún `inherit`; ningún agente de
  seguridad o compuerta por debajo de lo fijado aquí.
- No regresión: tasa de PR con hallazgos del revisor y retrabajo, antes/después.
- FinOps mide la cuota del plan Max antes y después de v1 (28/09) y de v2 (fecha de
  fusión). Precios de Haiku: citar https://claude.com/pricing con fecha (verificar).

## Reversión
`git revert` del PR en cada proyecto; `--sesion base`: restaurar el respaldo de
`~/.claude/settings.json`. Menos de 10 minutos.

---
Revisión: sin veredicto del guardián de FinOps (se omitió para ahorrar cuota, por
pedido de Andres); lo sustituye el veredicto obligatorio del agente `seguridad` de
SeguridadGeneral sobre la tarea 3.
