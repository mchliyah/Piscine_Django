#!/usr/bin/env zsh

# Optional overrides before running:
# export POSTGRES_DB=postgres
# export POSTGRES_USER=postgres
# export POSTGRES_PASSWORD=''
# export POSTGRES_HOST=localhost
# export POSTGRES_PORT=5432

export POSTGRES_DB="${POSTGRES_DB:-postgres}"
export POSTGRES_USER="${POSTGRES_USER:-postgres}"
export POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-}"
export POSTGRES_HOST="${POSTGRES_HOST:-}"
export POSTGRES_PORT="${POSTGRES_PORT:-5432}"

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
VENV_DIR="$SCRIPT_DIR/.venv"

cd "$SCRIPT_DIR" || exit 1

if [[ -x "$VENV_DIR/bin/python3" ]]; then
  "$VENV_DIR/bin/python3" manage.py runserver 127.0.0.1:8000
else
  python3 manage.py runserver 127.0.0.1:8000
fi
