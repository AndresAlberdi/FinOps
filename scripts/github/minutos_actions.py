#!/usr/bin/env python3
"""Minutos de GitHub Actions por repositorio privado, solo lectura.

El endpoint oficial de tiempos (`/actions/runs/{id}/timing`) devuelve ceros, así
que se calcula desde la duración de cada trabajo (`/actions/runs/{id}/jobs`),
redondeando hacia arriba por trabajo, como factura GitHub. Es una ESTIMACIÓN:
la cifra exacta está en Facturación → Uso de la cuenta.

Reglas del proyecto (CLAUDE.md): solo `gh api` con GET; los datos van a
datos/github/ (ignorado por git); nada de tokens en argumentos.

Entrada: datos/github/repos.txt, una línea por repositorio:
    <owner/repo> [<directorio de configuración de gh para esa cuenta>]
Uso: python3 scripts/github/minutos_actions.py --mes 2026-09 --cuota 3000
"""

import argparse
import calendar
import math
import os
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DATOS = RAIZ / "datos" / "github"
MAX_TRABAJO_MIN = 360  # un trabajo alojado por GitHub no puede durar más de 6 h


def minutos_trabajo(inicio: str, fin: str) -> int:
    """Minutos facturables de un trabajo (redondeo hacia arriba); 0 si no corrió."""
    if not inicio or not fin:
        return 0
    segundos = (_t(fin) - _t(inicio)).total_seconds()
    return math.ceil(segundos / 60) if segundos > 0 else 0


def _t(texto: str) -> datetime:
    return datetime.fromisoformat(texto)  # Python 3.11+ acepta el sufijo «Z»


def resumir(trabajos: list[tuple], eventos: dict[str, str]) -> dict:
    """trabajos: (id_ejecucion, inicio, fin, conclusion); eventos: id -> evento."""
    cat: dict[str, int] = defaultdict(int)
    for rid, inicio, fin, _conclusion in trabajos:
        m = minutos_trabajo(inicio, fin)
        if m > MAX_TRABAJO_MIN:
            cat["descartados (>6 h, artefacto)"] += m
        elif m:
            cat["Dependabot" if eventos.get(rid) == "dynamic" else "CI y demás"] += m
    return dict(cat)


def cuota_usada(resumen: dict, cuota: int) -> tuple[int, int, float]:
    """(minutos sin Dependabot, minutos con Dependabot, porcentaje de la cuota)."""
    base = resumen.get("CI y demás", 0)
    total = base + resumen.get("Dependabot", 0)
    return base, total, round(100 * total / cuota, 1) if cuota else 0.0


def rango(mes: str) -> str:
    anio, m = (int(x) for x in mes.split("-"))
    return f"{anio}-{m:02d}-01..{anio}-{m:02d}-{calendar.monthrange(anio, m)[1]}"


def gh(argumentos: list[str], config: str | None) -> str:
    entorno = dict(os.environ)
    if config:
        entorno["GH_CONFIG_DIR"] = config
    r = subprocess.run(
        ["gh", "api", *argumentos],
        capture_output=True,
        text=True,
        env=entorno,
        check=False,
    )
    return r.stdout


def leer_repos(ruta: Path | None = None) -> list[tuple[str, str | None]]:
    archivo = ruta or DATOS / "repos.txt"
    if not archivo.exists():
        raise SystemExit(
            f"Falta {archivo} (una línea por repositorio: owner/repo [config de gh])"
        )
    salida = []
    for linea in archivo.read_text().splitlines():
        partes = linea.split("#", 1)[0].split()
        if partes:
            salida.append((partes[0], partes[1] if len(partes) > 1 else None))
    return salida


def medir(repo: str, config: str | None, mes: str) -> dict:
    corridas = gh(
        ["--paginate", f"repos/{repo}/actions/runs?created={rango(mes)}&per_page=100",
         "--jq", ".workflow_runs[] | [.id,.event] | @tsv"],
        config,
    )  # fmt: skip
    eventos = dict(
        linea.split("\t") for linea in corridas.splitlines() if "\t" in linea
    )
    trabajos = []
    for rid in eventos:
        salida = gh(
            [f"repos/{repo}/actions/runs/{rid}/jobs?per_page=100", "--jq",
             ".jobs[] | [.started_at,.completed_at,.conclusion] | @tsv"],
            config,
        )  # fmt: skip
        for linea in salida.splitlines():
            p = (linea.split("\t") + ["", "", ""])[:3]
            trabajos.append((rid, *p))
    return {"ejecuciones": len(eventos), **resumir(trabajos, eventos)}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--mes", required=True, help="AAAA-MM")
    p.add_argument(
        "--cuota",
        type=int,
        default=3000,
        help="minutos gratis del plan (Pro 3000, Free 2000)",
    )
    args = p.parse_args(argv)
    DATOS.mkdir(parents=True, exist_ok=True)
    total = 0
    for repo, config in leer_repos():
        r = medir(repo, config, args.mes)
        base, con, _ = cuota_usada(r, args.cuota)
        total += con
        print(
            f"{repo:42} {r['ejecuciones']:5d} ejecuciones  {base:6d} min (con Dependabot {con})"
        )
    print(
        f"\nTotal {args.mes}: {total} min = {100 * total / args.cuota:.1f} % de {args.cuota} min gratis"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
