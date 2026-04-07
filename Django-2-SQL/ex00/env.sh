#!/usr/bin/env bash

set -e

INFO_COLOR='\033[1;34m'
RESET_COLOR='\033[0m'

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    printf "%b[INFO]%b to activate the venv in the current shell run:\n" "$INFO_COLOR" "$RESET_COLOR"
    printf "  . ./env.sh\n"
    printf "  source ./env.sh\n"
fi

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
LIB_DIR=$(cd "$SCRIPT_DIR/.." && pwd)
VENV_DIR="$LIB_DIR/django_venv"

if [ ! -d "$VENV_DIR" ]; then
    if ! python3 -m venv "$VENV_DIR"; then
        rm -rf "$VENV_DIR"
        python3 -m pip install virtualenv
        python3 -m virtualenv "$VENV_DIR"
    fi
fi

. "$VENV_DIR/bin/activate"

python -m pip install -r "$SCRIPT_DIR/requirements.txt"

alias python=python3
hash -r
