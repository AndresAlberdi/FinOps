# Ahorro de minutos de CI en `SeguroLoTengoDemo` — bloque para la sesión dueña de `segurolotengo-demo`

> Origen: FinOps-Ecosistema, 2026-10-25 (v2). **Veredictos: guardián, aprobada con condiciones G1 a G10; agente `seguridad`, aprobada con condiciones S1 a S10 (ambos del 2026-10-25, incorporados abajo). No se envía a la sesión dueña hasta que Andres lo autorice en el chat.**
>
> **Valor muy bajo, y se declara de entrada:** con las condiciones de los revisores, el único ahorro medido es de **~106 minutos en 25 días (~0,64 USD; ~0,8 USD al mes)**. El exceso facturado de GitHub en octubre fue de 7,65 USD. **Recomendación de FinOps: no ejecutar este bloque ahora**; subir el tope de Actions unos USD es más barato que el trabajo de la sesión dueña. El bloque queda documentado por si el volumen de CI crece.

## Qué se midió (solo lectura, 1 al 25/10/2026)
Fuente: API de GitHub (`actions/runs` y `jobs`) con la cuenta propietaria; minutos por trabajo redondeados hacia arriba, Linux 2 núcleos a **0,006 USD por minuto** (docs.github.com, «Actions runner pricing», consultada el 2026-10-25). Datos crudos en `datos/github/` (no versionado). Cifras recalculadas por el guardián:
- **3.762 minutos** de CI en 628 ejecuciones del flujo `CI`: ~22,57 USD brutos, contra 22,88 de la pantalla de Facturación que mostró Andres el 25/10 (captura, no API).
- **Por trabajo:** pruebas y lint 1.582 (media 2,53 min), Semgrep 908 (1,45), Trivy 640 (1,02), Gitleaks 632 (1,01). `CodeQL` no cobra.
- **Por evento:** `pull_request` 2.534 (67 %); `push` a `main` 1.228 (33 %; 204 ejecuciones).
- **Cambios solo de documentación:** 106 ejecuciones y 636 minutos (16,9 %): 76 en PR (465 min) y 30 en `push` (171 min).
- **Canceladas:** 46 ejecuciones y 227 minutos; en PR son 19 y 105 minutos. Los datos solo registran «cancelada», no la causa.
- **Ejecuciones por rama de PR:** mediana 1, media 1,7, p90 3.
- **Por qué el margen es corto:** cada trabajo cobra **al menos 1 minuto**; un trabajo auxiliar de detección costaría ≥ 1 minuto por ejecución de PR (424 en 25 días) y ahorraría 306 minutos brutos como máximo, así que la detección debe ir **dentro** de los trabajos existentes.
- **Reglas de la rama (`main-protegida` y `produccion-protegida`):** cuatro chequeos obligatorios (`Typecheck, lint y tests`, `Semgrep (SAST)`, `Gitleaks (secret scanning)`, `Trivy (dependencias e IaC)`), sin actores con bypass, política «rama al día» **desactivada**. `ci.yml` corre en `push` solo a `main`.

## Qué pedir (único pedido)
1. **Omitir solo `Typecheck, lint y tests` (solo sus pasos, no el trabajo) en PR con base `main` cuyos cambios sean solo de documentación.**
   - **Detección dentro del propio trabajo,** con `git diff --no-renames --name-only -z HEAD^1 HEAD` sobre la referencia de fusión del PR (`fetch-depth: 2`), sin `--diff-filter`, de modo que renombres, eliminaciones y rutas de origen cuentan. Solo `git`: sin API de PR, sin acciones de terceros y sin ampliar `permissions` (queda `contents: read`).
   - **Clasificación estricta (Y):** un archivo es documentación solo si su extensión es `md`, `pdf`, `csv`, `png`, `jpg` o `txt` **y** su ruta empieza por `docs/`, `Prompts/` o `pantallas/` en la raíz del repositorio, o es un `*.md` en la raíz. **Fuerzan la corrida completa y ganan siempre:** `.github/`, `.claude/`, `.semgrep/`, `.gitleaks*`, `.trivyignore*`, `src/`, `tests/`, `e2e/`, `infra/`, `scripts/`, `public/`, `docs/manuales-asistente/`, `docs/asistente/`, `package*.json` y los archivos de configuración de la raíz (`*.config.*`). Quedan fuera de «documentación»: `.json`, `.js`, `.html`, `.css`, `.svg` y `.docx`.
   - **Falla cerrada, en el código:** `set -euo pipefail`; la salida vale `completo` por defecto y se omite solo si es exactamente `solo_docs` (el `if` compara contra el literal `steps.detectar.outputs.solo_docs == 'true'`); lista vacía, ausencia de `HEAD^2`, ausencia de `.git` o cualquier error de git dan corrida completa. Aplica solo con `github.event_name == 'pull_request'` y `github.base_ref == 'main'`: en `push` y en los PR hacia `produccion` corre todo (allí no hay CI de respaldo).
   - **Los otros tres trabajos no se tocan:** Semgrep, Trivy y Gitleaks corren siempre y completos (Semgrep con `p/secrets` analiza texto de documentación y escanear sigue siendo §1.5 de `docs/03`; Gitleaks mantiene `fetch-depth: 0`). Ahorro medido bajo estas reglas: **~106 minutos en 25 días**.

## Lo que NO se pide (y por qué)
- **Borradores y `ready_for_review`:** se descarta. Los datos dicen mediana de 1 ejecución por rama (media 1,7), así que casi no hay qué ahorrar, y un chequeo omitido con `if` figura como «skipped», que cuenta como cumplido: al pasar a «listo» el PR podría aparecer fusionable sin CI. No vale ese riesgo.
- **Omitir Semgrep, Trivy o Gitleaks:** no. Omitir Semgrep reduce un control del estándar (§1.5) por 39 minutos (~0,23 USD en 25 días); sin aceptación expresa de `seguridad`, el bloque quedaría rechazado.
- **Reducir la CI de `push` a `main`:** no. Con «rama al día» desactivada, es la única que prueba el resultado combinado de la fusión (y la fusión a `main` es el despliegue). Ahorraría ~424 minutos, pero cambia la semántica de la compuerta.
- No se activa «rama al día», no se cambian nombres de trabajos ni de chequeos obligatorios, no se toca el estándar de SeguridadGeneral. FinOps no edita archivos de `segurolotengo-demo`.

## Pruebas (no regresión)
- **Casos que deben correr completos** (cada uno con un PR de prueba): renombre de `src/x.ts` a `docs/x.md`; solo la fixture `src/domain/__tests__/datos/*.txt`; solo `docs/manuales-asistente/_indice.json`; un `.tsx` en `src/components/v4/pantallas/`; un `.md` en `.github/` o en `infra/`; un PR con documentación y código; un PR cuya detección falla (se simula quitando `HEAD^2`).
- **Caso que debe omitir:** un PR solo de documentación (`docs/*.md`): los cuatro chequeos quedan en verde y `Typecheck, lint y tests` cobra 1 minuto.
- **Los escáneres siguen viendo todo:** en ese PR, Gitleaks, Trivy y Semgrep corren completos; un secreto de prueba revocado hace fallar Gitleaks.
- **Umbral de no regresión y disparador de reversión:** el trabajo de pruebas en un PR solo de documentación cobra 1 minuto; en noviembre **ninguna falla de la CI de `push` a `main` atribuible a un PR omitido**; si ocurre una, **se revierte el mismo día**. El ahorro se mide **por ejecución** (minutos por PR solo de documentación), no por el total mensual.
- **Antes de cada fusión,** el procedimiento verifica que los cuatro check runs del último commit concluyeron `success` y no `skipped`, y lo anota en el mensaje de fusión.

## Reversión
Quitar el paso de detección y los `if` de los pasos de pruebas: un commit revertible, ~5 minutos más una corrida de CI. Los nombres de los trabajos no cambian, así que la reversión no toca las reglas de la rama. La fusión del revert dispara un despliegue sin efecto funcional.

## Cómo trabajar
Worktree y rama propios, partiendo de `origin/main`; un PR; commit por ruta; **push y PR solo con el «sí» de Andres en tu chat**. Andres autoriza; tú operas. Revisión de `seguridad` antes del OK de fusión (toca la compuerta de CI). Ningún secreto en el repositorio.

## Controles de `docs/03` que toca
§1.5 (escáneres del estándar): **no se reduce ninguno**; solo las pruebas de código se omiten, y solo cuando el cambio no contiene código ni configuración. **Costo:** turnos de la sesión dueña (se declara y se mide). **Ahorro esperado:** ~0,8 USD al mes; **no se mide hasta el 1/12**, con la lectura de noviembre por ejecución. **Reversión:** arriba.

## Observaciones para la sesión dueña (fuera del bloque)
Los rulesets de `SeguroLoTengoDemo` piden 0 aprobaciones, sus contextos obligatorios no están atados a GitHub Actions por `integration_id` y el repositorio privado no tiene secret scanning de GitHub (`security_and_analysis` nulo). Son hallazgos de `seguridad`, no de costo.
