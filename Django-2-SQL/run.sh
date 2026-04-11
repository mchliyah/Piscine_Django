#!/usr/bin/env zsh

if [[ -f ".env" ]]; then
  set -a
  source ./.env
  set +a
fi

export POSTGRES_DB="${POSTGRES_DB:-}"
export POSTGRES_USER="${POSTGRES_USER:-}"
export POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-}"
export POSTGRES_HOST="${POSTGRES_HOST:-}"
export POSTGRES_PORT="${POSTGRES_PORT:-}"

if [[ -z "$POSTGRES_DB" || -z "$POSTGRES_USER" || -z "$POSTGRES_PASSWORD" || -z "$POSTGRES_HOST" || -z "$POSTGRES_PORT" ]]; then
  echo "[ERROR] Missing DB configuration. Set POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT in .env or shell."
  exit 1
fi

POSTGRES_CONTAINER_NAME="${POSTGRES_CONTAINER_NAME:-djangotraining-postgres}"
POSTGRES_IMAGE="${POSTGRES_IMAGE:-postgres:15}"

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
VENV_DIR="$SCRIPT_DIR/.venv"

cd "$SCRIPT_DIR" || exit 1

start_postgres_container() {
  if ! command -v docker >/dev/null 2>&1; then
    echo "[ERROR] Docker is required to start PostgreSQL automatically."
    return 1
  fi

  if docker ps --format '{{.Names}}' | grep -qx "$POSTGRES_CONTAINER_NAME"; then
    return 0
  fi

  if docker ps -a --format '{{.Names}}' | grep -qx "$POSTGRES_CONTAINER_NAME"; then
    docker start "$POSTGRES_CONTAINER_NAME" >/dev/null
  else
    docker run -d \
      --name "$POSTGRES_CONTAINER_NAME" \
      -e POSTGRES_DB="$POSTGRES_DB" \
      -e POSTGRES_USER="$POSTGRES_USER" \
      -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
      -p "$POSTGRES_PORT":5432 \
      "$POSTGRES_IMAGE" >/dev/null
  fi

  echo "[INFO] Waiting for PostgreSQL container to become ready..."
  for _ in {1..30}; do
    if docker exec "$POSTGRES_CONTAINER_NAME" pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" >/dev/null 2>&1; then
      return 0
    fi
    sleep 1
  done

  echo "[ERROR] PostgreSQL container did not become ready in time."
  return 1
}

if ! start_postgres_container; then
  exit 1
fi

if [[ ! -d "$VENV_DIR" ]]; then
  source ./env.sh
else
  source "$VENV_DIR/bin/activate"
fi

if ! python3 manage.py migrate --check >/dev/null 2>&1; then
  echo "[INFO] Applying Django migrations..."
  python3 manage.py migrate --noinput
fi

python3 manage.py runserver 127.0.0.1:8000
