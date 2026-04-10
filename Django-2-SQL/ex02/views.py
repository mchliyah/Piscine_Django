import os

import psycopg2
from django.http import HttpResponse
from django.utils.html import escape


def _db_value(primary_key: str, alternate_key: str, default: str) -> str:
    return os.environ.get(primary_key) or os.environ.get(alternate_key) or default


def _create_movies_table(connection_params):
    sql = """
    CREATE TABLE IF NOT EXISTS ex02_movies (
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


def _populate_movies_table(connection_params):
    movies = [
        {
            "title": "The Phantom Menace",
            "episode_nb": 1,
            "opening_crawl": None,
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "1999-05-19",
        },
        {
            "title": "Attack of the Clones",
            "episode_nb": 2,
            "opening_crawl": None,
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2002-05-16",
        },
        {
            "title": "Revenge of the Sith",
            "episode_nb": 3,
            "opening_crawl": None,
            "director": "George Lucas",
            "producer": "Rick McCallum",
            "release_date": "2005-05-19",
        },
        {
            "title": "A New Hope",
            "episode_nb": 4,
            "opening_crawl": None,
            "director": "George Lucas",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1977-05-25",
        },
        {
            "title": "The Empire Strikes Back",
            "episode_nb": 5,
            "opening_crawl": None,
            "director": "Irvin Kershner",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1980-05-17",
        },
        {
            "title": "Return of the Jedi",
            "episode_nb": 6,
            "opening_crawl": None,
            "director": "Richard Marquand",
            "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
            "release_date": "1983-05-25",
        },
        {
            "title": "The Force Awakens",
            "episode_nb": 7,
            "opening_crawl": None,
            "director": "J. J. Abrams",
            "producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
            "release_date": "2015-12-11",
        },
    ]

    sql = """
    INSERT INTO ex02_movies (title, episode_nb, opening_crawl, director, producer, release_date)
    VALUES (%s, %s, %s, %s, %s, %s);
    """

    results = []
    with psycopg2.connect(**connection_params) as connection:
        connection.autocommit = True
        with connection.cursor() as cursor:
            for movie in movies:
                try:
                    cursor.execute(
                        sql,
                        (
                            movie["title"],
                            movie["episode_nb"],
                            movie["opening_crawl"],
                            movie["director"],
                            movie["producer"],
                            movie["release_date"],
                        ),
                    )
                    results.append("OK")
                except Exception as error:
                    results.append(str(error))
    return results


def display(request):
    connection_params = {
        "dbname": _db_value("POSTGRES_DB", "DB_NAME", "djangotraining"),
        "user": _db_value("POSTGRES_USER", "DB_USER", "djangouser"),
        "password": _db_value("POSTGRES_PASSWORD", "DB_PASSWORD", "secret"),
        "host": _db_value("POSTGRES_HOST", "DB_HOST", "localhost"),
        "port": _db_value("POSTGRES_PORT", "DB_PORT", "5432"),
    }
    try:
        with psycopg2.connect(**connection_params) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT title, episode_nb, opening_crawl, director, producer, release_date
                    FROM ex02_movies
                    ORDER BY episode_nb;
                    """
                )
                movies = cursor.fetchall()
                if not movies:
                    return HttpResponse("No data available")

                rows = []
                for title, episode_nb, opening_crawl, director, producer, release_date in movies:
                    rows.append(
                        "<tr>"
                        f"<td>{escape(str(title))}</td>"
                        f"<td>{escape(str(episode_nb))}</td>"
                        f"<td>{escape('' if opening_crawl is None else str(opening_crawl))}</td>"
                        f"<td>{escape(str(director))}</td>"
                        f"<td>{escape(str(producer))}</td>"
                        f"<td>{escape(str(release_date))}</td>"
                        "</tr>"
                    )

                html = (
                    "<table border='1'>"
                    "<thead><tr>"
                    "<th>title</th><th>episode_nb</th><th>opening_crawl</th>"
                    "<th>director</th><th>producer</th><th>release_date</th>"
                    "</tr></thead>"
                    "<tbody>"
                    + "".join(rows)
                    + "</tbody></table>"
                )
                return HttpResponse(html)
    except Exception:
        return HttpResponse("No data available")


def populate(request):
    connection_params = {
        "dbname": _db_value("POSTGRES_DB", "DB_NAME", "djangotraining"),
        "user": _db_value("POSTGRES_USER", "DB_USER", "djangouser"),
        "password": _db_value("POSTGRES_PASSWORD", "DB_PASSWORD", "secret"),
        "host": _db_value("POSTGRES_HOST", "DB_HOST", "localhost"),
        "port": _db_value("POSTGRES_PORT", "DB_PORT", "5432"),
    }
    try:
        results = _populate_movies_table(connection_params)
        return HttpResponse("<br>".join(results))
    except Exception as error:
        return HttpResponse(str(error), status=500)


def init(request):
    connection_params = {
        "dbname": _db_value("POSTGRES_DB", "DB_NAME", "djangotraining"),
        "user": _db_value("POSTGRES_USER", "DB_USER", "djangouser"),
        "password": _db_value("POSTGRES_PASSWORD", "DB_PASSWORD", "secret"),
        "host": _db_value("POSTGRES_HOST", "DB_HOST", "localhost"),
        "port": _db_value("POSTGRES_PORT", "DB_PORT", "5432"),
    }

    try:
        _create_movies_table(connection_params)
        return HttpResponse("OK")
    except Exception as error:
        return HttpResponse(str(error), status=500)
