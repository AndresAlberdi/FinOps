"""Pruebas de scripts/github/minutos_actions.py con datos simulados."""

import importlib.util
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ESPEC = importlib.util.spec_from_file_location(
    "ma", RAIZ / "scripts" / "github" / "minutos_actions.py"
)
ma = importlib.util.module_from_spec(ESPEC)
ESPEC.loader.exec_module(ma)


def test_un_trabajo_se_redondea_hacia_arriba():
    assert ma.minutos_trabajo("2026-09-01T10:00:00Z", "2026-09-01T10:00:01Z") == 1
    assert ma.minutos_trabajo("2026-09-01T10:00:00Z", "2026-09-01T10:03:01Z") == 4
    assert ma.minutos_trabajo("2026-09-01T10:00:00Z", "2026-09-01T10:03:00Z") == 3


def test_trabajo_sin_fechas_o_con_duracion_cero_no_cuenta():
    assert ma.minutos_trabajo("", "") == 0
    assert ma.minutos_trabajo("2026-09-01T10:00:00Z", "2026-09-01T10:00:00Z") == 0


def test_resumir_descarta_el_artefacto_de_24_horas_y_separa_dependabot():
    trabajos = [
        ("1", "2026-09-01T10:00:00Z", "2026-09-01T10:04:00Z", "success"),
        ("2", "2026-09-01T10:00:00Z", "2026-09-02T10:00:00Z", "cancelled"),
        ("3", "2026-09-01T10:00:00Z", "2026-09-01T10:06:00Z", "success"),
    ]
    r = ma.resumir(trabajos, {"1": "pull_request", "2": "dynamic", "3": "dynamic"})
    assert r == {
        "CI y demás": 4,
        "descartados (>6 h, artefacto)": 1440,
        "Dependabot": 6,
    }


def test_cuota_usada_con_y_sin_dependabot():
    base, total, pct = ma.cuota_usada({"CI y demás": 2750, "Dependabot": 208}, 3000)
    assert (base, total, pct) == (2750, 2958, 98.6)
    assert ma.cuota_usada({}, 0) == (0, 0, 0.0)


def test_rango_del_mes():
    assert ma.rango("2026-09") == "2026-09-01..2026-09-30"
    assert ma.rango("2026-02") == "2026-02-01..2026-02-28"


def test_leer_repos(tmp_path):
    f = tmp_path / "repos.txt"
    f.write_text(
        "# cuentas\nAndresAlberdi/SeguridadGeneral\nsegurolotengopy/WhatsAppModular /home/x/.config/gh-pro\n\n"
    )
    assert ma.leer_repos(f) == [
        ("AndresAlberdi/SeguridadGeneral", None),
        ("segurolotengopy/WhatsAppModular", "/home/x/.config/gh-pro"),
    ]


def test_medir_con_gh_simulado(monkeypatch):
    def falso(argumentos, config):
        if "runs?created" in argumentos[1]:
            return "11\tpull_request\n12\tdynamic\n"
        return "2026-09-01T10:00:00Z\t2026-09-01T10:05:00Z\tsuccess\n"

    monkeypatch.setattr(ma, "gh", falso)
    r = ma.medir("o/r", None, "2026-09")
    assert r == {"ejecuciones": 2, "CI y demás": 5, "Dependabot": 5}
