# ESTADO — FinOps-Ecosistema

**Última actualización:** 2026-09-30

## Punto de retorno (leer primero al abrir una sesión)

**Contexto:** Andres consiguió créditos de Claude con la condición de consumir el equivalente a una semana en 40 horas (ventana iniciada ~2026-09-30 19:00 UTC; plan Max, cuota semanal en 4 % al iniciar; ver `mediciones/claude/2026-09-linea-base.md` §3 y §6). **Prioridad:** NovuChat, SeguroLoTengo, SeguridadGeneral, WhatsApp-Modular, Claude-Proyectos y PRETSO. Esta sesión corre en Sonnet 5.5.

**Repositorio:** `AndresAlberdi/FinOps` (GEN, público). `main` protegido por el ruleset 24272555: sin borrado ni force-push, historial lineal, PR con 1 aprobación y revisión de propietario, `compuerta-pr` obligatorio y al día, **solo squash**. Toda escritura en `main` pasa por PR; la aprobación la da `segurolotengopy` con el OK de Andres en el chat. Estándar DevSecOps v2 con el stack `solo-ci` (PR #1 fusionado, `2313d55`); desvíos en `docs/05`.

### Pendientes, por orden
1. **Exportación de facturación a BigQuery — opción B (US multirregional) decidida y en marcha (2026-10-01).** Dos cuentas de facturación abiertas: la de la cuenta principal de Google (5 proyectos ligados, **tope de 5 por cuenta alcanzado**, por eso no se pudo crear un proyecto dedicado) y la de la cuenta C (3 proyectos); la cuenta B no tiene. **Cuenta C:** proyecto `finops-ecosistema-c-4831` (dedicado, con facturación) con dataset `billing_export` en `US`; **export activado por Andres** (la cuenta de servicio `billing-export-bigquery` ya figura como propietaria del dataset; aún sin tablas). **Cuenta principal:** dataset `billing_export` en `US` creado en `novuchatstaging` (proyecto ya ligado a esa cuenta); **falta que Andres active el export** en la consola apuntando a `novuchatstaging` / `billing_export`. Se creó y se borró (`DELETE_REQUESTED`, recuperable 30 días) el proyecto `finops-ecosistema-a-4831`. Verificar en solo lectura que lleguen las tablas (el llenado inicial puede tardar hasta 5 días) y medir el costo real de Firestore por proyecto.
2. **AWS: hecho.** Rol `finops-lectura` creado el 2026-10-01 con la sesión de la raíz, por autorización expresa de Andres; la raíz ya tiene MFA y no tiene claves de acceso; su sesión se cerró. `Andres_Alberdi_1` (grupo Administradores) ya puede asumir el rol sin permisos adicionales (verificado con el simulador de IAM y con una consulta real). **Primera línea base:** `mediciones/aws/2026-09-linea-base.md` (septiembre USD 4,96; agosto en cero). A vigilar: AWS Transfer Family (se factura por hora).
3. **Palanca A (sesión principal en Sonnet):** Andres informó el 2026-10-01 que una sesión nueva en Code arranca en Sonnet. No verificado desde aquí con `get_session` (no hay una sesión creada después de su prueba que se pueda leer). Se da por confirmada por su observación; avisar a SeguridadGeneral.
4. **Firestore fuera de `us-east1`** (`mediciones/gcp/2026-09-firestore-regiones.md`): seis bases en `nam5`, dos en `us-central1`. **`nam5` y `us-east1` cuestan lo mismo** (almacenamiento 0,18 USD/GiB-mes; lecturas 0,06, escrituras 0,18, borrados 0,02 por 100 000); `us-central1` es más barato (0,15 y mitad en operaciones). Migrar de `nam5` a `us-east1` no ahorra. Medir el costo real antes de proponer nada; `pretso-prod` (vacía) es la única barata de mover y es decisión de PRETSO y de Andres.
5. **Bloque 2 (línea base):** bloqueado hasta que haya acceso de lectura a alguna facturación (pendientes 1 y 2). La de Claude ya está en curso.
6. **Fase 2b:** falta solo NovuChat. Andres informó el 2026-10-01 que responderá tras unas pruebas; Claude-Proyectos ya reportó.
7. **`CLAUDE.md` de este proyecto**, una sola edición cuando toque: dice que `recolector-costos` usa Sonnet y hoy usa Haiku.
8. ~~Rutas de los agentes~~ **hecho:** todas absolutas, hacia `/home/andres-alberdi/SeguridadGeneral` (decisión de Andres, 2026-09-30; nunca `~`).
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
