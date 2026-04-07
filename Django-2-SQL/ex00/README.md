# ex00 - SQL table creation with psycopg2

This exercise exposes a Django view at:

- `http://127.0.0.1:8000/ex00/init`

The view uses `psycopg2` to connect to PostgreSQL and creates the table `ex00_movies` if it does not already exist.

## Environment variables (optional)

The view reads PostgreSQL connection settings from environment variables, with sensible local defaults:

- `POSTGRES_DB` or `DB_NAME` (default: `postgres`)
- `POSTGRES_USER` or `DB_USER` (default: `postgres`)
- `POSTGRES_PASSWORD` or `DB_PASSWORD` (default: empty)
- `POSTGRES_HOST` or `DB_HOST` (default: `localhost`)
- `POSTGRES_PORT` or `DB_PORT` (default: `5432`)

## Run

```bash
cd /goinfre/mchliyah/Piscine_Django/Django-2-SQL/ex00
python3 -m pip install -r requirements.txt
python3 manage.py runserver
```

Then open:

- `http://127.0.0.1:8000/ex00/init`

## One-command launch

```bash
cd /goinfre/mchliyah/Piscine_Django/Django-2-SQL/ex00
chmod +x run.sh
./run.sh
```

You can override DB settings before launch:

```bash
export POSTGRES_DB=postgres
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=''
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
./run.sh
```

Notes:

- `GET /` and `GET /favicon.ico` returning `404` is expected for this exercise.
- The important route is `GET /ex00/init`.

## Troubleshooting `500` on `/ex00/init`

If you see an error like:

- `connection to server ... failed`
- `No such file or directory` (socket)

then PostgreSQL is not running/reachable with current settings.

Quick checks:

```bash
psql --version
```

If your PostgreSQL listens on TCP:

```bash
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
./run.sh
```

If your PostgreSQL uses local Unix socket, leave `POSTGRES_HOST` empty (default in `run.sh`).
