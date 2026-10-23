# Política de disco y de worktrees de sesiones — propuesta

> Origen: FinOps-Ecosistema, 2026-10-23, por pedido de Andres, a partir del informe de la sesión «SeguroLoTengo Sesion Principal» (`~/CLAUDE_DESCARGAS/SeguroLoTengo_informe-disco-y-worktrees_2026-10-23.md`, medido por esa sesión) y de lecturas de FinOps en solo lectura el mismo día.
> Estado: **borrador sin revisar**. Antes de entregarla a SeguridadGeneral pasa por `guardian-calidad-seguridad` y por `seguridad` (toca borrado de datos de trabajo y la política de sesiones). Marcas: **[M]** medido; **[O]** opinión de FinOps.

## Evidencia
- **[M]** El disco `/` de la laptop (468 GB) llegó al **98 %** (9,5 GB libres). `segurolotengo-demo/.claude` pesaba ≈163 GB, todo en **159 worktrees** de git (1,8 a 4,1 GB cada uno, por `node_modules` y `.next`).
- **[M]** La app administra 33 de esos worktrees (31 GB) de 11 proyectos; el resto lo crean sesiones y agentes (86 `agent-*` terminados) y nadie los limpia.
- **[M]** Se borraron 111 worktrees limpios con rama ya en `main` (111,8 GB), sin `--force` y sin borrar ramas: 98 % → 74 % (116 GB libres). Lectura de FinOps del 23-oct: 48 worktrees en ese repo y 20 GB en `~/NovuChat/.claude/worktrees`. Quedan 27 (≈28 GB) que decide Andres: 11 con cambios y 16 con ramas sin fusionar.
- **[M]** Con el disco lleno fallan pruebas con `EDQUOT` y, con `/tmp` en memoria, los comandos que escriben mucho (sesiones de Constructora y Cartera lo reportaron).
- **[O]** El costo no es dinero sino riesgo operativo: sin espacio se corrompen commits locales no publicados y se pierden respaldos.

## Propuesta
1. **Alerta de disco al 80 % y al 90 %** de `/` (aviso, no corte). La da la serie diaria de cuota al empezar la jornada, y como depende de la laptop se declara como **aviso**, no monitoreo operativo (política general del 11/10/2026).
2. **Cada agente o sesión borra SU worktree al terminar**, solo si: el árbol está limpio, la rama está empujada o ya fusionada, nunca con `--force`, y nunca se borra la rama. Si hay cambios o commits sin publicar, avisa y no borra.
3. **Ningún worktree se borra sin dueño:** el de otra sesión (por ejemplo `rroca-sinpanel` con el respaldo de Rubén) solo lo borra su dueña, con el «sí» de Andres.
4. **Limpieza periódica de lo terminado:** usar «Settings › Storage › Clean up inactive sessions» de la app, con el script de limpieza segura de SeguroLoTengo como referencia (ensayo por defecto, `--ejecutar` explícito, sin `--force`, registro de lo borrado).
5. **Evaluar una caché compartida de `node_modules`** (por ejemplo almacén común de pnpm) para no repetir 1 a 2 GB por rama. [O], sin medir el ahorro: se mide en un proyecto antes de adoptarla.
6. **Los traspasos de relevo** registran qué worktrees quedan vivos y por qué, para que archivar una sesión no borre sin querer lo que otra necesita.

## Prueba de no regresión y reversión
- **Prueba:** tras aplicar (2) y (4), el disco se mantiene por debajo del 80 %; **no se pierde ningún commit sin publicar** (comprobación por sesión: `git rev-list --count origin/main..<rama>` y rama remota antes de borrar); ninguna rama se borra.
- **Reversión:** los worktrees borrados se recrean con `git worktree add` desde su rama; la política se revierte por PR. No cambia producción.
- **Ahorro:** disco liberado medido (111,8 GB el 23-oct); no hay ahorro en dinero.

## Lo que NO se propone
- Borrar ramas ni usar `--force`.
- Limpiar `~/Descargas` ni `~/CLAUDE_DESCARGAS` (archivos de Andres y entregables).
- Un monitor automático que borre solo.

## Entrega
- Bloque 2 — SeguridadGeneral (su repositorio, su sesión): incorporar las reglas 2 a 4 y 6 a su estándar de sesiones (§2.4), tras la revisión de `seguridad`. No se edita su repositorio desde aquí.

## Decisiones que esperan a Andres
1. Los umbrales de alerta de disco (80 % y 90 %).
2. Qué hacer con los 27 worktrees restantes de SeguroLoTengo y con los 20 GB de NovuChat.
3. Si se evalúa la caché compartida de `node_modules`.
