# Modelo por rol — confirmar en git lo ya aplicado

> **<PROYECTO>:** la carpeta sobre la que se trabaja. Andres pega este bloque en
> la sesión de ese proyecto. Lo propio de cada proyecto está en la tabla de
> §«Qué cambió en cada proyecto»; nada del bloque depende de un proyecto en
> particular.

Eres la sesión de `<PROYECTO>`. El 2026-09-28, el script
`~/SeguridadGeneral/04-claude-code/modelos-por-rol-2026-09/aplicar.sh` fijó el
campo `model` de cada subagente por su rol (**Opus** para planificar, revisar y
seguridad; **Sonnet** para ejecutar), agregó `planificador`, `implementador` y
`revisor-codigo` donde faltaban y añadió a `CLAUDE.md` la sección «Delegación
entre agentes y costo». Los 77 archivos están aplicados en disco, idénticos al
manifiesto (verificado el 2026-09-28 desde FinOps-Ecosistema), pero **ningún
proyecto los confirmó en git**: un `git checkout .`, un `git clean` o un cambio
de rama los pierde, y la rama principal en GitHub no los tiene. Este bloque los
confirma. No se rediscute la asignación: la regla está en
`~/SeguridadGeneral/04-claude-code/README.md` §2.2 y §2.4.

Lee primero: `CLAUDE.md`, `ESTADO.md` (o la bitácora del proyecto) y
`git status --porcelain -- .claude CLAUDE.md docs`.

## Las decisiones que no se tocan
1. `opus` para `planificador`, `revisor-codigo`, `seguridad`, `devsecops` y los
   agentes de revisión o seguridad del proyecto; `sonnet` para `implementador`,
   `deploy`, `proyectos` y los agentes de dominio que codifican. Nunca `inherit`.
2. `CLAUDE.md` es estable: solo invariantes; estado y pendientes fuera de él.
3. Este bloque **no cambia el contenido** de ningún agente: solo confirma lo
   aplicado. Si un archivo difiere del manifiesto, se detiene y se informa.

## Cómo trabajar
- Worktree y rama propios `chore/modelo-por-rol`, desde la rama base que indica
  la tabla (por defecto `main`; `master` en Claude-Proyectos). Nunca cambiar de
  rama en la carpeta principal ni `git add -A`.
- Copiar a la rama **solo** los archivos de la tabla (columna «Qué va en el
  commit»), desde la carpeta principal, y `git add` cada uno por nombre. Los
  demás cambios sin confirmar son de otros frentes: no se tocan.
- Antes de confirmar `CLAUDE.md`, leer su diff: debe contener solo las filas de
  agentes, la sección «Delegación entre agentes y costo» y la reubicación que
  indique la tabla. Todo archivo al que el `CLAUDE.md` nuevo apunte debe existir
  en el commit. Si trae cambios de otro frente, separarlos y dejarlos fuera.
- Andres autoriza; tú operas. *Push* y PR solo con su «sí» en el chat.
- Conventional Commits: `chore(claude): fijar modelo por rol en subagentes`.

## Bloque único — confirmar y abrir PR (≈ 15 min)
**Prueba (antes del commit, en la rama):**
1. Cada agente del manifiesto es idéntico a su fuente:
   `cmp ~/SeguridadGeneral/04-claude-code/modelos-por-rol-2026-09/<PROYECTO>/<archivo> .claude/agents/<archivo>`
   para cada fila de `manifiesto.tsv` del proyecto → sin diferencias.
2. `grep -l '^model: *inherit' .claude/agents/*.md` → vacío.
3. Todo archivo de `.claude/agents/` con encabezado YAML tiene `model:`
   (los documentos sin encabezado, como `PLAN_AGENTES_*.md`, no son agentes).
4. Los agentes de la columna «Deben estar en opus» lo están; los de la columna
   «En sonnet, declarados» siguen igual (no se tocan en este bloque).
5. Referencias: cada ruta nueva que cite `CLAUDE.md` existe en el commit.
6. `CLAUDE.md` < 30 KB.
7. CI requerido de la rama base en verde (`compuerta-pr` donde exista: Firmas,
   Hipatia, NovuChat, Novuchat-site, PRETSO). Donde no exista, `gitleaks`
   local sobre la rama, y decirlo en la descripción del PR.

**Reversión:** `git revert` del commit (menos de 5 minutos). Los respaldos de
`modelos-por-rol-2026-09/respaldo-*/` solo devuelven los agentes modificados:
no borran los nuevos ni revierten `CLAUDE.md`, y son locales.

**Costo:** solo tokens de la sesión; cero consultas pagas. El ahorro lo mide
FinOps-Ecosistema en su Bloque 2 (créditos de uso antes y después del 28/09).
Opus 5.5 cuesta USD 4/20 y Sonnet 5 USD 2/10 por millón de tokens de entrada y
salida, pero la lectura de caché cuesta lo mismo en ambos (USD 0,20): el ahorro
está en la entrada no cacheada y la salida, no en el total
(https://claude.com/pricing, consultado el 2026-09-28).

## Qué cambió en cada proyecto

| Proyecto | Rama base | Qué va en el commit | Deben estar en opus | En sonnet, declarados | Particularidad |
|---|---|---|---|---|---|
| **SeguridadGeneral** | `main` | `.claude/` y `CLAUDE.md` (nunca versionados); `04-claude-code/README.md`, `CLAUDE.md.template`, `agents/*.md` (7), `agentes-globales/`, `modelos-por-rol-2026-09/` (sin `respaldo-*`, ya ignorado) | `planificador`, `revisor-codigo` | — | **Va primero:** es la fuente del estándar. Corregir en el mismo PR el ejemplo `model: inherit` de `README.md` §2.2 (línea 40), que contradice su tabla. `01-seguridad/10-inventario…` y `CATALOGO…` son de otro frente. Pasar por su agente `seguridad` la lista de «En sonnet, declarados» de toda esta tabla y las herramientas de `planificador` (`Bash`, `WebFetch`, `WebSearch`). |
| Claude-Proyectos | `master` | `.claude/` y `CLAUDE.md` (nunca versionados) | `planificador`, `revisor-codigo` | — | `LEEME.md` y las fichas modificadas son de otro frente. |
| AAB1_EMPRESA | `main` | `operaciones`, `implementador`, `revisor-codigo`, `CLAUDE.md`, **`docs/tarifas-modelos.md`** y el fragmento de **`ESTADO.md`** que recibió lo quitado de `CLAUDE.md` | `revisor-codigo` y los que ya lo estén | `operaciones` (codifica en su dominio; lo revisa `revisor-codigo`) | `CLAUDE.md` perdió 24 líneas: van a `docs/tarifas-modelos.md` y a `ESTADO.md`, ambos sin confirmar, y deben entrar en el mismo commit. `CLAUDE.md` nuevo cita `SESIONES/` (sin versionar): no confirmarla; quitar la mención o preguntar a Andres qué es. |
| ChatBotRAG | **`chore/estandar-devsecops`** (rama hija) | `deploy`, `devsecops`, `seguridad`, `implementador`, `planificador`, `revisor-codigo`, `CLAUDE.md` | `planificador`, `revisor-codigo`, `seguridad`, `devsecops` | `proyectos` (acta y estado; no decide) | En `main` no existen ni `CLAUDE.md` ni `.claude/`: viven en `chore/estandar-devsecops`. **No partir de `main`**: arrastraría medio estándar y chocaría con su PR. Confirmar en una rama hija y fusionar después del estándar, o esperar a que este se fusione. |
| Encuentrame.BO/encuentrame.bo | `main` | `ia`, `README`, `revisor-codigo`, `CLAUDE.md` | `revisor-codigo` y los que ya lo estén | `ia`, `qa`, `api`, `proyectos` | La carpeta principal está en `fix/appcheck-excluir-health`: rama nueva desde `main`. **Pendiente fuera de este bloque:** `proyectos` («planificar una fase, revisar si algo está terminado») y `qa` (previo a fusionar) están en sonnet desde antes; lo decide su sesión con SeguridadGeneral (pasar a opus o separar la parte de evaluación). |
| Firmas-NoCualificadas | `main` | `deploy`, `devsecops`, `seguridad`, `implementador`, `planificador`, `revisor-codigo`, `CLAUDE.md` | `planificador`, `revisor-codigo`, `seguridad`, `devsecops` | `proyectos` | `CLAUDE.md` en 28 KB, cerca del límite. |
| Hipatia | `main` | ídem Firmas | ídem Firmas | `proyectos` | La carpeta principal está en `docs/cierre-fase-4`: rama nueva desde `main` (no difiere en `.claude/` ni en `CLAUDE.md`). |
| ManejoQRSimple | `main` | `backend-dev`, `code-reviewer`, `scraper-yape`, `test-engineer`, `CLAUDE.md` | `code-reviewer` | `test-engineer` (antes `inherit`), `scraper-yape` (antes opus; codifica) | — |
| NovuChat | `main` | los 15 agentes modificados, `planificador`, `revisor-codigo`, `CLAUDE.md` | `planificador`, `revisor-codigo`, `seguridad`, `devsecops`, `analista-de-solicitudes` y los que ya lo estén | `proyectos` si existe, y los de dominio | `Analisis/` y `Demo-Recursos/` sin confirmar son de otro frente. |
| Novuchat-site | `main` | ídem Firmas | ídem Firmas | `proyectos` | — |
| PRETSO | `main` | ídem Firmas | ídem Firmas | `proyectos` | — |
| segurolotengo-demo | `main` | `seguridad-cumplimiento`, `planificador`, `revisor-codigo`, `CLAUDE.md` y **`docs/claude/`** completo | `planificador`, `revisor-codigo`, `seguridad-cumplimiento` | los seis de dominio | `CLAUDE.md` bajó de 88 a 27,6 KB: el detalle pasó a `docs/claude/` (sin versionar), que **debe ir en el mismo commit**. **No mover** `PLAN_AGENTES_SEGUROLOTENGO.md`: `qa-testing.md` lo cita por nombre. |
| WhatsApp-Modular | `main` | los 8 agentes, `CLAUDE.md` | `code-reviewer` y los que ya lo estén | `test-engineer`, `qa-integracion`, `cost-analyst` (antes `inherit`), `meta-api-expert` (antes opus; codifica) | — |
| FinOps-Ecosistema | — | — | — | — | Se confirma en su propio Bloque 0. |

«Y los que ya lo estén»: los agentes que el manifiesto dejó en `opus`; la
prueba 1 lo garantiza sin enumerarlos.

## Lo que NO entra en este bloque (y por qué)
- **slt-rediseno** no estuvo en el manifiesto y no es repositorio git: su agente
  `seguridad-cumplimiento` quedó en `sonnet` (contradice
  `~/SeguridadGeneral/04-claude-code/README.md` §2.2), no tiene `planificador`
  ni `revisor-codigo`, y su `CLAUDE.md` pesa 69 KB. Andres decide primero si es
  un proyecto activo o una copia de `segurolotengo-demo`.
- Cambiar el modelo de los agentes marcados «En sonnet, declarados»: es una
  decisión de contenido, no de confirmación; va a SeguridadGeneral.
- Proyectos sin agentes propios (claude-tooling-radar, FacturadorSIAT, n8n-oci,
  Onboarding-Generico, RAG-Generico): usan los globales de `~/.claude/agents/`,
  ya con modelo por rol.

## Entregables al cerrar
- PR `chore/modelo-por-rol` con las pruebas 1–7 en su descripción.
- `ESTADO.md` (o bitácora) del proyecto: una línea con fecha y PR.
- Fecha de fusión comunicada a FinOps-Ecosistema (vía Andres), para la medición.

---
**Veredicto del guardián (2026-09-28):** APROBADA CON CONDICIONES en la primera
versión. Hallazgos 1–6 (ChatBotRAG desde `main`, destinos de AAB1, prueba de
modelos no determinista, CI inexistente en 8 repositorios, referencia a
`PLAN_AGENTES`, alcance de la reversión) incorporados en esta versión. Revisión
del agente `seguridad`: no obligatoria (no toca IAM, redes, retención ni
pipeline); recomendada y asignada a la sesión de SeguridadGeneral.
