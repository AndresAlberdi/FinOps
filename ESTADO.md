# ESTADO — FinOps-Ecosistema

**Última actualización:** 2026-09-30

## Punto de retorno (leer primero al abrir una sesión)

**Contexto:** Andres consiguió créditos de Claude con la condición de consumir el equivalente a una semana en 40 horas (ventana iniciada ~2026-09-30 19:00 UTC; plan Max, cuota semanal en 4 % al iniciar; ver `mediciones/claude/2026-09-linea-base.md` §3 y §6). **Prioridad:** NovuChat, SeguroLoTengo, SeguridadGeneral, WhatsApp-Modular, Claude-Proyectos y PRETSO. Esta sesión corre en Sonnet 5.5.

**Repositorio:** `AndresAlberdi/FinOps` (GEN, público). `main` protegido por el ruleset 24272555: sin borrado ni force-push, historial lineal, PR con 1 aprobación y revisión de propietario, `compuerta-pr` obligatorio y al día, **solo squash**. Toda escritura en `main` pasa por PR; la aprobación la da `segurolotengopy` con el OK de Andres en el chat. Estándar DevSecOps v2 con el stack `solo-ci` (PR #1 fusionado, `2313d55`); desvíos en `docs/05`.

### Pendientes, por orden
1. **Exportación de facturación a BigQuery — opción B (US multirregional), funcionando en la cuenta C; la principal conectada y esperando su primera tabla (2026-10-01).** **Cuenta C:** proyecto dedicado `finops-ecosistema-c-4831`, tabla de exportación ya creada; **primera línea base real en `mediciones/gcp/2026-09-linea-base-cuenta-c.md`** (septiembre USD 0,53, casi todo Gemini en `novuchatdemo`, detenido el 5/09). **Cuenta principal:** dataset `billing_export` en `novuchatstaging` (el tope de 5 proyectos por cuenta de facturación impidió uno dedicado); export «Costo de uso estándar» habilitado (captura de Andres) y cuenta de servicio de exportación ya propietaria del dataset; **falta su primera tabla** (actualización diaria). Verificar en solo lectura y consolidar Google con las dos cuentas. Cuenta B (NovuChat): sin facturación. FOCUS no se activa (innecesario).
2. **AWS: hecho.** Rol `finops-lectura` creado el 2026-10-01 con la sesión de la raíz, por autorización expresa de Andres; la raíz ya tiene MFA y no tiene claves de acceso; su sesión se cerró. `Andres_Alberdi_1` (grupo Administradores) ya puede asumir el rol sin permisos adicionales (verificado con el simulador de IAM y con una consulta real). **Primera línea base:** `mediciones/aws/2026-09-linea-base.md` (septiembre USD 4,96; agosto en cero). A vigilar: AWS Transfer Family (se factura por hora).
3. **Palanca A (sesión principal en Sonnet):** Andres informó el 2026-10-01 que una sesión nueva en Code arranca en Sonnet. No verificado desde aquí con `get_session` (no hay una sesión creada después de su prueba que se pueda leer). Se da por confirmada por su observación; avisar a SeguridadGeneral.
4. **Firestore fuera de `us-east1`** (`mediciones/gcp/2026-09-firestore-regiones.md`): seis bases en `nam5`, dos en `us-central1`. **`nam5` y `us-east1` cuestan lo mismo** (almacenamiento 0,18 USD/GiB-mes; lecturas 0,06, escrituras 0,18, borrados 0,02 por 100 000); `us-central1` es más barato (0,15 y mitad en operaciones). Migrar de `nam5` a `us-east1` no ahorra. Medir el costo real antes de proponer nada; `pretso-prod` (vacía) es la única barata de mover y es decisión de PRETSO y de Andres.
5. **Bloque 2 (línea base):** en curso. Hecho: Claude (cuota), AWS (`mediciones/aws/`) y Google cuenta C. **Meta WhatsApp: empezado** (`mediciones/meta/2026-10-plan-linea-base.md`): desde el 1/10/2026 los mensajes de servicio se cobran, así que no hay línea base previa y octubre es el primer mes medible; script y pruebas listos; **falta el token de solo lectura (usuario de sistema de Meta, lo crea Andres) y los IDs de las WABA** (NovuChat respondió: una compartida con WhatsApp-Modular, una propia, una de Bellido en el portafolio de su doctor —que el token **no** verá sin su acceso— y una de demo; el pricing del webhook no se guarda, así que `pricing_analytics` es la única fuente y el único control de gasto, porque Meta no ofrece alerta para Cloud API). Falta: Google cuenta principal (esperando tabla), OCI, n8n y GitHub (sin acceso, `docs/04` §2.3).
6. **Fase 2b: cerrada.** Las seis sesiones reportaron; NovuChat el 2026-10-01 (`informes/2026-09-29.md` completo).
6b. **Posible hueco de costo de Gemini (verificar):** NovuChat informa que la credencial de producción es el proyecto `NovuchatDemo` (cuenta C) con crédito **prepago**, que se agotó el 29/09 (error 402) hasta que Andres compró créditos el 30/09. El export de facturación de la cuenta C solo muestra 0,53 USD de Gemini hasta el 5/09: **el consumo prepago puede no aparecer en el export**. Comparar con el saldo y el uso en Google AI Studio (pantalla que solo Andres ve) antes de dar por buena la línea base de Gemini.
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
