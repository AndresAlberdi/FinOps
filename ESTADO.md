# ESTADO — FinOps-Ecosistema

**Última actualización:** 2026-10-02

## Punto de retorno (leer primero al abrir una sesión)

**Contexto:** Andres consiguió créditos de Claude con la condición de consumir el equivalente a una semana en 40 horas (ventana iniciada ~2026-09-30 19:00 UTC; plan Max, cuota semanal en 4 % al iniciar; ver `mediciones/claude/2026-09-linea-base.md` §3 y §6). **Prioridad:** NovuChat, SeguroLoTengo, SeguridadGeneral, WhatsApp-Modular, Claude-Proyectos y PRETSO. Esta sesión corre en Sonnet 5.5.

**Repositorio:** `AndresAlberdi/FinOps` (GEN, público). `main` protegido por el ruleset 24272555: sin borrado ni force-push, historial lineal, PR con 1 aprobación y revisión de propietario, `compuerta-pr` obligatorio y al día, **solo squash**. Toda escritura en `main` pasa por PR; la aprobación la da `segurolotengopy` con el OK de Andres en el chat. Estándar DevSecOps v2 con el stack `solo-ci` (PR #1 fusionado, `2313d55`); desvíos en `docs/05`.

### Pendientes, por orden
1. **Exportación de facturación a BigQuery — opción B (US multirregional), funcionando en las dos cuentas con facturación; los datos son PROVISIONALES (2026-10-01).** Las dos tablas existen, pero el **llenado inicial sigue en curso (hasta 5 días)**: la cuenta C llega al 10/09 y la principal al 06/09. **Error mío corregido:** el PR #9 decía que Gemini «se detuvo el 5/09»; era un artefacto de datos incompletos (ya suma 1,16 USD hasta el 10/09 y sigue creciendo). **Releer a partir del 2026-10-06** (`SELECT MAX(DATE(usage_start_time)), MAX(export_time)`), confirmar septiembre completo y recién entonces fijar la línea base de Google (`mediciones/gcp/2026-09-linea-base-cuenta-c.md` y `…-cuenta-principal.md`). La cuenta principal está **cubierta por créditos** (neto ≈ 0 en lo leído): falta el desglose y su vencimiento. Cuenta C: proyecto dedicado `finops-ecosistema-c-4831`; principal: dataset en `novuchatstaging`.
2. **AWS: hecho.** Rol `finops-lectura` creado el 2026-10-01 con la sesión de la raíz, por autorización expresa de Andres; la raíz ya tiene MFA y no tiene claves de acceso; su sesión se cerró. `Andres_Alberdi_1` (grupo Administradores) ya puede asumir el rol sin permisos adicionales (verificado con el simulador de IAM y con una consulta real). **Primera línea base:** `mediciones/aws/2026-09-linea-base.md` (septiembre USD 4,96; agosto en cero). A vigilar: AWS Transfer Family (se factura por hora).
3. **Palanca A (sesión principal en Sonnet):** Andres informó el 2026-10-01 que una sesión nueva en Code arranca en Sonnet. No verificado desde aquí con `get_session` (no hay una sesión creada después de su prueba que se pueda leer). Se da por confirmada por su observación; avisar a SeguridadGeneral.
4. **Firestore fuera de `us-east1`** (`mediciones/gcp/2026-09-firestore-regiones.md`): seis bases en `nam5`, dos en `us-central1`. **`nam5` y `us-east1` cuestan lo mismo** (almacenamiento 0,18 USD/GiB-mes; lecturas 0,06, escrituras 0,18, borrados 0,02 por 100 000); `us-central1` es más barato (0,15 y mitad en operaciones). Migrar de `nam5` a `us-east1` no ahorra. Medir el costo real antes de proponer nada; `pretso-prod` (vacía) es la única barata de mover y es decisión de PRETSO y de Andres.
5. **Bloque 2 (línea base):** en curso. Hecho: Claude (cuota), AWS (septiembre 4,96 USD), Google (provisional hasta el 6/10), Meta (0,06 USD), GitHub (**USD 4,00 al mes** fijos, el plan Pro de `segurolotengopy`; Actions facturable USD 0; ambas cuentas con presupuesto de Actions en USD 0 y «detener el uso» activado: **si se agotan los 3.000 minutos incluidos, el CI privado se bloquea**; recomendado subir a ~USD 10, decide Andres; verificado con las pantallas de Facturación) y **OCI (USD 0,00 en agosto y septiembre, medido con la CLI)** (`mediciones/oci/2026-09-linea-base.md`): cómputo al 96–99 % de lo gratuito; el hallazgo H-13 de «150 GB de bloque» **no existe**; el bucket de respaldos tiene 3,25 GiB y **la retención de 14 días no se aplica** (el respaldo diario creció de 183 a 326 MiB en 4 días, 80 % la base de datos de n8n; el tope gratuito de 20 GB se alcanzaría hacia mediados de noviembre, centavos); **memoria de la VM al 21,5 %: a 1,5 puntos de la condición de recuperación por inactividad de Oracle** (limpiar la VM podría empeorar ese riesgo). Falta: n8n (corre en esa misma VM, sin costo propio) y el cierre exacto de GitHub (Andres, Facturación y planes → Uso).
6. **Fase 2b: cerrada.** Las seis sesiones reportaron; NovuChat el 2026-10-01 (`informes/2026-09-29.md` completo).
6b. **Gemini prepago (verificar tras el llenado):** NovuChat informa crédito prepago agotado el 29/09 y repuesto el 30/09 en `NovuchatDemo` (cuenta C). **Hipótesis aún sin base:** que el export oculte ese consumo. La tabla está incompleta (llega al 10/09), así que antes hay que esperar al 06/10; después, comparar con el saldo y uso de Google AI Studio (pantalla que solo Andres ve).
7. **`CLAUDE.md` de este proyecto**, una sola edición cuando toque: dice que `recolector-costos` usa Sonnet y hoy usa Haiku.
8. ~~Rutas de los agentes~~ **hecho:** todas absolutas, hacia `/home/andres-alberdi/SeguridadGeneral` (decisión de Andres, 2026-09-30; nunca `~`).
9. Borrar o conservar `AndresAlberdi/FinOpsEcosistema` (vacío): decisión de Andres.
10. Bloques 1 (políticas por otorgar), 3 y 4: tras tener línea base.
11. **Control de costos por negocio (requisito de Andres, 2026-10-02):** PRETSO, Hipatia, NovuChat y SeguroLoTengo llevan su propio control. Plan en `docs/06-costos-por-negocio.md` (un FinOps central con vista por negocio; costo directo «medido» y compartido «asignado»). **Hallazgo:** PRETSO (cuenta de facturación …5B3F) e Hipatia (…44F7) facturan por cuentas que no se exportan hoy ni lista la identidad de lectura; falta saber a qué cuenta de Google pertenecen y activar su export. Mapa v0.3 (2026-10-02): lo «por asignar» resuelto con los valores por defecto de Andres (quinto negocio «AAB1 / WhatsApp-Modular», Encuéntrame.BO y ManejoQRSimple propios, categoría «Comunes»); de 28 proyectos de Google solo 9 facturan. Falta: reglas de asignación (§4), la cuenta de Google de …5B3F y …44F7, dueño de `OnboardingGenerico` y de la WABA …1573, costo de Lovable, Snyk y del dominio `hipatiabo.com`. Siguiente paso mío: cortar las líneas base por negocio.

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
