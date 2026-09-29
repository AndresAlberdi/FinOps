# ESTADO — FinOps-Ecosistema

**Última actualización:** 2026-09-29

## Punto de retorno (leer primero al abrir una sesión)

**Prioridad decidida por Andres (2026-09-28):** concentrarse solo en **NovuChat, SeguroLoTengo (`segurolotengo-demo`) y SeguridadGeneral**, con pocos tokens. La subida a GitHub de este repositorio queda para después (Andres no espera cambios en la laptop hasta el fin de semana siguiente).

### Pendientes, en orden
1. **Confirmar en git el modelo por rol en los tres proyectos prioritarios** — bloque `propuestas/transversal/2026-09-modelo-por-rol-confirmar.md` (también en `~/Descargas/FINOPS_bloque-modelo-por-rol-confirmar_2026-09-28.md`). Andres lo pega en la sesión de cada proyecto, en este orden:
   - a. **SeguridadGeneral** primero (es la fuente del estándar; corregir el ejemplo `model: inherit` de `04-claude-code/README.md` §2.2; su agente `seguridad` revisa la lista «En sonnet, declarados»).
   - b. **segurolotengo-demo**: `docs/claude/` va en el mismo commit que `CLAUDE.md` (si se pierde, se pierde el contenido que salió de `CLAUDE.md`); no mover `PLAN_AGENTES_SEGUROLOTENGO.md`.
   - c. **NovuChat**: 15 agentes modificados + `planificador` y `revisor-codigo`; dejar fuera `Analisis/` y `Demo-Recursos/`.
   - **Riesgo mientras tanto:** los cambios están solo en disco; no usar `git checkout .`, `git clean` ni cambiar de rama en esas carpetas.
1b. **v2 (Haiku + sesión base Sonnet)** — `propuestas/transversal/2026-09-modelo-por-rol-v2.md`, enviada el 2026-09-29 a la sesión «Estatus del proyecto» de SeguridadGeneral. Pendiente: su simulación, la decisión sobre `revisor-codigo`/`code-reviewer` a sonnet (choca con `docs/03` §1.9) y pasar `recolector-costos` de FinOps a `haiku` (lo hace esta sesión, cuando SeguridadGeneral publique el criterio).
2. **Decisión de Andres:** qué es `slt-rediseno` (¿proyecto activo o copia de `segurolotengo-demo`?). Si es activo: `seguridad-cumplimiento` está en sonnet, faltan `planificador`/`revisor-codigo`, `CLAUDE.md` de 69 KB.
3. **Decisión de Andres:** qué agente `seguridad` usa esta sesión (no existe en `.claude/agents/` de FinOps; candidato: el de SeguridadGeneral).
4. **Bloque 0 de FinOps (postergado):** falta, con «sí» de Andres, `git remote add origin git@github.com:AndresAlberdi/FinOpsEcosistema.git` y *push* de `main` (el clasificador de permisos lo bloqueó; aprobarlo en pantalla). Después: rama `chore/estandar-devsecops`, `/aplicar-estandar-devsecops` modo A, ruleset, PR.
5. **Bloque 2, acotado a lo prioritario:** línea base de Claude (créditos de uso antes y después del 28/09) para medir la palanca de modelo por rol. Nota: Opus 5.5 y Sonnet 5 cobran igual la lectura de caché (USD 0,20/M; claude.com/pricing, 2026-09-28): no esperar −50 % del total.
6. Resto del ecosistema (otros 11 proyectos del bloque de cierre, Bloques 1, 3 y 4): en pausa por decisión de prioridad.

## Hecho
- 2026-09-28 · Proyecto creado: `CLAUDE.md`, `docs/00` a `docs/04`, `Prompts/arranque.md`, agentes `recolector-costos`, `analista-finops` y `guardian-calidad-seguridad`.
- 2026-09-28 · Primera palanca, previa al proyecto: asignación de modelo por rol en los subagentes de Claude Code y `CLAUDE.md` estables (detalle en `~/SeguridadGeneral/04-claude-code/README.md` §2.2 y §2.4). Falta su medición (Bloque 2).
- 2026-09-28 · Verificación de esa palanca: los 77 archivos del manifiesto (`~/SeguridadGeneral/04-claude-code/modelos-por-rol-2026-09/`) están aplicados en disco en 14 carpetas, idénticos, pero **sin confirmar en git en ningún proyecto**. Bloque de cierre con veredicto del guardián (aprobada con condiciones, incorporadas).
- 2026-09-28 · Repositorio remoto creado por Andres: `AndresAlberdi/FinOpsEcosistema` (cuenta GEN), público (modo A), colaborador `segurolotengopy`, aún vacío.
- 2026-09-28 · Bloque 0 parcial: identidad GEN verificada (`gh`, `user.email` y llave SSH = `AndresAlberdi`); `git init -b main` y primer commit local; `gitleaks` sin hallazgos. Sin remoto ni *push*.

## Queda abierto
- Visibilidad: pública por ahora (modo A). El diseño ya excluye datos e identificadores del repositorio.
