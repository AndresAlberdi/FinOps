"""Prueba de scripts/local/con-limite.sh: el tope mata al comando, no a quien lo lanza."""

import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "local" / "con-limite.sh"


def _systemd_de_usuario_disponible() -> bool:
    if shutil.which("systemd-run") is None:
        return False
    try:
        r = subprocess.run(
            ["systemd-run", "--user", "--scope", "--quiet", "true"],
            check=False,
            capture_output=True,
            timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return r.returncode == 0


needs_systemd = pytest.mark.skipif(
    not _systemd_de_usuario_disponible(),
    reason="requiere systemd --user con cgroups delegados",
)


def _correr(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(SCRIPT), *args], check=False, capture_output=True, text=True, timeout=60
    )


def test_sin_comando_da_uso_y_codigo_2():
    r = _correr()
    assert r.returncode == 2
    assert "uso:" in r.stderr


@pytest.mark.parametrize("tope", ["0G", "6", "abc", "-1G", "1.5G", "6GB"])
def test_tope_invalido_se_rechaza(tope):
    r = _correr("-m", tope, "--", "true")
    assert r.returncode == 2
    assert "inválido" in r.stderr


def test_m_sin_valor_da_uso():
    assert _correr("-m").returncode == 2


@needs_systemd
def test_comando_dentro_del_tope_termina_bien():
    r = _correr("-m", "300M", "--", "python3", "-c", "b = bytearray(50 * 1024 * 1024)")
    assert r.returncode == 0


@needs_systemd
def test_comando_que_supera_el_tope_muere_por_sigkill():
    r = _correr("-m", "200M", "--", "python3", "-c", "b = bytearray(600 * 1024 * 1024)")
    # SIGKILL: -9 para Python, 137 en una terminal
    assert r.returncode in (-9, 137)


@needs_systemd
def test_devuelve_el_codigo_de_salida_del_comando():
    r = _correr("--", "python3", "-c", "raise SystemExit(7)")
    assert r.returncode == 7
