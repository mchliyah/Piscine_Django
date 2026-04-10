import os

import psycopg2
from django.http import HttpResponse
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt


def _db_value(primary_key: str, alternate_key: str, default: str) -> str:
    return os.environ.get(primary_key) or os.environ.get(alternate_key) or default


def _connection_params():
    return {
        "dbname": _db_value("POSTGRES_DB", "DB_NAME", "djangotraining"),
        "user": _db_value("POSTGRES_USER", "DB_USER", "djangouser"),
        "password": _db_value("POSTGRES_PASSWORD", "DB_PASSWORD", "secret"),
        "host": _db_value("POSTGRES_HOST", "DB_HOST", "localhost"),
        "port": _db_value("POSTGRES_PORT", "DB_PORT", "5432"),
    }


def _create_movies_table(connection_params):
    table_sql = """
    CREATE TABLE IF NOT EXISTS ex06_movies (
        title VARCHAR(64) UNIQUE NOT NULL,
        episode_nb INTEGER PRIMARY KEY,
        opening_crawl TEXT,
        director VARCHAR(32) NOT NULL,
        producer VARCHAR(128) NOT NULL,
        release_date DATE NOT NULL,
        created TIMESTAMP NOT NULL DEFAULT NOW(),
        updated TIMESTAMP NOT NULL DEFAULT NOW()
    );
    """

    function_sql = """
    CREATE OR REPLACE FUNCTION update_changetimestamp_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated = now();
        NEW.created = OLD.created;
        RETURN NEW;
    END;
    $$ language 'plpgsql';
    """

    trigger_sql = """
    DROP TRIGGER IF EXISTS update_films_changetimestamp ON ex06_movies;
    CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
    ON ex06_movies FOR EACH ROW EXECUTE PROCEDURE
    update_changetimestamp_column();
    """

    with psycopg2.connect(**connection_params) as connection:
        with connection.cursor() as cursor:
            cursor.execute(table_sql)
            cursor.execute(function_sql)
            cursor.execute(trigger_sql)


def _movie_payloads():
    return [
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


def _populate_movies(connection_params):
    sql = """
    INSERT INTO ex06_movies (title, episode_nb, opening_crawl, director, producer, release_date)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (episode_nb)
    DO UPDATE SET
        title = EXCLUDED.title,
        opening_crawl = EXCLUDED.opening_crawl,
        director = EXCLUDED.director,
        producer = EXCLUDED.producer,
        release_date = EXCLUDED.release_date;
    """

    results = []
    with psycopg2.connect(**connection_params) as connection:
        connection.autocommit = True
        with connection.cursor() as cursor:
            for movie in _movie_payloads():
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


def init(request):
    try:
        _create_movies_table(_connection_params())
        return HttpResponse("OK")
    except Exception as error:
        return HttpResponse(str(error), status=500)


def populate(request):
    try:
        results = _populate_movies(_connection_params())
        return HttpResponse("<br>".join(results))
    except Exception as error:
        return HttpResponse(str(error), status=500)


def display(request):
    try:
        with psycopg2.connect(**_connection_params()) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT title, episode_nb, opening_crawl, director, producer, release_date, created, updated
                    FROM ex06_movies
                    ORDER BY episode_nb;
                    """
                )
                movies = cursor.fetchall()

        if not movies:
            return HttpResponse("No data available")

        rows = []
        for title, episode_nb, opening_crawl, director, producer, release_date, created, updated in movies:
            rows.append(
                "<tr>"
                f"<td>{escape(str(title))}</td>"
                f"<td>{escape(str(episode_nb))}</td>"
                f"<td>{escape('' if opening_crawl is None else str(opening_crawl))}</td>"
                f"<td>{escape(str(director))}</td>"
                f"<td>{escape(str(producer))}</td>"
                f"<td>{escape(str(release_date))}</td>"
                f"<td>{escape(str(created))}</td>"
                f"<td>{escape(str(updated))}</td>"
                "</tr>"
            )

        html = (
            "<table border='1'>"
            "<thead><tr>"
            "<th>title</th><th>episode_nb</th><th>opening_crawl</th>"
            "<th>director</th><th>producer</th><th>release_date</th>"
            "<th>created</th><th>updated</th>"
            "</tr></thead>"
            "<tbody>"
            + "".join(rows)
            + "</tbody></table>"
        )
        return HttpResponse(html)
    except Exception:
        return HttpResponse("No data available")


@csrf_exempt
def update(request):
    try:
        with psycopg2.connect(**_connection_params()) as connection:
            connection.autocommit = True
            with connection.cursor() as cursor:
                if request.method == "POST":
                    title = request.POST.get("title", "").strip()
                    opening_crawl = request.POST.get("opening_crawl", "")
                    if title:
                        cursor.execute(
                            "UPDATE ex06_movies SET opening_crawl = %s WHERE title = %s;",
                            (opening_crawl, title),
                        )

                cursor.execute("SELECT title FROM ex06_movies ORDER BY episode_nb;")
                titles = [row[0] for row in cursor.fetchall()]

        if not titles:
            return HttpResponse("No data available")

        options = "".join(f"<option value='{escape(t)}'>{escape(t)}</option>" for t in titles)
        html = (
            "<form method='post'>"
            "<select name='title' required>"
            f"{options}"
            "</select>"
            "<input type='text' name='opening_crawl' required>"
            "<button type='submit' name='update'>update</button>"
            "</form>"
        )
        return HttpResponse(html)
    except Exception:
        return HttpResponse("No data available")
