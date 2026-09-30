"""Automatiza las verificaciones de CLAUDE.md que no dependen de una persona."""

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
VERBOS_PROHIBIDOS = re.compile(
    r"\b(create|update|delete|put|apply|set-iam-policy|remove|terminate|modify)"
    r"(-[a-z-]+)?\b",
    re.IGNORECASE,
)
# Verbos que solo son una palabra en comentarios o mensajes de ayuda no cuentan:
# se miran únicamente las líneas que invocan una CLI de nube o de GitHub.
INVOCA_NUBE = re.compile(r"\b(aws|gcloud|gsutil|bq|oci|gh|kubectl|terraform)\b")


def _scripts():
    carpeta = RAIZ / "scripts"
    return [p for p in carpeta.rglob("*") if p.suffix in {".sh", ".py"}]


def test_gitignore_excluye_datos_y_exportes():
    lineas = (RAIZ / ".gitignore").read_text().splitlines()
    for patron in ("datos/", "*.csv", "*.parquet", ".env"):
        assert patron in lineas, f"falta {patron} en .gitignore"


def test_scripts_solo_usan_verbos_de_lectura():
    infractores = []
    for ruta in _scripts():
        for n, linea in enumerate(ruta.read_text().splitlines(), 1):
            limpia = linea.split("#", 1)[0]
            if INVOCA_NUBE.search(limpia) and VERBOS_PROHIBIDOS.search(limpia):
                infractores.append(f"{ruta.relative_to(RAIZ)}:{n}: {linea.strip()}")
    assert not infractores, "verbos de modificación:\n" + "\n".join(infractores)


def test_ningun_script_escribe_fuera_de_datos():
    # Regla de scripts/LEEME.md: la salida va solo a datos/.
    sospechosos = []
    for ruta in _scripts():
        for n, linea in enumerate(ruta.read_text().splitlines(), 1):
            limpia = linea.split("#", 1)[0]
            if re.search(r">\s*(?!/dev/null|&|\"?\$\{?DATOS)[\w./\"$]", limpia) and (
                "datos/" not in limpia and "DATOS" not in limpia
            ):
                sospechosos.append(f"{ruta.relative_to(RAIZ)}:{n}: {linea.strip()}")
    assert not sospechosos, "salida fuera de datos/:\n" + "\n".join(sospechosos)
