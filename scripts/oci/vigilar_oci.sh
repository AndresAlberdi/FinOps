#!/usr/bin/env bash
# Vigilancia de OCI, solo lectura. Corre en GitHub Actions (ver
# .github/workflows/vigilancia-oci.yml) con un token de sesión de corta vida.
#
# Reglas del proyecto: sin credenciales embebidas; no escribe archivos; ningún
# verbo de modificación; la salida es PÚBLICA (repositorio público), así que
# solo imprime «OK» o «SUPERADO» por medida: nunca montos, OCID, espacio de
# nombres, nombre del bucket ni respuestas crudas de la CLI (los errores de la
# CLI se descartan).
#
# Entorno requerido (secretos o variables del Environment, nunca en el YAML):
#   OCI_PROFILE, OCI_TENANCY, OCI_COMPARTMENT, OCI_NAMESPACE, OCI_BUCKET
# Opcional: MODO=diario|semanal|todo (por defecto «todo»),
#           UMBRAL_BUCKET_GIB (15), UMBRAL_MEMORIA_PCT (21), TOPE_DISCO_GB (150)
#
# Salida: código 0 si todo está dentro de lo gratuito; 1 si una medida se
# supera o no se puede medir (un fallo de medición también avisa: el silencio
# no es «todo bien»).
set -uo pipefail
export LC_ALL=C # decimales con punto (awk), sea cual sea la configuración regional

MODO="${MODO:-todo}"
UMBRAL_BUCKET_GIB="${UMBRAL_BUCKET_GIB:-15}"
UMBRAL_MEMORIA_PCT="${UMBRAL_MEMORIA_PCT:-21}"
TOPE_DISCO_GB="${TOPE_DISCO_GB:-150}"
TOPE_OCPU=2
TOPE_MEM_GB=12

for v in OCI_PROFILE OCI_TENANCY OCI_COMPARTMENT OCI_NAMESPACE OCI_BUCKET; do
  if [ -z "${!v:-}" ]; then
    echo "FALLO: falta la variable $v"
    exit 1
  fi
done

fallos=0
oci_q() { oci --profile "$OCI_PROFILE" --auth security_token "$@" 2>/dev/null; }
# Para sumas: la CLI no imprime nada con una lista vacía, así que «salida vacía
# con éxito» vale 0, y un fallo de la CLI no imprime nada (= sin medir).
oci_suma() {
  local salida rc
  salida=$(oci --profile "$OCI_PROFILE" --auth security_token "$@" 2>/dev/null; echo "RC:$?")
  rc="${salida##*RC:}"
  salida="${salida%RC:*}"
  salida=$(printf '%s' "$salida" | tr -d '[:space:]')
  if [ "$rc" != 0 ]; then return 0; fi
  if [ -z "$salida" ]; then echo 0; else echo "$salida"; fi
}
# Cada medida imprime una sola línea con su estado.
ok() { echo "OK       $1"; }
superado() { echo "SUPERADO $1"; fallos=$((fallos + 1)); }
sin_medida() { echo "SIN MEDIR $1"; fallos=$((fallos + 1)); }

# Compara con decimales sin depender de bc.
mayor_o_igual() { awk -v a="$1" -v b="$2" 'BEGIN { exit !(a >= b) }'; }

medir_bucket() {
  local bytes gib
  bytes=$(oci_q os bucket get --namespace-name "$OCI_NAMESPACE" \
    --bucket-name "$OCI_BUCKET" --fields approximateSize \
    --query 'data."approximate-size"' --raw-output)
  if ! [[ "$bytes" =~ ^[0-9]+$ ]]; then
    sin_medida "bucket de respaldos"
    return
  fi
  gib=$(awk -v b="$bytes" 'BEGIN { printf "%.2f", b / 1073741824 }')
  if mayor_o_igual "$gib" "$UMBRAL_BUCKET_GIB"; then
    superado "bucket de respaldos (umbral ${UMBRAL_BUCKET_GIB} GiB)"
  else
    ok "bucket de respaldos"
  fi
}

medir_memoria() {
  local fin ini datos veredicto
  fin=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  ini=$(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ)
  # MQL solo admite intervalos de 1m-60m, 1h-24h y 1d: se pide el p95 diario de
  # los últimos 7 días, de TODAS las series (una por instancia). La regla de
  # recuperación de Oracle usa el p95 de la ventana de 7 días; el máximo de los
  # p95 diarios es su aproximación (verificar contra la CLI en la primera corrida).
  datos=$(oci_q monitoring metric-data summarize-metrics-data \
    --namespace oci_computeagent --compartment-id "$OCI_COMPARTMENT" \
    --query-text 'MemoryUtilization[1d].percentile(0.95)' \
    --start-time "$ini" --end-time "$fin" \
    --query 'data[*]."aggregated-datapoints"[*].value' --output json)
  veredicto=$(printf '%s' "$datos" | UMBRAL="$UMBRAL_MEMORIA_PCT" python3 -c '
import json, os, sys
try:
    series = json.load(sys.stdin)
    umbral = float(os.environ["UMBRAL"])
    maximos = [max(float(v) for v in s) for s in series if s]
except Exception:
    print("SIN"); sys.exit()
if not maximos:
    print("SIN")
else:
    print("SUPERADO" if min(maximos) <= umbral else "OK")
' 2>/dev/null)
  case "$veredicto" in
    OK) ok "memoria de la VM" ;;
    SUPERADO) superado "memoria de la VM cerca del umbral de recuperación (verificar la regla con Oracle)" ;;
    *) sin_medida "memoria de la VM" ;;
  esac
}

medir_computo() {
  # Tope gratuito A1: 2 OCPU y 12 GB en total (1.500 OCPU-h y 9.000 GB-h al
  # mes). Se comprueba la configuración, que es determinista, en vez de
  # proyectar horas: cualquier OCPU o GB de más se cobra. Solo formas A1 (las
  # E2.Micro tienen su propio cupo gratuito). Alcance: el compartimento
  # indicado, sin subcompartimentos (documentado en la propuesta).
  local datos veredicto
  datos=$(oci_q compute instance list --compartment-id "$OCI_COMPARTMENT" \
    --all --output json)
  veredicto=$(printf '%s' "$datos" | TO="$TOPE_OCPU" TM="$TOPE_MEM_GB" python3 -c '
import json, os, sys
try:
    inst = json.load(sys.stdin).get("data", [])
    o = m = 0.0
    for i in inst:
        if i.get("lifecycle-state") in ("TERMINATED", "TERMINATING"):
            continue
        if not str(i.get("shape", "")).startswith("VM.Standard.A1"):
            continue
        cfg = i["shape-config"]
        o += float(cfg["ocpus"])
        m += float(cfg["memory-in-gbs"])
except Exception:
    print("SIN"); sys.exit()
print("SUPERADO" if o > float(os.environ["TO"]) or m > float(os.environ["TM"]) else "OK")
' 2>/dev/null)
  case "$veredicto" in
    OK) ok "cómputo A1" ;;
    SUPERADO) superado "cómputo A1 por encima de 2 OCPU / 12 GB" ;;
    *) sin_medida "cómputo A1" ;;
  esac
}

medir_disco() {
  # Tope gratuito: 200 GB entre discos de arranque Y volúmenes de bloque. Los
  # discos de arranque se listan por dominio de disponibilidad.
  local ads ad arranque bloque total="" suma=0
  ads=$(oci_q iam availability-domain list --compartment-id "$OCI_TENANCY" \
    --query 'data[*].name' --output json | python3 -c 'import sys,json; print("\n".join(json.load(sys.stdin)))' 2>/dev/null)
  if [ -z "$ads" ]; then
    sin_medida "discos"
    return
  fi
  while IFS= read -r ad; do
    arranque=$(oci_suma bv boot-volume list --compartment-id "$OCI_COMPARTMENT" \
      --availability-domain "$ad" --all \
      --query "sum(data[?\"lifecycle-state\"=='AVAILABLE'].\"size-in-gbs\")" --raw-output)
    if ! [[ "$arranque" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
      sin_medida "discos de arranque"
      return
    fi
    suma=$(awk -v a="$suma" -v b="$arranque" 'BEGIN { print a + b }')
  done <<< "$ads"
  bloque=$(oci_suma bv volume list --compartment-id "$OCI_COMPARTMENT" --all \
    --query "sum(data[?\"lifecycle-state\"=='AVAILABLE'].\"size-in-gbs\")" --raw-output)
  if ! [[ "$bloque" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
    sin_medida "volúmenes de bloque"
    return
  fi
  total=$(awk -v a="$suma" -v b="$bloque" 'BEGIN { print a + b }')
  if awk -v t="$total" -v tope="$TOPE_DISCO_GB" 'BEGIN { exit !(t > tope) }'; then
    superado "discos (tope ${TOPE_DISCO_GB} GB entre arranque y bloque)"
  else
    ok "discos"
  fi
}

medir_costo() {
  # Costo del mes en curso por día; se suman SOLO los montos positivos (un
  # crédito negativo no compensa un cargo). El monto NO se imprime. «null» o
  # una respuesta ilegible es «sin medir», nunca OK. La Usage API tiene
  # retraso (verificar su latencia).
  local ini fin datos veredicto
  ini=$(date -u +%Y-%m-01T00:00:00Z)
  fin=$(date -u -d 'tomorrow' +%Y-%m-%dT00:00:00Z)
  datos=$(oci_q usage-api usage-summary request-summarized-usages \
    --tenant-id "$OCI_TENANCY" --granularity DAILY --query-type COST \
    --time-usage-started "$ini" --time-usage-ended "$fin" \
    --query 'data.items' --output json)
  veredicto=$(printf '%s' "$datos" | python3 -c '
import json, sys
try:
    items = json.load(sys.stdin)
    # Lista vacía (retraso de la Usage API) o cualquier monto null: sin medir.
    if not items or any(i.get("computed-amount") is None for i in items):
        print("SIN"); sys.exit()
    suma = sum(float(i["computed-amount"]) for i in items if float(i["computed-amount"]) > 0)
except Exception:
    print("SIN"); sys.exit()
print("SUPERADO" if suma > 0.005 else "OK")
' 2>/dev/null)
  case "$veredicto" in
    OK) ok "costo del mes" ;;
    SUPERADO) superado "costo del mes mayor que cero" ;;
    *) sin_medida "costo del mes" ;;
  esac
}

case "$MODO" in
  diario)
    medir_bucket
    medir_memoria
    ;;
  semanal)
    medir_costo
    medir_computo
    medir_disco
    ;;
  todo)
    medir_bucket
    medir_memoria
    medir_costo
    medir_computo
    medir_disco
    ;;
  *)
    echo "FALLO: MODO desconocido"
    exit 1
    ;;
esac

if [ "$fallos" -gt 0 ]; then
  echo "RESULTADO: $fallos medida(s) superada(s) o sin medir"
  exit 1
fi
echo "RESULTADO: todo dentro de lo gratuito"
