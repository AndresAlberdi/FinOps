# 05 · Desvíos del estándar DevSecOps v2

| Versión | Fecha | Estado |
|---|---|---|
| 0.2 | 2026-09-30 | Sin desvíos: se aplica el stack `solo-ci` del estándar (bootstrap 2.2) |

Este repositorio no despliega nada. Usa el stack `solo-ci` (calidad, seguridad-estatica y compuerta-pr), sin `release.yml`, DAST, `deploy.sh` ni variables de nube. Se aplicó con `bootstrap-repo.sh --stack solo-ci --modo A --sin-gh`.

**Lo único propio:**

| Qué | Dónde | Por qué |
|---|---|---|
| `stack: python` en el manifiesto | `.devsecops.yml` | El repositorio tendrá scripts de consulta en Python y la prueba de invariantes |
| `tests/test_invariantes.py` | `tests/` | Automatiza tres verificaciones de `CLAUDE.md`: `datos/` y los exportes ignorados por git, scripts sin verbos de modificación y salida solo en `datos/`. `calidad` la ejecuta porque detecta pruebas |
| Sin la skill `pase-a-produccion` | `.claude/skills/` | No hay pase a producción |
| `.claude/worktrees/` en `.gitignore` | raíz | Los worktrees viven dentro del proyecto |

No se cargaron variables ni secretos de GitHub (`--sin-gh`). El ruleset de `main` con el check `compuerta-pr` lo crea Andres.
