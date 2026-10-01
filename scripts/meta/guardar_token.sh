#!/usr/bin/env bash
# Guarda el token de solo lectura de Meta en datos/meta/token (permiso 0600).
# El valor se escribe en un prompt oculto: no aparece en pantalla, en el
# historial ni en el chat. Sin argumentos. Lo corre una persona, una vez.
set -euo pipefail
mkdir -p datos/meta
umask 077
printf 'Pega el token de solo lectura de Meta (no se mostrará) y pulsa Enter: '
read -rs token
printf '\n'
[[ -n "$token" ]] || { echo "Token vacío: no se guardó nada." >&2; exit 1; }
printf '%s' "$token" > datos/meta/token
chmod 600 datos/meta/token
echo "Guardado en datos/meta/token (permiso 600). Longitud: ${#token} caracteres."
