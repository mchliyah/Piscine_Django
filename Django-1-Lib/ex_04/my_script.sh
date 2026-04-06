#!/bin/sh

set -e

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
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
python -m pip install -r "$SCRIPT_DIR/requirement.txt"
