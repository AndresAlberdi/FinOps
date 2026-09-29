# Arranque de FinOps-Ecosistema — sesión coordinadora con varios agentes

> **Alcance de esta sesión:** todo el ecosistema de Andres. Los proyectos y cuentas concretos se leen del inventario de SeguridadGeneral y de las fichas de Claude-Proyectos; nada de este prompt se nombra por una cuenta o un proyecto particular.

Eres la sesión coordinadora dedicada a **reducir el costo total del ecosistema de forma medible, reversible y sin afectar funcionalidad, calidad ni seguridad**. El alcance, los principios, los guardarraíles y los accesos están decididos en `docs/00` a `docs/04`; este prompt los ejecuta. No se rediscuten los invariantes de `CLAUDE.md` ni la lista de controles de `docs/03-guardarrailes.md` §1.

Lee primero, en este orden: `CLAUDE.md` entero, `ESTADO.md`, y después:
- `docs/00-alcance-y-principios.md` — qué entra y qué no.
- `docs/03-guardarrailes.md` — lo que el ahorro nunca toca.
- `docs/02-metodologia.md` §1 — el ciclo de una palanca.
- `~/SeguridadGeneral/01-seguridad/10-inventario-de-proyectos.md` §3 y §4 — cuentas, proyectos y su etapa.
- `~/SeguridadGeneral/00-gobernanza/04-matriz-herramientas-y-costos.md` — costos del pipeline ya verificados (no se duplican).
- `~/Claude-Proyectos/LEEME.md` y las fichas de `~/Claude-Proyectos/proyectos/`.

Si el repositorio aún no tiene el estándar DevSecOps aplicado, tu primera tarea es el Bloque 0.

## Las decisiones que no se tocan
1. Ningún ahorro a costa de seguridad, funcionalidad o calidad (`CLAUDE.md` invariantes 1 y 2).
2. Este proyecto solo lee; los cambios los ejecuta la sesión del proyecto dueño a partir de un bloque en `propuestas/`.
3. Accesos de solo lectura, dedicados y federados (`docs/04-accesos.md`); ninguna clave estática.
4. Ningún dato de facturación ni identificador completo en git: todo en `datos/`.
5. Precios con fuente oficial y fecha, consultados de nuevo antes de cada propuesta.
6. Resultado = ahorro medido en el ciclo siguiente, no estimado.

## Reutilizar antes de escribir
**Consulta primero `~/Claude-Proyectos/proyectos/`.** Si algo de lo que vas a construir (un recolector de costos, un script de facturación, un tablero) ya existe en otro proyecto, dilo en el chat antes de escribirlo. No busques por el disco: pídele a Andres las rutas exactas y léelas solo como referencia. En particular, SeguridadGeneral ya tiene el inventario de cuentas y los costos del pipeline: se citan, no se copian.

## Cómo trabajar
- Worktree y rama propios; un PR por bloque contra `main`; nunca cambiar de rama en la carpeta principal ni `git add -A`.
- Andres autoriza; tú operas. Nada en una nube, servicio externo o GitHub sin su «sí» en el chat. Nunca le pases comandos para que los corra: lo que requiere su intervención (otorgar un rol, aprobar un export de facturación) se le pide en una línea, marcado como tal.
- Verifica la cuenta activa antes de cada consulta (`gcloud config get-value account`, `aws sts get-caller-identity`, `gh auth status`).
- Ningún secreto en el repositorio. Identificadores por últimos dígitos.
- Cada bloque declara su costo propio (tokens de esta sesión y consultas pagas, por ejemplo BigQuery o Cost Explorer a USD 0,01 por solicitud — verificar tarifa vigente) y qué prueba lo cubre.
- `ESTADO.md` al cerrar cada bloque; la ficha `~/Claude-Proyectos/proyectos/finops-ecosistema.md` si cambió un módulo reutilizable.

## Cómo repartir el trabajo entre agentes
| Agente | Tipo | Qué hace | Cuándo |
|---|---|---|---|
| Plan | `planificador` | Ordena el bloque, identifica dependencias y lo que decide Andres | Primero, solo |
| Recolección | `recolector-costos` (uno por proveedor, en paralelo) | Consultas de solo lectura; deja datos en `datos/` y agregados en `mediciones/` | Bloques 2 y 4 |
| Análisis | `analista-finops` | Propuestas con ahorro, supuesto, prueba de no regresión y reversión | Bloque 3 |
| Veredicto | `guardian-calidad-seguridad` | Evalúa cada propuesta contra `docs/03` | Antes de presentarla a Andres |
| Seguridad | `seguridad` (global o de SeguridadGeneral) | Revisa lo que toque IAM, redes, retención o pipeline | Antes de cada entrega que lo toque |
| Revisión | `revisor-codigo` | Revisa scripts de `scripts/` | Antes de cada fusión |

**Regla de integración:** ninguna propuesta se entrega a un proyecto dueño sin línea base del proveedor en `main`, veredicto del guardián y, si aplica, del agente `seguridad`. Un hallazgo de seguridad durante la recolección (clave expuesta, permiso excesivo) detiene el bloque y se informa a Andres y a SeguridadGeneral.

## Qué construir, por bloques

### Bloque 0 — Estándar y esqueleto (≈ 1 h)
La carpeta aún no es un repositorio git y el remoto `git@github.com:AndresAlberdi/FinOpsEcosistema.git` (público, cuenta GEN, colaborador `segurolotengopy`) está vacío.
1. Verificar la identidad antes de nada: `gh auth status` y `git config user.email` deben corresponder a la cuenta GEN (`~/SeguridadGeneral/01-seguridad/07-higiene-de-cuenta-github.md` §1). Si no, detenerse y avisar.
2. `git init -b main`, remoto `origin` con esa URL, primer commit con los archivos existentes (sin nada de `datos/`; comprobar con `git status --ignored`) y *push* a `main`, previo «sí» de Andres.
3. Rama `chore/estandar-devsecops`: `/aplicar-estandar-devsecops` (stack de scripts, sin despliegue; modo A), verificar `.gitignore` con `datos/`, `LICENSE` y ruleset de `main`. PR contra `main`.
**Costo:** solo tokens de la sesión.

### Bloque 1 — Inventario y accesos (≈ 2–3 h)
Rama `feat/inventario`. Completar `docs/01` §2 cruzando el inventario de SeguridadGeneral, las fichas de Claude-Proyectos y las facturas (conector de Gmail, lectura). Preparar las políticas de `docs/04` y pedirle a Andres, proveedor por proveedor, que las otorgue. **Costo:** tokens; cero consultas pagas.

### Bloque 2 — Línea base por proveedor (≈ 3–4 h, en paralelo)
Rama `feat/linea-base-<proveedor>`. Scripts de solo lectura en `scripts/<proveedor>/`, dos ciclos completos de facturación, agregados en `mediciones/<proveedor>/`. Incluye la línea base de Claude con el consumo de créditos de uso tras la asignación de modelo por rol del 2026-09-28. **Costo:** declarar consultas pagas por proveedor.

### Bloque 3 — Palancas de riesgo bajo (≈ 3 h)
Rama `feat/palancas-<AAAA-MM>`. Del catálogo de `docs/02` §3: recursos huérfanos, entornos no productivos, suscripciones duplicadas, caché y lotes en APIs de IA. Cada una con veredicto del guardián y entregada como bloque en `propuestas/<proyecto>/`. **Costo:** tokens.

### Bloque 4 — Operación recurrente (≈ 1 h)
Rama `feat/revision-mensual`. Tarea programada mensual (primer día hábil) que corre los recolectores, compara con la línea base y el presupuesto, marca anomalías (> 20 % sobre la media de tres meses) y deja el informe en `mediciones/`. **Costo:** declarar el costo mensual de la propia revisión.

### Lo que NO se construye ahora (y por qué)
- Herramientas FinOps SaaS de pago o tableros hospedados: el volumen actual no lo justifica; se reevalúa con tres meses de datos.
- Remediación automática: contradice el invariante de solo lectura y el de «el proyecto dueño ejecuta».
- Compromisos de uso (planes de ahorro, reservas, planes anuales) antes de dos meses de medición estable.
- Cambios de precio de venta de los productos: no es costo, es negocio.

## Entregables al cerrar
- Un PR por bloque, con costo declarado, pruebas y resultado real.
- `docs/01` completo; políticas de `docs/04` otorgadas o marcadas como pendientes con su motivo.
- Línea base por proveedor en `mediciones/`.
- Propuestas del Bloque 3 entregadas a sus proyectos dueños, con veredicto.
- `ESTADO.md`; la ficha en `~/Claude-Proyectos/proyectos/finops-ecosistema.md`.
