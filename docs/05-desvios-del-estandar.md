# 05 · Desvíos del estándar DevSecOps v2

| Versión | Fecha | Estado |
|---|---|---|
| 0.4 | 2026-09-30 | Vigente; PR #1 fusionado; ruleset solo con squash |

Este repositorio no despliega nada. Usa el stack `solo-ci` (calidad, seguridad-estatica y compuerta-pr), sin `release.yml`, DAST, `deploy.sh` ni variables de nube. Se aplicó con `bootstrap-repo.sh` 2.2, `--stack solo-ci --modo A --sin-gh`. Lo que sigue es todo lo que difiere de lo que genera el script.

| # | Qué | Dónde | Por qué |
|---|---|---|---|
| 1 | `stack: python` en el manifiesto | `.devsecops.yml` | El repositorio tendrá scripts de consulta en Python (hoy solo tiene la prueba de invariantes) |
| 2 | `tests/test_invariantes.py` | `tests/` | Automatiza las verificaciones de `CLAUDE.md` (scripts sin verbos de modificación, salida solo en `datos/`, `datos/` ignorado). Los revisores son funciones puras con casos positivos y negativos, porque `scripts/` aún está vacío; `calidad` la ejecuta al detectar pruebas |
| 3 | `.github/dependabot.yml` solo con `github-actions` | `.github/` | El repositorio no tiene `package.json`, dependencias Python, Dockerfile ni `infra/`; los otros cuatro ecosistemas fallarían cada semana. Se añade el que corresponda si aparece |
| 4 | `.github/CODEOWNERS` con `@AndresAlberdi @segurolotengopy` y sin las rutas de los stacks que despliegan (firestore, Docker, AWS, `infra/`); quedan previstas las que aún no existen (`requirements*.txt`, `pyproject.toml`, `CHANGELOG.md`) | `.github/` | Los equipos `@ORG/...` del script no existen en un repositorio personal y harían imposible la revisión de propietario; la autora no aprueba su propio PR |
| 5 | `.github/workflows/codeql.yml` añadido y variable de repositorio `CODEQL_LENGUAJES=python` | `.github/`, Settings → Variables | El modo A lo exige en repositorios públicos y `solo-ci` no lo copia. Sin la variable analizaría JavaScript |
| 6 | Sin la skill `pase-a-produccion` | `.claude/skills/` | No hay pase a producción |
| 7 | `.claude/worktrees/`, `.coverage` y `coverage.xml` en `.gitignore` | raíz | Los worktrees viven dentro del proyecto; `pytest --cov` genera los otros dos |

Las rutas al estándar en `.claude/agents/` y en la skill apuntan a `~/SeguridadGeneral`, no a una ruta efímera.

No se cargaron variables ni secretos de GitHub más allá de `CODEQL_LENGUAJES` (`--sin-gh`). El ruleset de `main` (id 24272555: sin borrado ni force-push, historial lineal, 1 aprobación con revisión de propietario y `compuerta-pr` obligatorio) lo creó Claude con autorización de Andres el 2026-09-30 y, también con su autorización, se dejó con `allowed_merge_methods: [squash]`, como pide el estándar (el script de bootstrap no lo fija).
