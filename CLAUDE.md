# FinOps-Ecosistema — optimización de costos y recursos del ecosistema

Proyecto transversal que mide y reduce el costo de todos los servicios que usa Andres (Claude/Anthropic, AWS, Google Cloud y Firebase, OCI, n8n, Meta WhatsApp Cloud API, GitHub y los demás que figuren en el inventario) **sin afectar funcionalidad, calidad ni seguridad**. No es una aplicación: produce inventarios, líneas base, propuestas y mediciones. Los cambios en otros proyectos los ejecuta la sesión de ese proyecto.

Lea por ruta cuando la tarea lo requiera: `docs/00-alcance-y-principios.md` (qué se optimiza y qué no), `docs/01-inventario-de-servicios.md`, `docs/02-metodologia.md`, `docs/03-guardarrailes.md`, `docs/04-accesos.md`. El estado y los avances viven en `ESTADO.md`, nunca en este archivo.

## Invariantes (no admiten excepción)

1. **Ningún ahorro a costa de seguridad.** Nunca se proponen como ahorro los controles listados en `docs/03-guardarrailes.md` §1 (cifrado, respaldos, retención exigida por norma, WAF, App Check, escáneres del estándar, logs de auditoría, federación OIDC, licencias GHAS en modo B, alta disponibilidad de producción). Si una palanca toca uno de ellos, se descarta.
2. **Ningún ahorro a costa de funcionalidad o calidad.** Toda propuesta declara su prueba de no regresión (qué se mide antes y después: latencia, tasa de error, calidad de respuesta, cobertura) y su reversión. Sin prueba y reversión, no se propone.
3. **Solo lectura por defecto.** Este proyecto consulta costos y configuración con identidades de solo lectura (`docs/04-accesos.md`). No modifica recursos, repositorios ni servicios de otros proyectos.
4. **Los cambios los ejecuta el proyecto dueño.** Una propuesta aprobada se entrega como bloque en `propuestas/<proyecto>/<AAAA-MM>-<tema>.md`, con el formato de `~/Claude-Proyectos/prompts/PLANTILLA-PROMPT.md`, para que la sesión de ese proyecto la ejecute con su propio estándar y sus agentes.
5. **Andres autoriza; Claude opera.** Nada se ejecuta en una nube, un servicio externo o GitHub sin su «sí» en el chat. Nunca se le pasan comandos para que los corra: lo que requiere su intervención (otorgar un rol, una aprobación de facturación) se le pide por separado y en una línea.
6. **Ningún dato de facturación ni identificador en git.** Exportes, CSV, capturas y consultas con resultados van en `datos/` (ignorado por git). Los documentos versionados usan cifras agregadas e identificadores por sus últimos dígitos. Sin secretos, nunca.
7. **Precios con fuente y fecha.** Toda tarifa citada lleva la página oficial y la fecha de consulta; lo no confirmado se marca «(verificar)». Los precios se vuelven a consultar antes de cada propuesta: no se asumen de memoria.
8. **Ahorro medido, no estimado.** Cada propuesta ejecutada se cierra con la medición real del período siguiente frente a la línea base, anotada en `mediciones/`. Una estimación no cuenta como resultado.

## Coordinación

- **Claude-Proyectos** (`~/Claude-Proyectos/`): antes de proponer algo en un proyecto, leer su ficha en `proyectos/`. Al cerrar una jornada que cambie un módulo reutilizable de este proyecto, actualizar `proyectos/finops-ecosistema.md`.
- **SeguridadGeneral** (`~/SeguridadGeneral/`): es la fuente de verdad de seguridad y de costos de herramientas del pipeline (`00-gobernanza/04-matriz-herramientas-y-costos.md`) y del inventario de cuentas y proyectos (`01-seguridad/10-inventario-de-proyectos.md`). Este proyecto no los duplica: los cita. Toda propuesta que toque identidades, IAM, redes, retención o controles del pipeline pasa por el agente `seguridad` antes de entregarse.
- Leer código u otros repositorios está permitido en solo lectura, diciendo en el chat qué se leyó y para qué.

## Estructura

`docs/` (principios, inventario, metodología, guardarraíles, accesos) · `propuestas/<proyecto>/` (bloques para la sesión dueña) · `mediciones/` (línea base y resultado real, agregados) · `scripts/` (consultas de solo lectura, sin credenciales embebidas) · `datos/` (local, ignorado) · `Prompts/` (sesiones dedicadas).

## Verificación antes de terminar

- `scripts/`: `bash -n` o `ruff check` según el lenguaje; ningún script escribe fuera de `datos/` ni usa verbos de modificación (`create`, `update`, `delete`, `put`, `apply`).
- `git status` sin nada dentro de `datos/`; `gitleaks` o `./security-local.sh` cuando el estándar esté aplicado.
- Idioma: español formal (sin voseo). Conventional Commits.

## Delegación entre agentes y costo

La sesión principal orquesta. El modelo de cada agente está fijado en el campo `model` de su archivo en `.claude/agents/` (o en `~/.claude/agents/` para los genéricos): **Opus** para planificar, analizar palancas y revisar; **Sonnet** para recolectar y normalizar datos.

1. Ciclo de una palanca: `recolector-costos` (datos de solo lectura) → `analista-finops` (propuesta con prueba y reversión) → `guardian-calidad-seguridad` (veredicto) → entrega a la sesión dueña.
2. Búsquedas amplias: agente integrado `Explore`. Al delegar, pasar rutas y el criterio de terminado; no pegar datos extensos.
3. No usar el modo rápido (*fast mode*) salvo pedido explícito.
4. **Este archivo es estable.** Estado, cifras y pendientes van en `ESTADO.md` y `mediciones/`; cada edición de este archivo invalida la caché de contexto.
