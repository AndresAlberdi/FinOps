"""Pruebas de vigia/vigia_latidos.py con datos simulados (sin red)."""

import importlib.util
import io
import json
import urllib.error
import urllib.parse
from datetime import UTC, datetime
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
ESPEC = importlib.util.spec_from_file_location(
    "vg", RAIZ / "vigia" / "vigia_latidos.py"
)
vg = importlib.util.module_from_spec(ESPEC)
ESPEC.loader.exec_module(vg)

AHORA = datetime(2026, 11, 8, 12, 30, 0, tzinfo=UTC)
ENTRADA = {"proyecto": "wam", "repositorio": "segurolotengopy/WhatsAppModular",
           "workflow": "latido-receptor.yml", "max_horas": 14}  # fmt: skip


class Resp(io.BytesIO):
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def run(conclusion="success", actualizado="2026-11-08T10:30:00Z"):
    runs = [
        {
            "conclusion": conclusion,
            "updated_at": actualizado,
            "display_title": "SECRETO",
        }
    ]
    return Resp(json.dumps({"workflow_runs": runs}).encode())


def vacio():
    return Resp(b'{"workflow_runs": []}')


def error(codigo, nombre=None):
    cuerpo = (
        io.BytesIO(json.dumps({"name": nombre, "message": "TEXTO"}).encode())
        if nombre
        else None
    )
    return urllib.error.HTTPError("u", codigo, "x", {}, cuerpo)


def config(tmp_path, entradas=None):
    ruta = tmp_path / "l.json"
    ruta.write_text(json.dumps({"version": 1, "latidos": entradas or [ENTRADA]}))
    return ruta


def entorno(**extra):
    e = {"AVISOS_RESEND_API_KEY": "re_clave", "AVISOS_DE": "alertas-finops@avisos.aab1.website",
         "AVISOS_PARA": "a@b.c", "VIGIA_TOKEN_SEGUROLOTENGOPY": "tok"}  # fmt: skip
    e.update(extra)
    return e


def host(url):
    # host exacto de la URL, no una subcadena (CodeQL: incomplete-url-substring-sanitization)
    return urllib.parse.urlsplit(url).hostname


def abridor(exito=None, completado=None, resend=None, vistos=None):
    """GitHub responde según `status=` de la URL; Resend, con la función `resend`."""
    exito = exito if exito is not None else run()
    completado = completado if completado is not None else run()

    def abrir(req, timeout):
        url = req.full_url
        if vistos is not None:
            vistos.append(
                (url, {k.lower(): v for k, v in req.header_items()}, req.data)
            )
        if host(url) == "api.github.com":
            resp = exito if "status=success" in url else completado
            if isinstance(resp, Exception):
                raise resp
            return Resp(resp.getvalue())
        if host(url) == "api.resend.com":
            return resend() if resend else Resp(b"{}")
        return Resp(b"{}")  # latido

    return abrir


def sin_espera(s):
    return None


def correr(tmp_path, env=None, abrir=None, **kw):
    return vg.ejecutar(
        config(tmp_path), env or entorno(), AHORA, abrir or abridor(), sin_espera, **kw
    )


# --- configuración -----------------------------------------------------------


def test_la_config_real_es_valida():
    assert vg.cargar_config(RAIZ / "vigia" / "latidos.json")


@pytest.mark.parametrize("campo,valor", [
    ("proyecto", "WAM"), ("proyecto", "p123456"), ("repositorio", "sin-barra"),
    ("workflow", "../x.sh"), ("max_horas", 0), ("max_horas", True), ("max_horas", 9999),
])  # fmt: skip
def test_config_invalida_se_rechaza(tmp_path, campo, valor):
    with pytest.raises(vg.ErrorConfig):
        vg.cargar_config(config(tmp_path, [{**ENTRADA, campo: valor}]))


def test_proyecto_duplicado_se_rechaza(tmp_path):
    with pytest.raises(vg.ErrorConfig):
        vg.cargar_config(config(tmp_path, [ENTRADA, ENTRADA]))


def test_nombre_de_la_variable_del_token():
    assert (
        vg.nombre_variable_token("AndresAlberdi/FinOps") == "VIGIA_TOKEN_ANDRESALBERDI"
    )
    assert (
        vg.nombre_variable_token("segurolotengopy/x") == "VIGIA_TOKEN_SEGUROLOTENGOPY"
    )


# --- estados -----------------------------------------------------------------

EXITO = ("success", "2026-11-08T10:30:00Z")


def test_clasificar_los_cuatro_estados():
    assert vg.clasificar(EXITO, EXITO, AHORA, 14) == ("vivo", 2)
    assert vg.clasificar(EXITO, ("failure", "2026-11-08T11:30:00Z"), AHORA, 14) == (
        "fallido",
        2,
    )
    assert (
        vg.clasificar(("success", "2026-11-07T10:30:00Z"), None, AHORA, 14)[0]
        == "atrasado"
    )
    assert vg.clasificar(None, None, AHORA, 14) == ("sin_datos", None)


def test_un_fallo_anterior_al_exito_no_cuenta():
    assert (
        vg.clasificar(EXITO, ("failure", "2026-11-08T09:00:00Z"), AHORA, 14)[0]
        == "vivo"
    )


def test_cancelado_u_omitido_no_vuelve_fallido_un_latido_vivo():
    for c in ("cancelled", "skipped", "neutral"):
        assert vg.clasificar(EXITO, (c, "2026-11-08T11:30:00Z"), AHORA, 14)[0] == "vivo"


def test_las_horas_son_desde_el_ultimo_exito_aunque_falle_a_diario():
    viejo = ("success", "2026-10-29T10:30:00Z")  # 242 h
    est, horas = vg.clasificar(viejo, ("failure", "2026-11-08T12:00:00Z"), AHORA, 14)
    assert est == "atrasado" and horas == 242


def test_consultar_solo_toma_conclusion_y_fecha():
    assert (
        vg.consultar(ENTRADA, "t", "success", lambda r, timeout: run(), sin_espera)
        == EXITO
    )


@pytest.mark.parametrize("respuesta", [
    lambda r, timeout: Resp(b"no es json"),
    lambda r, timeout: vacio(),
    lambda r, timeout: run(conclusion="<script>"),
    lambda r, timeout: Resp(b'{"workflow_runs":[{"conclusion":["x"],"updated_at":"2026-11-08T10:30:00Z"}]}'),
    lambda r, timeout: run(actualizado="ayer"),
    lambda r, timeout: run(actualizado="2026-02-30T10:00:00Z"),
])  # fmt: skip
def test_respuestas_raras_son_sin_datos(respuesta):
    assert vg.consultar(ENTRADA, "t", "success", respuesta, sin_espera) is None


def test_error_de_red_se_reintenta_una_vez_y_luego_es_sin_datos():
    llamadas = []

    def falla(r, timeout):
        llamadas.append(1)
        raise urllib.error.URLError("x")

    assert vg.consultar(ENTRADA, "t", "success", falla, sin_espera) is None
    assert len(llamadas) == 2


def test_error_http_de_la_api_es_sin_datos_sin_reintento():
    llamadas = []

    def falla(r, timeout):
        llamadas.append(1)
        raise error(404)

    assert vg.consultar(ENTRADA, "t", "success", falla, sin_espera) is None
    assert len(llamadas) == 1


def test_no_se_siguen_redirecciones():
    manejador = vg._SinRedireccion()
    assert (
        manejador.redirect_request(None, None, 302, "x", {}, "http://otro.host") is None
    )


def test_el_presupuesto_de_tiempo_deja_el_resto_en_sin_datos(tmp_path, capsys):
    reloj = iter([0, 0, 10_000, 10_000, 10_000]).__next__
    entradas = [ENTRADA, {**ENTRADA, "proyecto": "otro", "workflow": "o.yml"}]
    vistos = []
    rc = vg.ejecutar(config(tmp_path, entradas), entorno(), AHORA, abridor(vistos=vistos),
                     sin_espera, reloj=reloj)  # fmt: skip
    consultas = [v for v in vistos if host(v[0]) == "api.github.com"]
    assert rc == 20 and len(consultas) == 2  # solo la primera entrada se consultó


# --- aviso -------------------------------------------------------------------


def test_aviso_informativo_y_urgente():
    a = vg.armar_aviso([("wam", "vivo", 2)], AHORA)
    assert (a["nivel"], a["que_se_espera_de_andres"], a["id_unico"]) == (
        "informativo",
        "nada",
        "vigia-2026-11-08-1230",
    )
    assert a["ocurrido_en"] == "2026-11-08T12:30:00Z" and vg.validar_aviso(a)
    b = vg.armar_aviso([("wam", "vivo", 2), ("oci", "atrasado", 30)], AHORA)
    assert b["nivel"] == "urgente" and vg.validar_aviso(b)


def test_primeros_400_caracteres_llevan_lo_esencial_incluso_con_25_entradas():
    a = vg.armar_aviso([(f"proy{i}", "atrasado", 300) for i in range(25)], AHORA)
    assert vg.validar_aviso(a)
    asunto, cuerpo = vg.formatear(a)
    assert "URGENTE" in asunto
    for esperado in ("URGENTE", "finops", "Qué se espera de Andres", "Qué pasó"):
        assert esperado in cuerpo[:400]


@pytest.mark.parametrize("texto", [
    "x@y.com", "https://x.com", "1234567", "123456", "+59171234567", "a" * 32,
    "re_abc", "AKIAxx", "eyJhb", "10.0.0.1", "localhost", "x.internal", "Bearer z",
])  # fmt: skip
def test_el_validador_rechaza_lo_prohibido_en_texto_y_asunto(texto):
    a = vg.armar_aviso([("wam", "vivo", 2)], AHORA)
    b = dict(a, que_paso=a["que_paso"] + "\n" + texto)
    c = dict(a, asunto=texto + " asunto")
    assert not vg.validar_aviso(b) and not vg.validar_aviso(c)


# --- ejecución ---------------------------------------------------------------


def test_todo_vivo_sale_0_envia_y_avisa_el_latido(tmp_path, capsys):
    vistos = []
    rc = correr(
        tmp_path,
        entorno(HEARTBEAT_URL="https://hc.example/ping"),
        abridor(vistos=vistos),
    )
    linea = json.loads(capsys.readouterr().out)
    assert (
        rc == 0
        and linea["resultado"] == "ok"
        and (linea["vivos"], linea["total"]) == (1, 1)
    )
    urls = [v[0] for v in vistos]
    assert "https://api.resend.com/emails" in urls and "https://hc.example/ping" in urls
    envio = next(v for v in vistos if v[0].endswith("/emails"))
    assert envio[1]["idempotency-key"] == "finops:vigia-2026-11-08-1230"
    assert json.loads(envio[2])["from"].endswith("<alertas-finops@avisos.aab1.website>")


def test_algo_atrasado_sale_20_para_fallar_a_proposito(tmp_path, capsys):
    rc = correr(tmp_path, abrir=abridor(exito=run(actualizado="2026-11-06T10:30:00Z")))
    assert rc == 20 and json.loads(capsys.readouterr().out)["nivel"] == "urgente"


def test_fallido_de_punta_a_punta(tmp_path, capsys):
    rc = correr(
        tmp_path, abrir=abridor(completado=run("failure", "2026-11-08T11:30:00Z"))
    )
    assert rc == 20


def test_sin_token_es_sin_datos_urgente_y_no_consulta_github(tmp_path, capsys):
    e = entorno()
    del e["VIGIA_TOKEN_SEGUROLOTENGOPY"]
    vistos = []
    rc = correr(tmp_path, e, abridor(vistos=vistos))
    assert rc == 20 and not any(host(v[0]) == "api.github.com" for v in vistos)


def test_el_registro_nunca_trae_clave_ni_titulos_ni_estado_por_entrada(
    tmp_path, capsys
):
    correr(tmp_path)
    salida = capsys.readouterr().out
    for prohibido in (
        "re_clave",
        "SECRETO",
        "tok",
        "a@b.c",
        "Qué pasó",
        "wam",
        "atrasado",
    ):
        assert prohibido not in salida


def test_5xx_se_reintenta_con_la_misma_clave_y_luego_agota(tmp_path, capsys):
    vistos = []

    def resend():
        raise error(500)

    rc = correr(tmp_path, abrir=abridor(resend=resend, vistos=vistos))
    llaves = [v[1]["idempotency-key"] for v in vistos if v[0].endswith("/emails")]
    assert rc == 12 and llaves == ["finops:vigia-2026-11-08-1230"] * 3


def test_error_de_red_en_resend_se_reintenta_y_no_avisa_el_latido(tmp_path, capsys):
    vistos = []

    def resend():
        raise urllib.error.URLError("x")

    rc = correr(tmp_path, entorno(HEARTBEAT_URL="https://hc.example/ping"),
                abridor(resend=resend, vistos=vistos))  # fmt: skip
    assert rc == 12 and not any("hc.example" in v[0] for v in vistos)


def test_409_concurrente_se_reintenta_y_otro_409_no(tmp_path, capsys):
    cuenta = []

    def concurrente():
        cuenta.append(1)
        raise error(409, "concurrent_idempotent_requests")

    assert (
        correr(tmp_path, abrir=abridor(resend=concurrente)) == 12 and len(cuenta) == 3
    )
    cuenta.clear()

    def distinta():
        cuenta.append(1)
        raise error(409, "invalid_idempotent_request")

    assert correr(tmp_path, abrir=abridor(resend=distinta)) == 13 and len(cuenta) == 1


def test_429_limite_de_frecuencia_se_reintenta_y_la_cuota_sale_12(tmp_path, capsys):
    cuenta = []

    def frecuencia():
        cuenta.append(1)
        raise error(429, "rate_limit_exceeded")

    assert correr(tmp_path, abrir=abridor(resend=frecuencia)) == 12 and len(cuenta) == 3
    cuenta.clear()

    def cuota():
        cuenta.append(1)
        raise error(429, "daily_quota_exceeded")

    assert correr(tmp_path, abrir=abridor(resend=cuota)) == 12 and len(cuenta) == 1
    assert (
        json.loads(capsys.readouterr().out.splitlines()[-1])["detalle"]
        == "cuota_agotada"
    )


def test_otro_4xx_no_se_reintenta_y_sale_13(tmp_path, capsys):
    cuenta = []

    def invalido():
        cuenta.append(1)
        raise error(422, "validation_error")

    assert correr(tmp_path, abrir=abridor(resend=invalido)) == 13 and len(cuenta) == 1


def test_un_3xx_de_resend_no_es_exito():
    class Otro(Resp):
        status = 302

    aviso = vg.armar_aviso([("wam", "vivo", 2)], AHORA)
    assert vg.enviar(aviso, "k", "alertas-finops@x.y", "a@b.c", lambda r, timeout: Otro(b""),
                     sin_espera) == "rechazo_proveedor"  # fmt: skip


@pytest.mark.parametrize("de", ["", "alertas-wam@avisos.aab1.website", "otro@x.y"])
def test_remitente_incoherente_sale_13(tmp_path, de):
    assert correr(tmp_path, entorno(AVISOS_DE=de)) == 13


def test_sin_clave_sale_13(tmp_path):
    e = entorno()
    del e["AVISOS_RESEND_API_KEY"]
    assert correr(tmp_path, e) == 13


def test_config_invalida_sale_13_con_registro_cerrado(tmp_path, capsys):
    ruta = tmp_path / "x.json"
    ruta.write_text("no es json")
    assert vg.ejecutar(ruta, entorno(), AHORA, abridor(), sin_espera) == 13
    linea = json.loads(capsys.readouterr().out)
    assert set(linea) == {"evento", "proyecto", "ref", "nivel", "resultado", "detalle",
                          "vivos", "total", "version"}  # fmt: skip


def test_el_workflow_no_usa_disparadores_peligrosos_ni_permisos_de_mas():
    lineas = (
        (RAIZ / ".github" / "workflows" / "vigia-latidos.yml").read_text().splitlines()
    )
    texto = "\n".join(x for x in lineas if not x.lstrip().startswith("#"))
    assert "pull_request" not in texto and "id-token" not in texto
    assert "contents: write" not in texto
