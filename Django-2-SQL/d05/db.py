import os
from pathlib import Path

import psycopg2


_ENV_LOADED = False


def load_env_file() -> None:
    global _ENV_LOADED
    if _ENV_LOADED:
        return

    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        _ENV_LOADED = True
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)

    _ENV_LOADED = True


def _db_value(primary_key: str, alternate_key: str, default: str) -> str:
    load_env_file()
    return os.environ.get(primary_key) or os.environ.get(alternate_key) or default


def _required_db_value(primary_key: str, alternate_key: str) -> str:
    value = _db_value(primary_key, alternate_key, "").strip()
    if value:
        return value
    raise RuntimeError(
        f"Missing required DB setting: set {primary_key} (or {alternate_key}) in environment or .env"
    )


def get_connection_params() -> dict[str, str]:
    return {
        "dbname": _required_db_value("POSTGRES_DB", "DB_NAME"),
        "user": _required_db_value("POSTGRES_USER", "DB_USER"),
        "password": _required_db_value("POSTGRES_PASSWORD", "DB_PASSWORD"),
        "host": _required_db_value("POSTGRES_HOST", "DB_HOST"),
        "port": _required_db_value("POSTGRES_PORT", "DB_PORT"),
    }


def get_db_connection():
    params = get_connection_params()
    return psycopg2.connect(
        dbname=params["dbname"],
        user=params["user"],
        password=params["password"],
        host=params["host"],
        port=params["port"],
    )


def get_django_database_config() -> dict[str, str]:
    params = get_connection_params()
    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": params["dbname"],
        "USER": params["user"],
        "PASSWORD": params["password"],
        "HOST": params["host"],
        "PORT": params["port"],
    }