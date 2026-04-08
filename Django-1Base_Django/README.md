# Django-1Base_Django

This folder is restructured as **one Django project root** with:

- one `manage.py`
- one project config package `d05/` (`settings.py`, `urls.py`, `wsgi.py`, `asgi.py`)
- four apps: `ex00`, `ex01`, `ex02`, `ex03`
- shared templates in `Templates/`

## Quick start

```bash
cd /path_to/Django-1Base_Django
source ./env.sh
python manage.py check
python manage.py runserver
```

Then open:

- `http://127.0.0.1:8000/ex00`
- `http://127.0.0.1:8000/ex01/django`
- `http://127.0.0.1:8000/ex01/display`
- `http://127.0.0.1:8000/ex01/templates`
- `http://127.0.0.1:8000/ex02`
- `http://127.0.0.1:8000/ex03`

## Static files

```bash
python manage.py collectstatic --noinput
```
