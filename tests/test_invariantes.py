"""Automatiza las verificaciones de CLAUDE.md que no dependen de una persona.

Reglas (CLAUDE.md, «Verificación antes de terminar»): ningún script de scripts/
usa verbos de modificación, ninguno escribe fuera de datos/, y git ignora datos/.
Los revisores son funciones puras (`revisar_sh`, `revisar_py`) para poder
probarlos con casos positivos y negativos, aunque scripts/ esté vacío.
"""

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

CLI_NUBE = r"(?:aws|gcloud|gsutil|bq|oci|gh|kubectl|terraform|az)"
# Verbos de modificación, en las formas de CLI más habituales.
VERBO_CLI = re.compile(
    r"(?:^|[\s;&|(])" + CLI_NUBE + r"\b.*?"
    r"\b(?:create|update|delete|put|apply|destroy|remove|rm|rb|mb|cp|mv|sync|"
    r"set-iam-policy|add-iam-policy-binding|remove-iam-policy-binding|"
    r"attach|detach|terminate|modify|start|stop|reboot|run-instances|"
    r"deploy|enable|disable|import|export|insert|patch|merge|close|transfer)"
    r"(?:-[a-z0-9-]+)?\b"
)
# boto3 / SDKs: llamadas de escritura.
LLAMADA_SDK = re.compile(
    r"\.(?:create|update|delete|put|terminate|modify|attach|detach|run|start|stop|"
    r"set_iam_policy|insert|patch|upload)_[a-z_]+\(|\.(?:put|delete|post|patch)\("
)
ESCRITURA_PY = re.compile(
    r"\.(?:write_text|write_bytes|touch|mkdir|unlink|rmdir)\(|"
    r"\bopen\([^)]*,\s*['\"][wax+]|shutil\.(?:rmtree|copy|move)|os\.(?:remove|rename|system)"
)
REDIRECCION_SH = re.compile(r">>?\s*(?!&|/dev/null)(\S+)")


def _sin_comentario(linea: str) -> str:
    return linea.split("#", 1)[0]


def revisar_sh(texto: str) -> list[str]:
    """Hallazgos en un script de shell: verbo de modificación o salida fuera de datos/."""
    hallazgos = []
    for n, linea in enumerate(texto.splitlines(), 1):
        limpia = _sin_comentario(linea)
        if VERBO_CLI.search(limpia):
            hallazgos.append(f"{n}: verbo de modificación: {linea.strip()}")
        for destino in REDIRECCION_SH.findall(limpia):
            destino = destino.strip("\"'")
            if not (
                destino.startswith(("datos/", "$DATOS", "${DATOS"))
                or "/datos/" in destino
            ):
                hallazgos.append(f"{n}: salida fuera de datos/: {linea.strip()}")
    return hallazgos


def revisar_py(texto: str) -> list[str]:
    """Hallazgos en un script de Python: SDK de escritura, archivos o procesos."""
    hallazgos = []
    for n, linea in enumerate(texto.splitlines(), 1):
        limpia = _sin_comentario(linea)
        if LLAMADA_SDK.search(limpia):
            hallazgos.append(f"{n}: llamada de escritura: {linea.strip()}")
        if ESCRITURA_PY.search(limpia) and "datos" not in limpia.lower():
            hallazgos.append(f"{n}: escritura fuera de datos/: {linea.strip()}")
    return hallazgos


def _scripts(sufijo: str) -> list[Path]:
    return sorted((RAIZ / "scripts").rglob(f"*{sufijo}"))


# --- Los scripts reales del repositorio ---------------------------------------


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


# --- Los revisores mismos: casos que deben fallar y casos que no --------------


def test_sh_detecta_modificaciones_de_nube_y_github():
    for linea in (
        "aws s3 rm s3://b/x",
        "aws iam create-role --role-name x",
        "gsutil rm -r gs://b",
        "gcloud projects add-iam-policy-binding p --member=m --role=r",
        "gcloud run deploy s",
        "bq rm -f -t d.t",
        "gh pr merge 3",
        "terraform apply",
        "kubectl delete pod x",
    ):
        assert revisar_sh(linea), linea


def test_sh_detecta_salida_fuera_de_datos():
    assert revisar_sh("echo x > /tmp/salida.txt")
    assert revisar_sh("aws sts get-caller-identity >> resultado.json")


def test_sh_acepta_lecturas_y_salida_en_datos():
    for linea in (
        "aws ce get-cost-and-usage --time-period Start=a,End=b > datos/aws/dia.json",
        'gcloud billing accounts list > "$DATOS/cuentas.json"',
        "bq query --use_legacy_sql=false 'SELECT 1'",
        "aws sts get-caller-identity > /dev/null",
        "# aws s3 rm solo es un comentario",
        "gh auth status 2>&1 | head -3",
    ):
        assert not revisar_sh(linea), linea


def test_py_detecta_escrituras():
    for linea in (
        "s3.delete_bucket(Bucket='b')",
        "cliente.put_object(Bucket='b', Key='k')",
        "ec2.terminate_instances(InstanceIds=['i'])",
        "Path('/tmp/x').write_text('a')",
        "open('salida.csv', 'w')",
        "shutil.rmtree('x')",
        "requests.post(url)",
    ):
        assert revisar_py(linea), linea


def test_py_no_da_falsos_positivos_en_python_normal():
    for linea in (
        "def f() -> int:",
        "if f > 0:",
        "x = a >> 2",
        "Path('datos/aws/dia.json').write_text(texto)",
        "datos = json.loads(Path('datos/a.json').read_text())",
        "respuesta = cliente.get_cost_and_usage(TimePeriod=p)",
    ):
        assert not revisar_py(linea), linea
