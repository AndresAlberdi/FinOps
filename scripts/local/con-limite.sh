#!/usr/bin/env bash
# con-limite.sh — corre un comando con tope de memoria (cgroup de systemd), para que el
# kernel mate el comando y no la sesión gráfica. Origen: el corte del 2026-10-10, en que
# Playwright (chrome-headless) y next-server agotaron 32 GB y swap y cayó GNOME Shell.
#
# Uso:    scripts/local/con-limite.sh [-m TOPE] -- comando [argumentos...]
#         TOPE: número entero con sufijo M o G (por defecto 6G). Sin swap.
# Salida: la del comando; si el kernel lo mata por superar el tope, SIGKILL (137 en la terminal).
set -euo pipefail

uso() {
  echo "uso: con-limite.sh [-m TOPE] -- comando [argumentos...]   (TOPE: 512M, 6G…)" >&2
  exit 2
}

tope="6G"
if [[ "${1:-}" == "-m" ]]; then
  [[ $# -ge 2 ]] || uso
  tope="$2"
  shift 2
fi
[[ "${1:-}" == "--" ]] && shift
[[ $# -ge 1 ]] || uso
[[ "$tope" =~ ^[1-9][0-9]*[MG]$ ]] || { echo "TOPE inválido: $tope (use 512M, 6G…)" >&2; exit 2; }

if ! command -v systemd-run >/dev/null 2>&1; then
  echo "systemd-run no está disponible: no se puede limitar la memoria" >&2
  exit 3
fi

exec systemd-run --user --scope --quiet \
  -p "MemoryMax=${tope}" -p MemorySwapMax=0 -- "$@"
