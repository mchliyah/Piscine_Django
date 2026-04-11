from django.http import HttpResponse

from d05.db import get_db_connection


def _create_movies_table():
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

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)


def init(request):
    try:
        _create_movies_table()
        return HttpResponse("OK")
    except Exception as error:
        return HttpResponse(str(error), status=500)
