# Advanced Django Project

## ex00 Overview
This project provides:
- a home page that redirects to the articles page
- an articles page displaying all articles in a table
- a login page using Django's authentication system

## Sample data (optional)
The project uses a Django fixture to populate the database with example users and articles:

- [fixtures/ex00_initial_data.json](fixtures/ex00_initial_data.json)

This fixture contains:
- 3 users
- 5 articles
- article content filled with placeholder text

## Load the fixture
After migrating, import the sample data with:

# Advanced Django Project

## ex00 Overview
This project provides:
- a home page that redirects to the articles page
- an articles page displaying every article as an HTML table (without full content)
# Advanced Django Project

Training project for Django 3 Advanced exercises `ex00` to `ex06`.

## Setup
```zsh
source .venv/bin/activate
python3 manage.py migrate
python3 manage.py loaddata fixtures/ex00_initial_data.json
```

## Run
```zsh
python3 manage.py runserver 127.0.0.1:8000
```

## Project layout
- `Advanced/`: project settings, URLs, and i18n routing
- `Templates/`: shared templates for all exercises
- `static/`: Bootstrap/menu CSS assets
- `fixtures/`: sample data for articles, users, and favourites
- `.vscode/launch.json`: debug profiles for step-by-step development

## Exercise summary

### `ex00` — Generic class views and models
- Builds `Article` and `UserFavouriteArticle` models.
- Provides `Home`, `Articles`, and `Login` pages with generic class-based views.
- Uses a fixture with 3 users and 5 articles.

### `ex01` — Generic class views again
- Adds `Publications`, `Detail`, `Logout`, and `Favourites`.
- Shows a user’s own publications and favourite articles.
- Includes article detail links and a logout link.

### `ex02` — `CreateView`
- Adds `Register`, `Publish`, and `Add to favourite` flows.
- Uses Django ready-made forms where appropriate.
- Sets `author` and `user` fields in the view during validation.

### `ex03` — Template tags and filters
- Adds a global menu visible from every page.
- Shows login form in the menu for anonymous users.
- Truncates article abstracts to 20 characters and adds a “published for” column.

### `ex04` — Bootstrap
- Applies Bootstrap styling to the menu/navbar.
- Loads shared Bootstrap-aware static CSS across templates.

### `ex05` — Internationalization
- Supports language-prefixed URLs such as `/en/articles/` and `/fr/articles/`.
- Translates the articles page and the menu.
- Includes language switch links on the articles page.

### `ex06` — Testing
- Verifies access control for `publications`, `publish`, and `favourites`.
- Verifies registered users cannot access the register form.
- Verifies the same article cannot be added twice to favourites.

## Fixture helpers
To regenerate the sample fixture with passwords you choose:
```zsh
python3 tools/generate_ex00_fixture.py \
  --alice-pass password123 \
  --bob-pass password123 \
  --charlie-pass password123 \
  --output fixtures/ex00_initial_data.json
```

## Debugging
Use VS Code launch profiles from `.vscode/launch.json`:
- `Django: Runserver (Step Debug)`
- `Django: Shell (Debug)`
- `Django: Load ex00 Fixture (Debug)`

Run a quick health check:
```zsh
python3 manage.py check
python3 manage.py test ex06
```