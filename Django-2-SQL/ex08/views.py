from django.shortcuts import render
from django.http import HttpResponse
import psycopg2
import os

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST', 'localhost'),
        dbname=os.environ.get('POSTGRES_DB', 'piscine_django'),
        user=os.environ.get('POSTGRES_USER', 'mchliyah'),
        password=os.environ.get('POSTGRES_PASSWORD', 'mysecretpassword'),
        port=os.environ.get('POSTGRES_PORT', '5432')
    )

def init(request):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DROP TABLE IF EXISTS ex08_people;
            DROP TABLE IF EXISTS ex08_planets;
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ex08_planets (
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) UNIQUE NOT NULL,
                climate VARCHAR,
                diameter INT,
                orbital_period INT,
                population BIGINT,
                rotation_period INT,
                surface_water REAL,
                terrain VARCHAR(128)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ex08_people (
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) UNIQUE NOT NULL,
                birth_year VARCHAR(32),
                gender VARCHAR(32),
                eye_color VARCHAR(32),
                hair_color VARCHAR(32),
                height INT,
                mass REAL,
                homeworld VARCHAR(64),
                FOREIGN KEY (homeworld) REFERENCES ex08_planets(name)
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Error: {e}")

def populate(request):
    success_messages = []
    error_messages = []
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Populate ex08_planets
        try:
            with open('d05_re/planets.csv', 'r') as f:
                # Skip header
                next(f)
                cursor.copy_expert("COPY ex08_planets(name, climate, diameter, orbital_period, population, rotation_period, surface_water, terrain) FROM STDIN WITH CSV HEADER", f)
            conn.commit()
            success_messages.append("OK: ex08_planets populated successfully.")
        except Exception as e:
            conn.rollback()
            error_messages.append(f"Error populating ex08_planets: {e}")

        # Populate ex08_people
        try:
            with open('d05_re/people.csv', 'r') as f:
                # Skip header
                next(f)
                cursor.copy_expert("COPY ex08_people(name, birth_year, gender, eye_color, hair_color, height, mass, homeworld) FROM STDIN WITH CSV HEADER", f)
            conn.commit()
            success_messages.append("OK: ex08_people populated successfully.")
        except Exception as e:
            conn.rollback()
            error_messages.append(f"Error populating ex08_people: {e}")

        cursor.close()
        conn.close()

    except Exception as e:
        error_messages.append(f"Database connection error: {e}")

    if error_messages:
        return HttpResponse("<br>".join(error_messages))
    else:
        return HttpResponse("<br>".join(success_messages))


def display(request):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.name, p.homeworld, pl.climate
            FROM ex08_people p
            JOIN ex08_planets pl ON p.homeworld = pl.name
            WHERE pl.climate LIKE '%windy%'
            ORDER BY p.name;
        """)
        people = cursor.fetchall()
        cursor.close()
        conn.close()
        if people:
            return render(request, 'ex08/display.html', {'people': people})
        else:
            return HttpResponse("No data available")
    except Exception as e:
        return HttpResponse(f"No data available: {e}")
