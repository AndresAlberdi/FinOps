# ESTADO — FinOps-Ecosistema

**Última actualización:** 2026-09-30

## Punto de retorno (leer primero al abrir una sesión)

**Contexto:** Andres consiguió créditos de Claude con la condición de consumir el equivalente a una semana en 40 horas (ventana iniciada ~2026-09-30 19:00 UTC; plan Max, cuota semanal en 4 % al iniciar; ver `mediciones/claude/2026-09-linea-base.md` §3 y §6). **Prioridad:** NovuChat, SeguroLoTengo, SeguridadGeneral, WhatsApp-Modular, Claude-Proyectos y PRETSO. Esta sesión corre en Sonnet 5.5.

**Repositorio:** `AndresAlberdi/FinOps` (GEN, público). `main` protegido por el ruleset 24272555: sin borrado ni force-push, historial lineal, PR con 1 aprobación y revisión de propietario, `compuerta-pr` obligatorio y al día, **solo squash**. Toda escritura en `main` pasa por PR; la aprobación la da `segurolotengopy` con el OK de Andres en el chat. Estándar DevSecOps v2 con el stack `solo-ci` (PR #1 fusionado, `2313d55`); desvíos en `docs/05`.

### Pendientes, por orden
1. **Decisión de Andres — exportación de facturación a BigQuery (las tres cuentas de Google).** Preferencia: `us-east1`, sin multirregional. Un dataset regional **no trae datos de meses anteriores**; uno multirregional `US` trae desde el inicio del mes anterior (`docs/04` §2.2). Opción A: regional `us-east1` ya + CSV manual de los dos últimos ciclos desde la consola. Opción B: `US` multirregional con retroactivo automático. Verificar que `us-east1` figure entre las ubicaciones regionales admitidas. Falta además el proyecto anfitrión: se propone reutilizar uno existente por cuenta. Nada se ha creado en ninguna nube desde esta sesión.
2. **Rol de solo lectura en AWS** (`docs/04` §2.1): una línea, cuando Andres decida.
3. **Prueba de la palanca A** (sesión principal en Sonnet): Andres abre una sesión nueva desde el botón de la app, sin escribir `/model`; se lee su `model` con `get_session`. Sin confirmar (`mediciones/claude/2026-09-linea-base.md` §5). Avisar el resultado a SeguridadGeneral (su PR #41 ya la deja como «verificar»).
4. **Firestore fuera de `us-east1`** (`mediciones/gcp/2026-09-firestore-regiones.md`): seis bases en `nam5` (multirregional), dos en `us-central1`. No migrar por precio de lista: medir el costo real con la exportación y solo entonces proponer. La única barata de mover es `pretso-prod` (vacía), y es decisión de la sesión de PRETSO y de Andres.
5. **Bloque 2 (línea base):** bloqueado hasta que haya acceso de lectura a alguna facturación (pendientes 1 y 2). La de Claude ya está en curso.
6. **Fase 2b:** NovuChat y Claude-Proyectos no escribieron su sección «Coordinación 2026-09-29» (`informes/2026-09-29.md`). Pedirles que la escriban.
7. **`CLAUDE.md` de este proyecto**, una sola edición cuando toque: dice que `recolector-costos` usa Sonnet y hoy usa Haiku.
8. **Rutas al estándar en los agentes** (`~/SeguridadGeneral` hoy): si Andres prefiere la absoluta, por robustez con la herramienta Read, cambiarla (el repositorio es público; solo revela un nombre de usuario).
9. Borrar o conservar `AndresAlberdi/FinOpsEcosistema` (vacío): decisión de Andres.
10. Bloques 1 (políticas por otorgar), 3 y 4: tras tener línea base.

### Coordinación 2026-09-29 (formato de la orden general)
- Fase 0: hecha — `main` en `AndresAlberdi/FinOps`.
- Fase 1: hecha — agentes sin `WebFetch`; `recolector-costos` en `haiku`; PR #1 (estándar) fusionado.
- Fase 2: 2a en curso (línea base de cuota); 2b consolidada en parte (`informes/2026-09-29.md`).
- Requiere a Andres: ver los pendientes 1 a 3 y 9.
- Costo: sesión en Opus 5.5 hasta el 2026-09-29 y en Sonnet 5.5 desde entonces por `/model`; sin consultas pagas.

## Hecho
- 2026-09-28 · Proyecto creado: `CLAUDE.md`, `docs/00` a `docs/04`, `Prompts/arranque.md`, agentes `recolector-costos`, `analista-finops` y `guardian-calidad-seguridad`.
- 2026-09-28 · Primera palanca, previa al proyecto: asignación de modelo por rol en los subagentes de Claude Code y `CLAUDE.md` estables (detalle en `~/SeguridadGeneral/04-claude-code/README.md` §2.2 y §2.4). Falta su medición (Bloque 2).
- 2026-09-28 · Verificación de esa palanca: los 77 archivos del manifiesto (`~/SeguridadGeneral/04-claude-code/modelos-por-rol-2026-09/`) están aplicados en disco en 14 carpetas, idénticos, pero **sin confirmar en git en ningún proyecto**. Bloque de cierre con veredicto del guardián (aprobada con condiciones, incorporadas).
- 2026-09-28 · Repositorio remoto creado por Andres: `AndresAlberdi/FinOpsEcosistema` (cuenta GEN), público (modo A), colaborador `segurolotengopy`, aún vacío.
- 2026-09-28 · Bloque 0 parcial: identidad GEN verificada (`gh`, `user.email` y llave SSH = `AndresAlberdi`); `git init -b main` y primer commit local; `gitleaks` sin hallazgos. Sin remoto ni *push*.

## Queda abierto
- Visibilidad: pública por ahora (modo A). El diseño ya excluye datos e identificadores del repositorio.
