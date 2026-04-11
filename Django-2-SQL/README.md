
# Quick exercise-by-exercise overview:

Ex00: create a table in PostgreSQL from a Django view using raw SQL.

Ex01: define the same table structure as a Django ORM model.

Ex02: insert Star Wars data with raw SQL.

Ex03: insert the same data with ORM.

Ex04: delete rows using raw SQL + form.

Ex05: delete rows using ORM + form.

Ex06: update rows in SQL and manage timestamps (created/updated).

Ex07: same update logic but with ORM timestamp features.

Ex08: introduce SQL relations (Foreign Key) and display joined data.

Ex09: do the same relation logic with ORM + fixtures.

Ex10: build a Many-to-Many search feature (movies ↔ characters) with form filters.

# ex00 - SQL table creation with psycopg2

## Shared DB credentials for all SQL apps

SQL exercises now use a single connection helper in `d05/db.py`.

All credentials can be configured once through environment variables or a `.env` file at project root:

1. `cp .env.example .env`
2. Edit `.env` with your real PostgreSQL values
3. Start the project as usual (`./run.sh` loads `.env` automatically)

This removes repeated credentials from views and keeps secrets out of source control.

This exercise exposes a Django view at:

- `http://127.0.0.1:8000/ex00/init`

The view uses `psycopg2` to connect to PostgreSQL and creates the table `ex00_movies` if it does not already exist.

## Environment variables

The project reads PostgreSQL connection settings from environment variables or `.env`:

- `POSTGRES_DB` or `DB_NAME` (required)
- `POSTGRES_USER` or `DB_USER` (required)
- `POSTGRES_PASSWORD` or `DB_PASSWORD` (required)
- `POSTGRES_HOST` or `DB_HOST` (required)
- `POSTGRES_PORT` or `DB_PORT` (required)

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

# ex01 - ORM Models definition

This exercise defines Django ORM models equivalent to the SQL schema created in ex00.

The `Movies` model has the following fields:

- `title`: CharField (unique, max_length=64)
- `episode_nb`: IntegerField (primary key)
- `opening_crawl`: TextField (nullable)
- `director`: CharField (max_length=32)
- `producer`: CharField (max_length=128)
- `release_date`: DateField

This model structure mirrors the ex00 SQL table, providing an object-oriented interface for database operations.

## ex01 setup

```bash
cd /goinfre/mchliyah/Piscine_Django/Django-2-SQL
source ./env.sh
python manage.py makemigrations ex01
python manage.py migrate
```

# ex02 - SQL data insertion

This exercise exposes two views:

- `http://127.0.0.1:8000/ex02/init` — creates `ex02_movies` table using psycopg2
- `http://127.0.0.1:8000/ex02/populate` — inserts the 7 Star Wars movies using raw SQL

`/ex02/populate` returns one line per insert (`OK` or an error message).

## ex02 setup

```bash
cd /goinfre/mchliyah/Piscine_Django/Django-2-SQL
source ./env.sh
python manage.py runserver
```

## ex02 quick check

```bash
# 1) Create the table
curl -s http://127.0.0.1:8000/ex02/init

# 2) Populate with the 7 Star Wars movies
curl -s http://127.0.0.1:8000/ex02/populate
```

# ex03 - ORM data insertion

This exercise exposes two views:

- `http://127.0.0.1:8000/ex03/populate` — inserts the 7 Star Wars movies with Django ORM
- `http://127.0.0.1:8000/ex03/display` — displays all data as an HTML table

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

# ex08 - SQL Foreign Keys

This exercise exposes two views:

- `http://127.0.0.1:8000/ex08/populate` — creates tables and loads data from CSV/TSV files
- `http://127.0.0.1:8000/ex08/display` — displays linked data from both tables

`/ex08/populate` inserts data into `ex08_movies` and `ex08_people` tables, establishing a relationship between them.

`/ex08/display` shows the `Movies` and `People` tables content as an HTML table with proper joins. If there is no data, or an error, it returns:

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

# ex09 - ORM Foreign Keys with Fixtures

This exercise exposes one view:

- `http://127.0.0.1:8000/ex09/display`

`/ex09/display` shows the `People` table content as an HTML table, filtered to show only people from windy planets. If there is no data, or an error, it returns:

- `No data available`

Models:
- **Planets** (11 fields): name, climate, diameter, orbital_period, population, rotation_period, surface_water, terrain, created, updated
- **People** (10 fields): name, birth_year, gender, eye_color, hair_color, height, mass, homeworld (FK to Planets), created, updated

Fixture loads 60 planets and 87 people (86 with homeworld FK, 1 null).

## ex09 setup

To populate the database, run:

```bash
cd /goinfre/mchliyah/Piscine_Django/Django-2-SQL
source ./env.sh
python manage.py makemigrations ex09
python manage.py migrate
python manage.py loaddata ex09/fixtures/ex09_initial_data.json
python manage.py runserver
```

## ex09 quick check

```bash
# 1) Run migrations
python manage.py makemigrations ex09
python manage.py migrate

# 2) Load fixture data
python manage.py loaddata ex09/fixtures/ex09_initial_data.json

# 3) Display people from windy planets
curl -s http://127.0.0.1:8000/ex09/display
```

# ex10 - ORM Many-to-Many relationships

This exercise introduces Many-to-Many relationships between Movies and People:

- `http://127.0.0.1:8000/ex10/` — displays a search form with filters:
  - Movies minimum release date (date input)
  - Movies maximum release date (date input)
  - Planet diameter greater than (integer input)
  - Character gender (dropdown list showing unique values from database)

The search returns characters who:
- Have matching gender
- Appear in films released within the date range
- Live on planets with diameter >= specified value

Results display:
- Character name
- Character gender
- Film title
- Homeworld name
- Homeworld diameter

If no matches found, displays: `Nothing corresponding to your research`

## ex10 Models

- **Planets**: name, climate, diameter, orbital_period, population, rotation_period, surface_water, terrain, timestamps
- **People**: name, birth_year, gender, eye_color, hair_color, height, mass, homeworld (FK), timestamps
- **Movies**: title, episode_nb, opening_crawl, director, producer, release_date, **characters (M2M to People)**, timestamps

Many-to-Many creates an intermediate table (`ex10_movies_characters`) for cross-references between movies and characters.

## ex10 setup

```bash
cd /goinfre/mchliyah/Piscine_Django/Django-2-SQL
source ./env.sh
python manage.py makemigrations ex10
python manage.py migrate
python manage.py loaddata ex10/fixtures/ex10_initial_data.json
python manage.py runserver
```

## ex10 quick check

```bash
# 1) Run migrations
python manage.py makemigrations ex10
python manage.py migrate

# 2) Load fixture data (60 planets, 87 people, 7 movies)
python manage.py loaddata ex10/fixtures/ex10_initial_data.json

# 3) Display search form
curl -s http://127.0.0.1:8000/ex10/

# 4) Search for female characters (1900-2000, diameter > 11000)
curl -s -X POST http://127.0.0.1:8000/ex10/ \
  -d "min_release_date=1900-01-01" \
  -d "max_release_date=2000-01-01" \
  -d "planet_diameter_gt=11000" \
  -d "gender=female"
```

Expected results (5 entries):
- The Phantom Menace - Padmé Amidala - female - Naboo - 12120
- A New Hope - Leia Organa - female - Alderaan - 12500
- The Empire Strikes Back - Leia Organa - female - Alderaan - 12500
- Return of the Jedi - Leia Organa - female - Alderaan - 12500
- Return of the Jedi - Mon Mothma - female - Chandrila - 13500
