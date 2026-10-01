"""Pruebas de scripts/meta/pricing_analytics.py con respuestas simuladas de Meta."""

import importlib.util
import io
import json
import urllib.error
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ESPEC = importlib.util.spec_from_file_location(
    "pa", RAIZ / "scripts" / "meta" / "pricing_analytics.py"
)
pa = importlib.util.module_from_spec(ESPEC)
ESPEC.loader.exec_module(pa)

RESPUESTA = {
    "pricing_analytics": {
        "data": [
            {
                "data_points": [
                    {
                        "pricing_category": "SERVICE",
                        "pricing_type": "REGULAR",
                        "country": "BO",
                        "volume": 1500,
                        "cost": 5.65,
                    },
                    {
                        "pricing_category": "SERVICE",
                        "pricing_type": "REGULAR",
                        "country": "BO",
                        "volume": 500,
                        "cost": 1.88,
                    },
                    {
                        "pricing_category": "MARKETING",
                        "pricing_type": "REGULAR",
                        "country": "BO",
                        "volume": 10,
                        "cost": 0.74,
                    },
                    {
                        "pricing_category": "SERVICE",
                        "pricing_type": "FREE_CUSTOMER_SERVICE",
                        "country": "BO",
                        "volume": 900,
                        "cost": 0,
                    },
                ]
            }
        ]
    },
    "id": "123456789012345",
}


def test_ultimos_oculta_el_identificador():
    assert pa.ultimos("123456789012345") == "…2345"
    assert "123456789" not in pa.ultimos("123456789012345")


def test_rango_del_mes_cubre_octubre_completo():
    inicio, fin = pa.rango_del_mes("2026-10")
    assert (fin - inicio) == 31 * 86400 - 1


def test_la_url_lleva_el_campo_y_nunca_el_token():
    url = pa.construir_url("999", "2026-10", "v23.0")
    assert url.startswith("https://graph.facebook.com/v23.0/999?")
    assert "pricing_analytics" in url and "granularity%28MONTHLY%29" in url
    assert "access_token" not in url and "Bearer" not in url


def test_agregar_suma_por_categoria_tipo_y_pais():
    r = pa.agregar(RESPUESTA)
    assert r["SERVICE/REGULAR/BO"] == {"costo": 7.53, "volumen": 2000}
    assert r["SERVICE/FREE_CUSTOMER_SERVICE/BO"]["costo"] == 0
    assert round(sum(v["costo"] for v in r.values()), 2) == 8.27


def test_agregar_tolera_respuestas_vacias():
    assert pa.agregar({}) == {}
    assert pa.agregar({"pricing_analytics": {"data": []}}) == {}


def test_leer_token_y_wabas(tmp_path):
    t = tmp_path / "token"
    t.write_text("  secreto-de-prueba \n")
    assert pa.leer_token(t) == "secreto-de-prueba"
    w = tmp_path / "wabas.txt"
    w.write_text("# comentario\n111222333 NovuChat demo\n444555666\n\n")
    assert pa.leer_wabas(w) == [("111222333", "NovuChat demo"), ("444555666", "…5666")]


def test_token_vacio_o_ausente_falla(tmp_path):
    for ruta in (tmp_path / "no-existe", tmp_path / "vacio"):
        if ruta.name == "vacio":
            ruta.write_text("")
        try:
            pa.leer_token(ruta)
        except SystemExit:
            continue
        raise AssertionError("debió fallar")


def test_consultar_envia_el_token_solo_en_la_cabecera(monkeypatch):
    vistos = {}

    class Respuesta(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def falso(peticion, timeout):
        vistos["url"], vistos["cab"], vistos["metodo"] = (
            peticion.full_url,
            dict(peticion.header_items()),
            peticion.get_method(),
        )
        return Respuesta(json.dumps(RESPUESTA).encode())

    monkeypatch.setattr(pa.urllib.request, "urlopen", falso)
    r = pa.consultar("999", "2026-10", "tok-secreto", "v23.0")
    assert r["id"] == "123456789012345"
    assert vistos["metodo"] == "GET"
    assert vistos["cab"]["Authorization"] == "Bearer tok-secreto"
    assert "tok-secreto" not in vistos["url"]


def test_consultar_devuelve_el_error_http_sin_fallar(monkeypatch):
    def falso(peticion, timeout):
        raise urllib.error.HTTPError(
            peticion.full_url, 190, "x", {}, io.BytesIO(b'{"error":"token"}')
        )

    monkeypatch.setattr(pa.urllib.request, "urlopen", falso)
    r = pa.consultar("999", "2026-10", "t", "v23.0")
    assert r["error"]["http"] == 190


def test_main_no_imprime_el_token_ni_el_id_completo(tmp_path, monkeypatch, capsys):
    (tmp_path / "token").write_text("TOKEN-SUPER-SECRETO")
    (tmp_path / "wabas.txt").write_text("987654321098765 Demo\n")
    monkeypatch.setattr(pa, "DATOS", tmp_path)
    monkeypatch.setattr(pa, "consultar", lambda *a, **k: RESPUESTA)
    monkeypatch.setenv("META_TOKEN_FILE", str(tmp_path / "token"))
    assert pa.main(["--mes", "2026-10"]) == 0
    salida = capsys.readouterr()
    assert "TOKEN-SUPER-SECRETO" not in salida.out + salida.err
    assert "987654321098765" not in salida.out + salida.err
    assert "USD 8.2700" in salida.out
    assert (tmp_path / "resumen-2026-10.json").exists()
