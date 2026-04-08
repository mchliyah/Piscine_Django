import os

import psycopg2
from django.http import HttpResponse


def _db_value(primary_key: str, alternate_key: str, default: str) -> str:
    return os.environ.get(primary_key) or os.environ.get(alternate_key) or default


def _create_movies_table(connection_params):
    sql = """
    CREATE TABLE IF NOT EXISTS ex00_movies (
        title VARCHAR(64) UNIQUE NOT NULL,
        episode_nb INTEGER PRIMARY KEY,
        opening_crawl TEXT,
        director VARCHAR(32) NOT NULL,
        producer VARCHAR(128) NOT NULL,
        release_date DATE NOT NULL
    );
    """

    with psycopg2.connect(**connection_params) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)


def init(request):
    host_value = os.environ.get("POSTGRES_HOST") or os.environ.get("DB_HOST")
    connection_params = {
        "dbname": _db_value("POSTGRES_DB", "DB_NAME", "postgres"),
        "user": _db_value("POSTGRES_USER", "DB_USER", "postgres"),
        "password": _db_value("POSTGRES_PASSWORD", "DB_PASSWORD", ""),
        "host": host_value if host_value is not None else "localhost",
        "port": _db_value("POSTGRES_PORT", "DB_PORT", "5432"),
    }

    try:
        _create_movies_table(connection_params)
        return HttpResponse("OK")
    except Exception as error:
        return HttpResponse(str(error), status=500)
