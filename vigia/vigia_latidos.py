#!/usr/bin/env python3
"""Vigía de latidos de FinOps: revisa que cada monitor programado siga vivo y envía
UN correo-resumen diario (contrato avisos-correo/v1, receta sin Node).

Diseño: FINOPS_diseno-vigia-de-latidos_2026-11-07.md; anexo 15 de SeguridadGeneral
(AL-09). Solo biblioteca estándar.

Reglas de seguridad (el repositorio es PÚBLICO y el correo reúne datos de terceros):
- Lee solo, por entrada, el último run completado de un workflow (conclusión y
  fecha). Nunca títulos, ramas, commits, mensajes ni logs.
- El texto del correo sale SOLO de constantes, nombres de la lista cerrada,
  enumeraciones, números y fechas. Nada de la API se copia al texto.
- El registro imprime una línea JSON con campos de lista cerrada. Nunca clave,
  token, asunto ni cuerpo (salvo --seco, solo para pruebas locales).
- Los tokens vienen del entorno: VIGIA_TOKEN_<PROPIETARIO> (mayúsculas, no
  alfanuméricos -> «_»). Solo lectura de Actions.

Entorno: AVISOS_RESEND_API_KEY, AVISOS_DE, AVISOS_PARA, VIGIA_TOKEN_*, y opcional
HEARTBEAT_URL (se avisa solo tras enviar el correo).

Estados: vivo | atrasado (horas desde el último ÉXITO > máximo) | fallido (el último
run completado falló y es posterior al último éxito; «cancelled», «skipped» y
«neutral» se ignoran) | sin_datos (sin token, sin éxito o error de la API).

Identidad del aviso: id_unico = vigia-AAAA-MM-DD-HHMM y ocurrido_en truncado al
minuto. Los reintentos de UNA corrida llevan la misma clave y los mismos bytes; un
relanzamiento manual (otro minuto) es otro aviso y consume un envío de la reserva.

Salida: 0 enviado y todo vivo; 20 enviado y hay alguno no vivo (el job falla a
propósito: segundo canal por el correo de fallo de GitHub); 12 reintentos o cuota
agotados; 13 configuración o rechazo del proveedor.
"""

import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

VERSION = "1"
PROYECTO = "finops"
ENLACE = "https://github.com/AndresAlberdi/FinOps/actions"
CONCLUSIONES = {
    "success", "failure", "cancelled", "skipped", "timed_out",
    "action_required", "neutral", "stale", "startup_failure",
}  # fmt: skip
RE_PROYECTO = re.compile(r"^(?!.*\d{5})[a-z][a-z0-9-]{1,29}$")  # sin rachas que el detector rechace
RE_DE = re.compile(r"^alertas-finops@[A-Za-z0-9][A-Za-z0-9.-]{1,100}$")
FALLOS = {"failure", "timed_out", "startup_failure"}
PREFIJOS_SECRETO = ("re_", "bearer ", "ghp_", "gho_", "ghs_", "github_pat_", "akia", "aiza", "xox", "eaa", "eyj", "-----begin")
PRESUPUESTO_S = 240  # tiempo total para consultar a GitHub; el resto pasa a sin_datos
TIMEOUT_S = 15
RE_REPO = re.compile(r"^([A-Za-z0-9][A-Za-z0-9-]{0,38})/([A-Za-z0-9._-]{1,100})$")
RE_WORKFLOW = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,80}\.ya?ml$")
RE_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
MAX_LATIDOS = 25  # que_paso admite 30 líneas
UA = "finops-vigia/1.0"


class _SinRedireccion(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None  # un 3xx es un error: nunca se reenvía Authorization a otro destino


ABRIR = urllib.request.build_opener(_SinRedireccion).open


class ErrorConfig(Exception):
    """Configuración inválida; el mensaje es de lista cerrada, sin valores."""


def cargar_config(ruta):
    try:
        datos = json.loads(Path(ruta).read_text(encoding="utf-8"))
        latidos = datos["latidos"]
    except (OSError, ValueError, KeyError, TypeError):
        raise ErrorConfig("config_ilegible") from None
    if not isinstance(latidos, list) or not 1 <= len(latidos) <= MAX_LATIDOS:
        raise ErrorConfig("config_cantidad")
    vistos = set()
    for e in latidos:
        if not isinstance(e, dict):
            raise ErrorConfig("config_entrada")
        p, r, w, h = (e.get("proyecto"), e.get("repositorio"), e.get("workflow"), e.get("max_horas"))
        if not (isinstance(p, str) and RE_PROYECTO.match(p)):
            raise ErrorConfig("config_proyecto")
        if not (isinstance(r, str) and RE_REPO.match(r)):
            raise ErrorConfig("config_repositorio")
        if not (isinstance(w, str) and RE_WORKFLOW.match(w)):
            raise ErrorConfig("config_workflow")
        if not (isinstance(h, int) and not isinstance(h, bool) and 1 <= h <= 720):
            raise ErrorConfig("config_horas")
        if p in vistos:
            raise ErrorConfig("config_duplicado")
        vistos.add(p)
    return latidos


def nombre_variable_token(repositorio):
    propietario = repositorio.split("/", 1)[0]
    return "VIGIA_TOKEN_" + re.sub(r"[^A-Za-z0-9]", "_", propietario).upper()


def _peticion(url, token=None, cuerpo=None, extra=None, metodo=None):
    cab = {"User-Agent": UA}
    if token:
        cab["Authorization"] = "Bearer " + token
    if extra:
        cab.update(extra)
    datos = None
    if cuerpo is not None:
        datos = json.dumps(cuerpo).encode("utf-8")
        cab["Content-Type"] = "application/json"
    return urllib.request.Request(url, data=datos, headers=cab, method=metodo)


def consultar(entrada, token, estado, abrir=ABRIR, dormir=time.sleep):
    """Último run con `status=<estado>` (success | completed) de un workflow:
    (conclusion, actualizado_en), o None si no hay datos. Un error de red se
    reintenta una vez; cualquier otro fallo es «sin datos», sin propagar texto."""
    url = (
        "https://api.github.com/repos/%s/actions/workflows/%s/runs"
        "?status=%s&per_page=1" % (entrada["repositorio"], entrada["workflow"], estado)
    )
    req = _peticion(
        url, token,
        extra={"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"},
    )  # fmt: skip
    datos = None
    for espera in (0, 2):
        if espera:
            dormir(espera)
        try:
            with abrir(req, timeout=TIMEOUT_S) as r:
                datos = json.load(r)
            break
        except urllib.error.HTTPError:
            return None  # 3xx, 4xx, 5xx de la API: sin datos
        except Exception:  # noqa: BLE001 - red o JSON ilegible
            continue
    try:
        runs = datos["workflow_runs"]
        if not runs:
            return None
        conclusion, actualizado = runs[0]["conclusion"], runs[0]["updated_at"]
        if not (isinstance(conclusion, str) and conclusion in CONCLUSIONES):
            return None
        if not (isinstance(actualizado, str) and RE_FECHA.match(actualizado)):
            return None
        _fecha(actualizado)
    except Exception:  # noqa: BLE001
        return None
    return conclusion, actualizado


def _fecha(texto):
    return datetime.strptime(texto, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def clasificar(exito, ultimo, ahora, max_horas):
    """-> (estado, horas desde el último éxito). `exito` y `ultimo` son (conclusion,
    actualizado_en) o None."""
    if exito is None:
        return "sin_datos", None
    t_exito = _fecha(exito[1])
    horas = max(0, int((ahora - t_exito).total_seconds() // 3600))
    if horas > max_horas:
        return "atrasado", horas
    if ultimo and ultimo[0] in FALLOS and _fecha(ultimo[1]) >= t_exito:
        return "fallido", horas
    return "vivo", horas


def armar_aviso(resultados, ahora):
    """Aviso avisos-correo/v1 con texto de constantes. `resultados`: lista de
    (proyecto, estado, horas)."""
    total = len(resultados)
    vivos = sum(1 for _, e, _ in resultados if e == "vivo")
    nivel = "informativo" if vivos == total else "urgente"
    if nivel == "informativo":
        titular = "Todos los latidos vivos (%d de %d)" % (vivos, total)
        espera = "nada"
        asunto = "Latidos: todos vivos (%d)" % total
    else:
        titular = "%d de %d latidos sin vivir" % (total - vivos, total)
        espera = "Revisar los latidos marcados; Claude propone el arreglo y usted autoriza"
        asunto = "Latidos: %d de %d sin vivir" % (total - vivos, total)
    lineas = [titular]
    for proyecto, estado, horas in resultados:
        lineas.append(
            "%s: %s%s" % (proyecto, estado, "" if horas is None else " (hace %d h)" % horas)
        )
    fecha = ahora.strftime("%Y-%m-%d-%H%M")
    return {
        "contrato": "avisos-correo/v1",
        "nivel": nivel,
        "proyecto": PROYECTO,
        "asunto": asunto,
        "que_paso": "\n".join(lineas),
        "que_se_espera_de_andres": espera,
        "enlace": ENLACE,
        "ocurrido_en": ahora.strftime("%Y-%m-%dT%H:%M:00Z"),
        "id_unico": "vigia-" + fecha,
    }


def validar_aviso(a):
    """Validador MÍNIMO (no espejo completo del corpus de WAM: se declara en la ficha,
    como la receta curl). Si algo no cuadra, el envío se aborta; nunca se redacta."""
    if a["contrato"] != "avisos-correo/v1" or a["nivel"] not in ("urgente", "aviso", "informativo"):
        return False
    if not RE_PROYECTO.match(a["proyecto"]) or a["enlace"] != ENLACE:
        return False
    textos = [a["asunto"], a["que_paso"], a["que_se_espera_de_andres"], a["proyecto"]]
    if not 3 <= len(a["asunto"]) <= 100 or "\n" in a["asunto"]:
        return False
    if not 1 <= len(a["que_paso"]) <= 1500 or len(a["que_paso"].split("\n")[0]) > 110:
        return False
    if len(a["que_paso"].split("\n")) > 30:
        return False
    if not 1 <= len(a["que_se_espera_de_andres"]) <= 180:
        return False
    if not re.match(r"^[A-Za-z0-9][A-Za-z0-9._:-]{7,119}$", a["id_unico"]):
        return False
    if not RE_FECHA.match(a["ocurrido_en"]):
        return False
    for t in textos:
        if re.search(r"[A-Za-z0-9+/=_-]{32,}", t):  # palabra larga: posible secreto
            return False
        if "+" in t and re.search(r"\+\d", t):
            return False
        if re.search(r"\d{7,}", t) or re.search(r"(?<!\d)\d{6}(?!\d)", t):
            return False
        if "@" in t or "://" in t or "www." in t:
            return False
        bajo = t.lower()
        if any(x in bajo for x in PREFIJOS_SECRETO) or "localhost" in bajo:
            return False
        if re.search(r"\d+\.\d+\.\d+\.\d+|\.internal|\.local", bajo):
            return False
    return True


def formatear(a):
    nivel = a["nivel"].upper()
    asunto = "[AAB1 %s] %s · %s" % (nivel, a["proyecto"], a["asunto"])
    primera, _, resto = a["que_paso"].partition("\n")
    cuerpo = "%s · %s · %s\nQué se espera de Andres: %s\nQué pasó: %s\n" % (
        nivel, a["proyecto"], a["ocurrido_en"], a["que_se_espera_de_andres"], primera,
    )  # fmt: skip
    if resto:
        cuerpo += resto + "\n"
    cuerpo += "Enlace: %s\n\nref %s:%s · contrato avisos-correo/v1\n" % (
        a["enlace"], a["proyecto"], a["id_unico"],
    )  # fmt: skip
    cuerpo += (
        "Aviso automático; responder a este correo no llega a nadie.\n"
        "Las acciones las ejecuta Claude con la autorización de Andres.\n"
    )
    return asunto, cuerpo


def _nombre_error(e):
    """Solo el código enumerado `name` del cuerpo de error de Resend; nada más."""
    try:
        nombre = json.load(e).get("name")
    except Exception:  # noqa: BLE001
        return ""
    return nombre if isinstance(nombre, str) and re.match(r"^[a-z_]{1,60}$", nombre) else ""


REINTENTABLES = {"concurrent_idempotent_requests", "rate_limit_exceeded"}
CUOTA = {"daily_quota_exceeded", "monthly_quota_exceeded"}


def enviar(aviso, clave, de, para, abrir=ABRIR, dormir=time.sleep):
    """POST a Resend con la misma Idempotency-Key. Devuelve un detalle de lista
    cerrada: enviado | reintentos_agotados | cuota_agotada | rechazo_proveedor."""
    asunto, cuerpo = formatear(aviso)
    carga = {
        "from": "AAB1 avisos · finops <%s>" % de,
        "to": [para],
        "subject": asunto,
        "text": cuerpo,
        "html": "<pre>%s</pre>" % html.escape(cuerpo),
    }
    llave = "%s:%s" % (aviso["proyecto"], aviso["id_unico"])
    for espera in (0, 1, 4):
        if espera:
            dormir(espera)
        req = _peticion(
            "https://api.resend.com/emails", clave, carga,
            extra={"Idempotency-Key": llave}, metodo="POST",
        )  # fmt: skip
        try:
            with abrir(req, timeout=TIMEOUT_S) as r:
                if r.status != 200:
                    return "rechazo_proveedor"
                return "enviado"
        except urllib.error.HTTPError as e:
            nombre = _nombre_error(e)
            if e.code >= 500 or nombre in REINTENTABLES:
                continue
            if nombre in CUOTA:
                return "cuota_agotada"
            return "rechazo_proveedor"  # el resto de los 4xx, incluido un 409 de carga distinta
        except Exception:  # noqa: BLE001 - red
            continue
    return "reintentos_agotados"


def latido(url, abrir=ABRIR):
    try:
        with abrir(_peticion(url), timeout=10):
            pass
    except Exception:  # noqa: BLE001 - el latido es un aviso aparte; no rompe el trabajo
        pass


def linea_registro(aviso, resultado, detalle, vivos=None, total=None):
    return json.dumps(
        {
            "evento": "vigia_latidos",
            "proyecto": PROYECTO,
            "ref": "%s:%s" % (PROYECTO, aviso["id_unico"]) if aviso else "",
            "nivel": aviso["nivel"] if aviso else "",
            "resultado": resultado,
            "detalle": detalle,
            "vivos": vivos,
            "total": total,
            "version": VERSION,
        },
        ensure_ascii=True,
    )


def ejecutar(ruta_config, entorno, ahora, abrir=ABRIR, dormir=time.sleep, seco=False, reloj=time.monotonic):
    try:
        latidos = cargar_config(ruta_config)
    except ErrorConfig as e:
        print(linea_registro(None, "error", str(e)))
        return 13
    inicio = reloj()
    resultados = []
    for e in latidos:
        token = entorno.get(nombre_variable_token(e["repositorio"]), "")
        exito = ultimo = None
        if token and reloj() - inicio < PRESUPUESTO_S:
            exito = consultar(e, token, "success", abrir, dormir)
            ultimo = consultar(e, token, "completed", abrir, dormir) if exito else None
        estado, horas = clasificar(exito, ultimo, ahora, e["max_horas"])
        resultados.append((e["proyecto"], estado, horas))
    vivos = sum(1 for _, est, _ in resultados if est == "vivo")
    aviso = armar_aviso(resultados, ahora)
    if not validar_aviso(aviso):
        print(linea_registro(None, "error", "aviso_invalido"))
        return 13
    if seco:
        asunto, cuerpo = formatear(aviso)
        print(asunto)
        print(cuerpo)
        return 0
    clave, de, para = (entorno.get(k, "") for k in ("AVISOS_RESEND_API_KEY", "AVISOS_DE", "AVISOS_PARA"))
    if not (clave and para and RE_DE.match(de)):
        print(linea_registro(aviso, "error", "configuracion", vivos, len(resultados)))
        return 13
    detalle = enviar(aviso, clave, de, para, abrir, dormir)
    print(linea_registro(aviso, "ok" if detalle == "enviado" else "error", detalle, vivos, len(resultados)))
    if detalle == "enviado":
        if entorno.get("HEARTBEAT_URL"):
            latido(entorno["HEARTBEAT_URL"], abrir)
        return 0 if aviso["nivel"] == "informativo" else 20
    return 12 if detalle in ("reintentos_agotados", "cuota_agotada") else 13


def main(argv):
    ruta = Path(__file__).resolve().parent / "latidos.json"
    return ejecutar(ruta, os.environ, datetime.now(timezone.utc), seco="--seco" in argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
