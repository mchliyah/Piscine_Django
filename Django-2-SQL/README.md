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

```bash
docker exec -it djangotraining-postgres bash
psql -h localhost -U djangouser -d djangotraining -c "\dt"
```

# ex03 - ORM data insertion

This exercise exposes two views:

- `http://127.0.0.1:8000/ex03/populate`
- `http://127.0.0.1:8000/ex03/display`

`/ex03/populate` inserts the 7 Star Wars movies with Django ORM and returns one line per insert (`OK` or an error message).

`/ex03/display` shows the `Movies` table content as an HTML table. If there is no data, or an error, it returns:

- `No data available`

## ex03 setup

```bash
cd /goinfre/mchliyah/Piscine_Django/Django-2-SQL
source ./env.sh
python manage.py makemigrations ex03
python manage.py migrate
python manage.py runserver
```


## ex03 quick check

```bash
curl -s http://127.0.0.1:8000/ex03/populate
curl -s http://127.0.0.1:8000/ex03/display
```

# ex04 - SQL data deletion with form

This exercise exposes four views:

- `http://127.0.0.1:8000/ex04/init` — creates `ex04_movies` table
- `http://127.0.0.1:8000/ex04/populate` — inserts the 7 Star Wars movies (can reinitialize if deleted)
- `http://127.0.0.1:8000/ex04/display` — displays all data as an HTML table
- `http://127.0.0.1:8000/ex04/remove` — shows an HTML form with a dropdown list of titles and a submit button to delete

The `remove` endpoint allows deletion of movies. After deletion, the form is redisplayed with the updated list of remaining titles.

## ex04 quick check

```bash
curl -s http://127.0.0.1:8000/ex04/init

curl -s http://127.0.0.1:8000/ex04/populate | head -1

curl -s http://127.0.0.1:8000/ex04/display

curl -s http://127.0.0.1:8000/ex04/remove

# curl -s -X POST http://127.0.0.1:8000/ex04/remove -d "title=The%20Force%20Awakens"
```

# ex05 - ORM data deletion with form

This exercise exposes three views using Django ORM:

- `http://127.0.0.1:8000/ex05/populate` — inserts the 7 Star Wars movies (can reinitialize if deleted)
- `http://127.0.0.1:8000/ex05/display` — displays all data as an HTML table
- `http://127.0.0.1:8000/ex05/remove` — shows an HTML form with a dropdown list of titles and a submit button to delete

The `remove` endpoint allows deletion of movies via ORM. After deletion, the form is redisplayed with the updated list of remaining titles.

## ex05 quick check

```bash
# 1) Populate with data
curl -s http://127.0.0.1:8000/ex05/populate | head -1

# 2) Display all data
curl -s http://127.0.0.1:8000/ex05/display

# 3) Show the remove form
curl -s http://127.0.0.1:8000/ex05/remove

# 4) Delete a movie (from a running server or form submission)
# curl -s -X POST http://127.0.0.1:8000/ex05/remove -d "title=The%20Phantom%20Menace"
```

# ex06 - SQL data update with timestamps

This exercise exposes four SQL-based views:

- `http://127.0.0.1:8000/ex06/init` — creates `ex06_movies` with `created` and `updated` timestamps and installs the update trigger
- `http://127.0.0.1:8000/ex06/populate` — inserts/reinserts the 7 Star Wars movies
- `http://127.0.0.1:8000/ex06/display` — displays all columns from `ex06_movies` in an HTML table
- `http://127.0.0.1:8000/ex06/update` — shows a form to select a movie and update `opening_crawl`

The trigger keeps `created` unchanged and refreshes `updated` on each row update.

## ex06 quick check

```bash
# 1) Create table + trigger
curl -s http://127.0.0.1:8000/ex06/init

# 2) Populate movies
curl -s http://127.0.0.1:8000/ex06/populate

# 3) Display all data
curl -s http://127.0.0.1:8000/ex06/display

# 4) Show update form
curl -s http://127.0.0.1:8000/ex06/update

# 5) Submit an update
curl -s -X POST http://127.0.0.1:8000/ex06/update -d "title=A%20New%20Hope" -d "opening_crawl=New%20crawl%20text"

```

# ex07 - ORM data update with timestamps

This exercise exposes three ORM-based views:

- `http://127.0.0.1:8000/ex07/populate` — inserts/reinserts the 7 Star Wars movies
- `http://127.0.0.1:8000/ex07/display` — displays all columns from `Movies` in an HTML table
- `http://127.0.0.1:8000/ex07/update` — shows a form to select a movie and update `opening_crawl`

The model uses automatic ORM timestamps:

- `created`: set on creation (`auto_now_add=True`)
- `updated`: refreshed on each save (`auto_now=True`)

## ex07 quick check

```bash
# 1) Run migrations
python manage.py makemigrations ex07
python manage.py migrate

# 2) Populate movies
curl -s http://127.0.0.1:8000/ex07/populate

# 3) Display all data
curl -s http://127.0.0.1:8000/ex07/display

# 4) Show update form
curl -s http://127.0.0.1:8000/ex07/update

# 5) Submit an update
curl -s -X POST http://127.0.0.1:8000/ex07/update -d "title=A%20New%20Hope" -d "opening_crawl=ORM%20new%20crawl"
```

# ex08 - SQL - Foreign Key

This exercise exposes three views:

- `http://127.0.0.1:8000/ex08/populate`
- `http://127.0.0.1:8000/ex08/display`

`/ex08/populate` inserts data into `ex08_movies` and `ex08_actors` tables, establishing a relationship between them.

`/ex08/display` shows the `Movies` and `Actors` tables content as an HTML table with proper joins. If there is no data, or an error, it returns:

- `No data available`

## ex08 setup

```bash
cd /goinfre/mchliyah/Piscine_Django/Django-2-SQL
source ./env.sh
python manage.py makemigrations ex08
python manage.py migrate
python manage.py runserver
```


## ex08 quick check

```bash
curl -s http://127.0.0.1:8000/ex08/populate
curl -s http://127.0.0.1:8000/ex08/display
```

# ex09 - ORM data loading from JSON

This exercise exposes one view:

- `http://127.0.0.1:8000/ex09/display`

`/ex09/display` shows the `People` table content as an HTML table, filtered to show only people from windy planets. If there is no data, or an error, it returns:

- `No data available`

## ex09 setup

To populate the database, run:

```bash
cd /goinfre/mchliyah/Piscine_Django/Django-2-SQL
source .venv/bin/activate
python3 manage.py loaddata ex09/fixtures/ex09_initial_data.json
```

- `http://127.0.0.1:8000/ex09/display`
