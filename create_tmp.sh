#!/bin/bash

# Check for the correct number of arguments
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <project_name> <app_name1> [<app_name2> ...]"
    exit 1
fi

PROJECT_NAME=$1
shift
APPS=("$@")

# Create the root project directory
if [ ! -d "$PROJECT_NAME" ]; then
    mkdir -p "$PROJECT_NAME"
    echo "Created project directory: $PROJECT_NAME"
fi

# Create the core project directory (e.g., project_name/project_name)
CORE_DIR="$PROJECT_NAME/$PROJECT_NAME"
if [ ! -d "$CORE_DIR" ]; then
    mkdir -p "$CORE_DIR"
    echo "Created core directory: $CORE_DIR"
fi

# --- Create manage.py in the root project directory ---
cat > "$PROJECT_NAME/manage.py" << EOL
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '$PROJECT_NAME.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
EOL

# Make manage.py executable
chmod +x "$PROJECT_NAME/manage.py"
echo "Created and configured manage.py"

# --- Create requirements.txt in the root project directory ---
touch "$PROJECT_NAME/requirements.txt"
echo "Created requirements.txt"

# --- Create and populate core project files ---

# __init__.py
touch "$CORE_DIR/__init__.py"

# settings.py
cat > "$CORE_DIR/settings.py" << EOL
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-your-secret-key'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '$PROJECT_NAME.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = '$PROJECT_NAME.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EOL

# urls.py
cat > "$CORE_DIR/urls.py" << EOL
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
]
EOL

# wsgi.py
cat > "$CORE_DIR/wsgi.py" << EOL
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '$PROJECT_NAME.settings')
application = get_wsgi_application()
EOL

# asgi.py
cat > "$CORE_DIR/asgi.py" << EOL
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '$PROJECT_NAME.settings')
application = get_asgi_application()
EOL

echo "Generated core project files in: $CORE_DIR"

# Create a templates directory inside the project
TEMPLATES_DIR="$PROJECT_NAME/templates"
if [ ! -d "$TEMPLATES_DIR" ]; then
    mkdir -p "$TEMPLATES_DIR"
    echo "Created directory: $TEMPLATES_DIR"
fi

# Create each app with default files and content
for APP_NAME in "${APPS[@]}"; do
    APP_PATH="$PROJECT_NAME/$APP_NAME"
    mkdir -p "$APP_PATH"
    echo "Created app directory: $APP_PATH"

    # --- Create and populate files ---

    # __init__.py (empty)
    touch "$APP_PATH/__init__.py"

    # apps.py
    APP_NAME_PASCAL_CASE=$(echo "$APP_NAME" | sed -r 's/(^|-|_)(\w)/\U\2/g')
    cat > "$APP_PATH/apps.py" << EOL
from django.apps import AppConfig

class ${APP_NAME_PASCAL_CASE}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '$APP_NAME'
EOL

    # models.py
    cat > "$APP_PATH/models.py" << EOL
from django.db import models

# Create your models here.
EOL

    # views.py
    cat > "$APP_PATH/views.py" << EOL
from django.shortcuts import render

# Create your views here.
EOL

    # urls.py
    cat > "$APP_PATH/urls.py" << EOL
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
]
EOL

    echo "Generated files for app: $APP_NAME"
done

echo "Project '$PROJECT_NAME' and apps created successfully."
