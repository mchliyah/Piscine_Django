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
export POSTGRES_HOST="${POSTGRES_HOST:-localhost}"
export POSTGRES_PORT="${POSTGRES_PORT:-5432}"

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
VENV_DIR="$SCRIPT_DIR/.venv"

cd "$SCRIPT_DIR" || exit 1

# Initialize venv only when missing, otherwise just activate it.
if [[ ! -d "$VENV_DIR" ]]; then
  source ./env.sh
else
  source "$VENV_DIR/bin/activate"
fi

# Apply migrations only when pending.
if ! python manage.py migrate --check >/dev/null 2>&1; then
  echo "[INFO] Applying Django migrations..."
  python manage.py migrate --noinput
fi

python manage.py runserver 127.0.0.1:8000
