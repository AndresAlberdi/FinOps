#!/usr/bin/env python3
"""Costo de WhatsApp Cloud API por cuenta (WABA), solo lectura.

Consulta `pricing_analytics` de la Graph API de Meta, que desglosa el cargo
aproximado por categoría de mensaje, tipo de precio y país. Un mes por corrida.

Reglas del proyecto (CLAUDE.md): solo lectura; el token llega por archivo o
variable, nunca por argumento ni por la URL; nunca se imprime; los datos crudos
van solo a datos/meta/ (ignorado por git) y los identificadores se muestran por
sus últimos dígitos.

Entradas:
  datos/meta/wabas.txt    una WABA por línea: <id> [alias]
  META_TOKEN_FILE         archivo con el token (por defecto datos/meta/token)
  META_GRAPH_VERSION      versión de la Graph API (verificar la vigente)

Uso: python3 scripts/meta/pricing_analytics.py --mes 2026-10
"""

import argparse
import calendar
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DATOS = RAIZ / "datos" / "meta"
BASE = "https://graph.facebook.com"
VERSION_POR_DEFECTO = "v23.0"  # (verificar) la versión vigente de la Graph API


def ultimos(identificador: str, n: int = 4) -> str:
    """Identificador por sus últimos dígitos."""
    return "…" + str(identificador)[-n:]


def rango_del_mes(mes: str) -> tuple[int, int]:
    """Marcas de tiempo UNIX (UTC) de inicio y fin del mes «AAAA-MM»."""
    anio, m = (int(x) for x in mes.split("-"))
    ultimo = calendar.monthrange(anio, m)[1]
    inicio = datetime(anio, m, 1, tzinfo=UTC)
    fin = datetime(anio, m, ultimo, 23, 59, 59, tzinfo=UTC)
    return int(inicio.timestamp()), int(fin.timestamp())


def construir_url(waba: str, mes: str, version: str = VERSION_POR_DEFECTO) -> str:
    """URL de pricing_analytics. El token NO va aquí: va en la cabecera."""
    inicio, fin = rango_del_mes(mes)
    campo = (
        f"pricing_analytics.start({inicio}).end({fin}).granularity(MONTHLY)"
        '.dimensions(["PRICING_CATEGORY","PRICING_TYPE","COUNTRY"])'
        '.metric_types(["COST","VOLUME"])'
    )
    consulta = urllib.parse.urlencode({"fields": campo})
    return f"{BASE}/{version}/{urllib.parse.quote(str(waba))}?{consulta}"


def agregar(respuesta: dict) -> dict:
    """Suma costo y volumen por (categoría, tipo de precio, país)."""
    filas: dict[tuple, dict] = defaultdict(lambda: {"costo": 0.0, "volumen": 0})
    bloque = respuesta.get("pricing_analytics", {})
    for grupo in bloque.get("data", []):
        for punto in grupo.get("data_points", []):
            clave = (
                punto.get("pricing_category", "?"),
                punto.get("pricing_type", "?"),
                punto.get("country", "?"),
            )
            filas[clave]["costo"] += float(punto.get("cost", 0) or 0)
            filas[clave]["volumen"] += int(punto.get("volume", 0) or 0)
    return {
        "/".join(k): {"costo": round(v["costo"], 4), "volumen": v["volumen"]}
        for k, v in sorted(filas.items())
    }


def leer_token(ruta: Path | None = None) -> str:
    """Token desde META_TOKEN_FILE o datos/meta/token. Nunca se imprime."""
    archivo = ruta or Path(os.environ.get("META_TOKEN_FILE", DATOS / "token"))
    if not archivo.exists():
        raise SystemExit(f"Falta el archivo del token: {archivo}")
    token = archivo.read_text().strip()
    if not token:
        raise SystemExit("El archivo del token está vacío")
    return token


def leer_wabas(ruta: Path | None = None) -> list[tuple[str, str]]:
    archivo = ruta or DATOS / "wabas.txt"
    if not archivo.exists():
        raise SystemExit(
            f"Falta la lista de WABA: {archivo} (una por línea: <id> [alias])"
        )
    salida = []
    for linea in archivo.read_text().splitlines():
        partes = linea.split("#", 1)[0].split()
        if partes:
            salida.append((partes[0], " ".join(partes[1:]) or ultimos(partes[0])))
    return salida


def consultar(waba: str, mes: str, token: str, version: str) -> dict:
    peticion = urllib.request.Request(
        construir_url(waba, mes, version),
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(peticion, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        cuerpo = e.read().decode("utf-8", "replace")[:300]
        return {"error": {"http": e.code, "mensaje": cuerpo}}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--mes", required=True, help="AAAA-MM")
    p.add_argument(
        "--version", default=os.environ.get("META_GRAPH_VERSION", VERSION_POR_DEFECTO)
    )
    args = p.parse_args(argv)
    token, wabas = leer_token(), leer_wabas()
    DATOS.mkdir(parents=True, exist_ok=True)
    resultado, total = {}, 0.0
    for waba, alias in wabas:
        crudo = consultar(waba, args.mes, token, args.version)
        (DATOS / f"pricing-{args.mes}-{ultimos(waba)}.json").write_text(
            json.dumps(crudo)
        )
        if "error" in crudo:
            print(f"{alias} ({ultimos(waba)}): error {crudo['error']}", file=sys.stderr)
            continue
        filas = agregar(crudo)
        resultado[alias] = filas
        total += sum(v["costo"] for v in filas.values())
        for clave, v in filas.items():
            print(f"{alias:20} {clave:42} {v['volumen']:8d} {v['costo']:10.4f}")
    print(
        f"\nTotal aproximado {args.mes}: USD {total:.4f} ({len(wabas)} WABA, {len(wabas)} solicitudes)"
    )
    (DATOS / f"resumen-{args.mes}.json").write_text(json.dumps(resultado, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
