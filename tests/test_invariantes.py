"""Automatiza las verificaciones de CLAUDE.md que no dependen de una persona.

Reglas (CLAUDE.md, «Verificación antes de terminar»): ningún script de scripts/
usa verbos de modificación, ninguno escribe fuera de datos/, y git ignora datos/.

Los revisores (`revisar_sh`, `revisar_py`) son funciones puras para poder probarlas
con casos positivos y negativos aunque scripts/ esté vacío. El de shell analiza
cada comando por su CLI y su subcomando (no busca palabras sueltas), de modo que
una opción como `--start-time` o un argumento como `export/` no dan falsos positivos.
"""

import re
import shlex
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# --- Shell ---------------------------------------------------------------------

DATOS_OK = ("datos/", "./datos/", "$DATOS", "${DATOS", "/dev/null")
SEPARADOR = re.compile(r"\s*(?:&&|\|\||;|\|)\s*")

AWS_LECTURA = ("get", "list", "describe", "head", "lookup", "batch-get", "filter")
GCLOUD_ESCRIBE = {
    "create", "delete", "update", "patch", "deploy", "enable", "disable", "import",
    "add-iam-policy-binding", "remove-iam-policy-binding", "set-iam-policy",
    "set", "unset", "start", "stop", "restart", "resize", "move", "undelete",
    "apply", "destroy", "attach", "detach", "add", "remove", "reset", "rotate",
    "login", "revoke", "activate-service-account", "submit", "cancel", "rollback",
}  # fmt: skip
GSUTIL_LECTURA = {"ls", "cat", "stat", "du", "hash", "version", "help"}
BQ_LECTURA = {"ls", "show", "head", "query", "version", "info", "help"}
BQ_DML = re.compile(
    r"\b(insert|update|delete|merge|create|drop|alter|truncate|grant|revoke)\b",
    re.IGNORECASE,
)
GH_ESCRIBE = {
    "merge", "create", "close", "reopen", "review", "comment", "edit", "delete",
    "ready", "lock", "unlock", "transfer", "rerun", "cancel", "run", "set", "enable",
    "disable", "fork", "sync", "archive", "unarchive", "rename", "upload", "add",
    "remove", "login", "logout", "refresh", "switch", "setup-git",
}  # fmt: skip
KUBECTL_ESCRIBE = {
    "apply", "create", "delete", "edit", "patch", "replace", "scale", "rollout", "exec",
    "cp", "drain", "cordon", "uncordon", "taint", "label", "annotate", "set", "run",
    "expose", "autoscale", "attach",
}  # fmt: skip
TERRAFORM_ESCRIBE = {"apply", "destroy", "import", "taint", "untaint", "force-unlock"}
LOCALES = {"rm", "mv", "cp", "touch", "mkdir", "ln", "dd", "install", "truncate", "tee"}


def _es_datos(ruta: str) -> bool:
    ruta = ruta.strip("\"'")
    return ruta.startswith(DATOS_OK) or "/datos/" in ruta


def _redirecciones(linea: str) -> list[str]:
    """Destinos de `>` y `>>` fuera de comillas, de (( )) y de [[ ]]."""
    destinos, comilla, i, n = [], "", 0, len(linea)
    anidado = 0  # profundidad de (( )) o [[ ]]
    while i < n:
        c = linea[i]
        if comilla:
            if c == comilla:
                comilla = ""
        elif c in "\"'":
            comilla = c
        elif linea.startswith(("((", "[["), i):
            anidado += 1
            i += 1
        elif linea.startswith(("))", "]]"), i) and anidado:
            anidado -= 1
            i += 1
        elif c == ">" and not anidado:
            previo = linea[i - 1] if i else ""
            if previo in "=-" or linea[i + 1 : i + 2] == "&":
                i += 1
                continue
            j = i + 1
            if linea[j : j + 1] == ">":
                j += 1
            while j < n and linea[j] == " ":
                j += 1
            k, q = j, ""
            while k < n and (q or linea[k] not in " ;|&"):
                if linea[k] in "\"'":
                    q = "" if q == linea[k] else (q or linea[k])
                k += 1
            destinos.append(linea[j:k])
            i = k
            continue
        i += 1
    return destinos


def _tokens(segmento: str) -> list[str]:
    try:
        toks = shlex.split(segmento)
    except ValueError:
        toks = segmento.split()
    while toks and ("=" in toks[0].split("/")[0] or toks[0] == "sudo"):
        toks = toks[1:]  # variables de entorno delante del comando
    return toks


def _valor(toks: list[str], *opciones: str) -> str | None:
    for i, t in enumerate(toks):
        for o in opciones:
            if t == o and i + 1 < len(toks):
                return toks[i + 1]
            if o.startswith("--") and t.startswith(o + "="):
                return t.split("=", 1)[1]
    return None


def _comando(segmento: str) -> str | None:
    toks = _tokens(segmento)
    if not toks:
        return None
    cli = Path(toks[0]).name
    pos = [t for t in toks[1:] if not t.startswith("-")]
    v = pos[0] if pos else ""
    v2 = pos[1] if len(pos) > 1 else ""
    # El nombre del comando y el primer argumento no opcional dan el subcomando.
    if cli == "aws":
        servicio, verbo = v, v2
        if servicio == "s3":
            return None if verbo in {"ls", "presign"} else f"aws s3 {verbo}"
        if servicio == "configure":
            return "aws configure"
        if verbo and not verbo.startswith(AWS_LECTURA):
            return f"aws {servicio} {verbo}"
    elif cli == "gcloud":
        modo = [t for t in pos[:6] if t in GCLOUD_ESCRIBE]
        if modo:
            return f"gcloud {modo[0]}"
    elif cli == "gsutil":
        if v and v not in GSUTIL_LECTURA:
            return f"gsutil {v}"
    elif cli == "bq":
        if v and v not in BQ_LECTURA:
            return f"bq {v}"
        if v == "query" and BQ_DML.search(" ".join(toks[2:])):
            return "bq query con DML"
    elif cli == "gh":
        if v == "api":
            metodo = (_valor(toks, "-X", "--method") or "").upper()
            if metodo in {"POST", "PUT", "PATCH", "DELETE"}:
                return f"gh api {metodo}"
            campos = any(
                t in {"-f", "-F", "--field", "--raw-field", "--input"} for t in toks
            )
            if campos and metodo != "GET":
                return "gh api con campos (POST implícito)"
        elif v2 in GH_ESCRIBE or (v == "auth" and v2 in GH_ESCRIBE):
            return f"gh {v} {v2}"
    elif cli == "kubectl":
        if v in KUBECTL_ESCRIBE:
            return f"kubectl {v}"
    elif cli == "terraform":
        if v in TERRAFORM_ESCRIBE:
            return f"terraform {v}"
    elif cli in {"curl", "wget"}:
        metodo = (_valor(toks, "-X", "--request") or "GET").upper()
        if metodo not in {"GET", "HEAD"}:
            return f"{cli} -X {metodo}"
        if any(t in {"-d", "--data", "--data-raw", "--data-binary", "-F", "--form", "-T",
                     "--upload-file"} for t in toks):  # fmt: skip
            return f"{cli} con cuerpo"
        salida = _valor(toks, "-o", "--output", "-O", "--output-document")
        if salida and not _es_datos(salida):
            return f"{cli} guarda fuera de datos/: {salida}"
    elif cli in LOCALES:
        destinos = [t for t in toks[1:] if not t.startswith("-")]
        if any(not _es_datos(d) for d in destinos):
            return f"{cli} fuera de datos/"
    return None


def revisar_sh(texto: str) -> list[str]:
    """Hallazgos en shell: verbo de modificación o salida fuera de datos/."""
    hallazgos = []
    for n, linea in enumerate(texto.splitlines(), 1):
        limpia = re.sub(r"(^|\s)#.*$", "", linea)
        if not limpia.strip():
            continue
        for segmento in SEPARADOR.split(limpia):
            motivo = _comando(segmento)
            if motivo:
                hallazgos.append(f"{n}: {motivo}: {linea.strip()}")
        for destino in _redirecciones(limpia):
            if not _es_datos(destino):
                hallazgos.append(
                    f"{n}: salida fuera de datos/ ({destino}): {linea.strip()}"
                )
    return hallazgos


# --- Python --------------------------------------------------------------------

SDK_ESCRIBE = re.compile(
    r"\.(?:create|update|delete|put|terminate|modify|attach|detach|reboot|insert|patch|"
    r"upload|remove|deploy|enable|disable|publish|send|invoke)_[a-z0-9_]+\(|"
    r"\b(?:requests|httpx|session|client)\.(?:post|put|patch|delete)\("
)
SUBPROCESO = re.compile(r"subprocess\.(?:run|call|check_call|check_output|Popen)\(")
SUBPROCESO_ESCRIBE = {
    "rm", "mv", "cp", "tee", "dd", "touch", "mkdir", "delete", "create", "update",
    "apply", "deploy", "put", "destroy", "POST", "PUT", "PATCH", "DELETE", "-X",
    "add-iam-policy-binding", "set-iam-policy",
}  # fmt: skip
ESCRIBE_ARCHIVO = re.compile(
    r"\.(?:write_text|write_bytes|touch|mkdir|unlink|rmdir|rename|replace)\(|"
    r"\.to_(?:csv|json|parquet|excel|pickle|feather|sql)\(|"
    r"\bopen\([^)]*?(?:,\s*|mode\s*=\s*)['\"][wax][bt+]*['\"]|"
    r"\bshutil\.(?:rmtree|copy\w*|move)\(|\bos\.(?:remove|rename|system|unlink|makedirs)\("
)
LITERAL = re.compile(
    r"""(?:Path|open|to_\w+|copy\w*|move|rmtree)\(\s*[rbf]*['"]([^'"]*)['"]"""
)


def revisar_py(texto: str) -> list[str]:
    """Hallazgos en Python: SDK de escritura, procesos, y archivos fuera de datos/."""
    hallazgos = []
    for n, linea in enumerate(texto.splitlines(), 1):
        limpia = re.sub(r"(^|\s)#.*$", "", linea)
        if SDK_ESCRIBE.search(limpia):
            hallazgos.append(f"{n}: llamada de escritura: {linea.strip()}")
        if SUBPROCESO.search(limpia):
            palabras = set(re.findall(r"""['"]([^'"\s]+)['"]""", limpia))
            if palabras & SUBPROCESO_ESCRIBE:
                hallazgos.append(f"{n}: subproceso que modifica: {linea.strip()}")
        if ESCRIBE_ARCHIVO.search(limpia):
            literal = LITERAL.search(limpia)
            destino = literal.group(1) if literal else None
            sin_ruta_clara = destino is None and "datos" not in limpia.lower()
            if sin_ruta_clara or (destino is not None and not _es_datos(destino)):
                hallazgos.append(f"{n}: escritura fuera de datos/: {linea.strip()}")
    return hallazgos


# --- Los scripts reales del repositorio -----------------------------------------


def _scripts(sufijo: str) -> list[Path]:
    return sorted((RAIZ / "scripts").rglob(f"*{sufijo}"))


def test_gitignore_excluye_datos_y_exportes():
    lineas = (RAIZ / ".gitignore").read_text().splitlines()
    for patron in ("datos/", "*.csv", "*.parquet", ".env", ".coverage"):
        assert patron in lineas, f"falta {patron} en .gitignore"


def test_scripts_sh_solo_leen_y_escriben_en_datos():
    infractores = [
        f"{r.relative_to(RAIZ)}:{h}"
        for r in _scripts(".sh")
        for h in revisar_sh(r.read_text())
    ]
    assert not infractores, "\n".join(infractores)


def test_scripts_py_solo_leen_y_escriben_en_datos():
    infractores = [
        f"{r.relative_to(RAIZ)}:{h}"
        for r in _scripts(".py")
        for h in revisar_py(r.read_text())
    ]
    assert not infractores, "\n".join(infractores)


# --- Los revisores mismos: lo que debe fallar y lo que no -----------------------

SH_DEBE_FALLAR = (
    "aws s3 rm s3://b/x",
    "aws iam create-role --role-name x",
    "aws s3 cp a s3://b/a",
    "gsutil rm -r gs://b",
    "gcloud projects add-iam-policy-binding p --member=m --role=r",
    "gcloud run deploy s",
    "gcloud config set project x",
    "bq rm -f -t d.t",
    "bq mk d",
    "bq query 'DELETE FROM t WHERE true'",
    "bq query --use_legacy_sql=false 'insert into t values (1)'",
    "gh pr merge 3",
    "gh api -X POST repos/o/r/issues",
    "gh api --method PATCH repos/o/r",
    "gh api repos/o/r/rulesets -f name=x",
    "gh auth switch",
    "curl -X DELETE https://api/x",
    "curl -o /tmp/salida.json https://api/x",
    "curl -d '{}' https://api/x",
    "aws sts get-caller-identity | tee /tmp/id.json",
    "terraform apply",
    "kubectl delete pod x",
    "rm -rf /tmp/x",
    "echo x > /tmp/salida.txt",
    "aws sts get-caller-identity >> resultado.json",
    "K=1 gcloud pubsub topics delete t",
)
SH_NO_DEBE_FALLAR = (
    "aws ce get-cost-and-usage --time-period Start=a,End=b > datos/aws/dia.json",
    'gcloud billing accounts list > "$DATOS/cuentas.json"',
    "bq query --use_legacy_sql=false 'SELECT 1'",
    "aws sts get-caller-identity > /dev/null",
    "# aws s3 rm solo es un comentario",
    "gh auth status 2>&1 | head -3",
    "aws ec2 describe-instances --start-time 2026-09-01",
    "aws s3 ls s3://b/export/",
    "gh run list --workflow deploy.yml",
    "gh api repos/o/r/rulesets",
    "gh api -X GET repos/o/r",
    "curl -s https://api/x -o datos/x.json",
    "gcloud firestore databases list --project=p --format='value(name)'",
    "gcloud services list --enabled",
    "echo $((a > b))",
    "[[ $a > $b ]] && echo si",
    "if [ -f datos/x ]; then echo ok; fi",
    "echo 'a > b'",
    "aws sts get-caller-identity 2>&1 | tee datos/id.json",
    "mkdir -p datos/aws",
    "set -euo pipefail",
    "",
)
PY_DEBE_FALLAR = (
    "s3.delete_bucket(Bucket='b')",
    "cliente.put_object(Bucket='b', Key='k')",
    "ec2.terminate_instances(InstanceIds=['i'])",
    "Path('/tmp/x').write_text('a')",
    "Path('/tmp/datos.txt').write_text('a')",
    "open('salida.csv', 'w')",
    "open(ruta, mode='w')",
    "df.to_csv('/tmp/x.csv')",
    "shutil.rmtree('x')",
    "requests.post(url)",
    "subprocess.run(['aws', 's3', 'rm', 's3://b/x'])",
    "subprocess.run(['rm', '-rf', 'x'])",
)
PY_NO_DEBE_FALLAR = (
    "def f() -> int:",
    "if f > 0:",
    "x = a >> 2",
    "Path('datos/aws/dia.json').write_text(texto)",
    "datos = json.loads(Path('datos/a.json').read_text())",
    "df.to_csv('datos/aws/x.csv')",
    "open('datos/x.json', 'w')",
    "respuesta = cliente.get_cost_and_usage(TimePeriod=p)",
    "subprocess.run(['aws', 's3', 'ls'])",
    "parser.add_argument('--x')",
    "df = df.set_index('a')",
)


def test_sh_detecta_lo_que_debe():
    for linea in SH_DEBE_FALLAR:
        assert revisar_sh(linea), linea


def test_sh_no_da_falsos_positivos():
    for linea in SH_NO_DEBE_FALLAR:
        assert not revisar_sh(linea), (linea, revisar_sh(linea))


def test_py_detecta_lo_que_debe():
    for linea in PY_DEBE_FALLAR:
        assert revisar_py(linea), linea


def test_py_no_da_falsos_positivos():
    for linea in PY_NO_DEBE_FALLAR:
        assert not revisar_py(linea), (linea, revisar_py(linea))


def test_sh_informa_el_numero_de_linea():
    texto = "set -e\naws s3 rm s3://b/x\n"
    assert revisar_sh(texto)[0].startswith("2:")
