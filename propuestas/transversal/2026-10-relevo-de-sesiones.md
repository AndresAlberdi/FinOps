# Relevo y cierre de sesiones — bloque reutilizable para las sesiones dueñas

> Origen: FinOps-Ecosistema, 2026-10-11, con el OK de Andres al orden de cierre. Parte de
> `mediciones/claude/2026-10-inventario-de-sesiones.md` (53 sesiones sin archivar, 12 «cerrar con relevo»).
> **Veredicto del guardián (2026-10-11): aprobado con condiciones; esta versión las incorpora (R1 a R7).
> No se envía a ninguna sesión hasta que Andres diga «ya».**
> Regla de Andres que manda: no se pierde avance de ningún proyecto y las sesiones no se pisan.

## Para qué
Una sesión de semanas relee su contexto en cada turno y, tras varias compactaciones, trabaja con un resumen que pierde detalle. El relevo traslada el estado a archivos versionados (`ESTADO.md`, ramas, PR, ficha) y deja que una sesión nueva empiece liviana. El ahorro es una **hipótesis sin medir** (ver «Medición»).

## El bloque (se pega tal cual en cada sesión «cerrar con relevo»)

```
Pedido de Andres (2026-10-11, vía FinOps-Ecosistema): esta sesión se va a relevar para
bajar el consumo de cuota de Claude. No se pierde nada: haz lo siguiente EN ESTE ORDEN.

1. Actualiza el «Punto de retorno» de tu ESTADO.md: qué estabas haciendo, qué sigue y
   qué decisiones esperan a Andres.
2. Deja todo cambio en una rama con commit. Trabaja en TU worktree; nunca cambies de rama
   en la carpeta principal ni uses `git add -A` ni `commit -a`. Commitea solo por ruta los
   archivos que tú tocaste; lo ajeno o dudoso se lista, no se commitea. Nunca commitees
   `.env`, credenciales, archivos ignorados ni datos. El push y el PR siguen la regla de
   siempre: solo con el «sí» de Andres en tu chat; sin ese «sí» basta el commit local.
   No fusiones y no toques producción por esto. Lo que quede sin commit, lístalo con ruta
   y motivo.
3. Inventario de tus worktrees: rama, último commit, fusionada o no. No borres ninguno.
4. Actualiza tu ficha en ~/Claude-Proyectos/proyectos/ si cambió un módulo reutilizable.
5. Responde con UNA línea: «lista para relevo: rama <nombre>, PR <número o sin push>» o lo
   que falta.

No cierres ni archives tu propia sesión: lo hace Andres después de verificar el relevo.
No toques otros proyectos. Sin secretos ni identificadores completos en lo que escribas.
```

## Orden (una sesión por vez)
**Regla de colisión:** antes de relevar una sesión, confirmar que ninguna otra sesión **de la misma carpeta principal** está en marcha. Una sesión que trabaja en su propio worktree no pisa a otra y puede relevarse aunque haya una en marcha en otro worktree; las que comparten la carpeta principal (por ejemplo, NovuChat Principal y Constructora/Operadora) van de una en una y solo si no hay otra de esa carpeta en marcha.

1. **Paso 1a, archivo directo (11):** ejecuciones de rutinas ya terminadas (5), las dos «Trivy» del 1/09, las dos sesiones vacías de «Remote control», la hija con PR fusionado («Hacer determinista el test de llave equivocada AES») y la de un minuto («Sistema de Aprendizaje»). Las archiva Andres desde la barra lateral; esta sesión no archiva sesiones ajenas. **Quedan fuera las 17 ejecuciones de la rutina de Hipatia** (decisión de Andres del 2026-10-11).
2. **Paso 1b, principales inactivas más de 48 h (8):** Sitio comercial novuchat.site, Encuentrame, Onboarding genérico, FNC, Hipatia repositorio local y hardening, Cobrador contrato para consumidores, Pendientes en ManejoQRSimple y Evaluación TeCNIa. **Pasan por la misma comprobación que el paso 2**: no se archivan sin confirmar que su `ESTADO.md` está al día. «Cerrar ya» es una clasificación, no una orden.
3. **Paso 2, con comprobación previa (3):** PRETSO (entrega de octubre), Mejora Continua (PR #1 abierto) y ProyectosClaude (PR #1 cerrado sin fusionar). «Novuchat chat» se queda en **Conservar** (en uso; se confirma qué pasó con su PR cerrado, sin archivarla).
4. **Relevo, de la más antigua a la más nueva, respetando la regla de colisión:** WhatsApp Modular (52 días) → RAG-Generico (34 días, en Opus) → SeguridadGeneral → Bancard → Firma CPC → NovuChat Principal → NovuChat Constructora/Operadora → Cartera de clientes → Análisis financiero de NovuChat (en Opus) → Novuchat rearquitectura → **SeguroLoTengo Principal, al terminar lo que Andres espera** → FinOps (esta, la última). Bancard y Firma CPC esperan a que SeguroLoTengo Principal no esté en marcha o trabajan solo en su worktree.

Cuentas: 39 «cerrar ya» − 17 (Hipatia) − 3 (paso 2) − 8 (paso 1b) = 11 de archivo directo.

## Verificación del relevo (prueba de no regresión)
La sesión responde «lista para relevo: rama X, PR N o sin push». Para que la sesión nueva vea el estado actualizado, **una de dos, a elección de Andres**: (a) el PR de `ESTADO.md` se fusiona con su OK antes de archivar, o (b) la sesión nueva lee el `ESTADO.md` de esa rama local (`git show <rama>:ESTADO.md`). Con eso, la sesión nueva (que lee solo `CLAUDE.md` y `ESTADO.md`) repite los pendientes; si coinciden con lo que dijo la antigua, Andres la archiva. Si no, se corrige `ESTADO.md` desde la antigua **antes** de archivar.
**Reversión:** la sesión antigua no se borra, se archiva; desarchivarla **(verificar que la app lo permite)**, sabiendo que reanudarla vuelve a costar su contexto.

## Medición
Una lectura de cuota (`get_usage`) antes y después de cada relevo, la serie diaria (`datos/claude/serie-cuota.tsv`) y el tamaño de contexto de cada sesión **en marcha** (`get_usage` con `session_id`; las inactivas no lo informan). **Límite honesto:** con otras sesiones trabajando en paralelo, la diferencia de una sola lectura no aísla el efecto de un relevo; se mira la tendencia de la semana. No se afirma un ahorro hasta tener al menos dos semanas comparables (invariante 8).

## Costo
Cada sesión gasta una pasada corta de cierre (leer su `ESTADO.md`, commit, una línea de respuesta) y la sesión nueva paga su arranque. No es cero: se declara y se mide.

## Lo que NO se hace
- No se cierran sesiones en marcha ni las ajenas desde FinOps.
- No se borra ningún worktree ni rama.
- No se toca la rutina de Hipatia (aplazada por Andres).
