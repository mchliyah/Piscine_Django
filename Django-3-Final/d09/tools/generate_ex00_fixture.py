#!/usr/bin/env python3

"""Generate a Django fixture for ex00 with known plaintext passwords.

This script hashes the chosen passwords with Django and writes a fixture
containing 3 users and 5 articles.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import django
from django.contrib.auth.hashers import make_password


DEFAULT_OUTPUT = Path("account/fixtures/ex00_initial_data.generated.json")
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def build_fixture(user_passwords: list[str]) -> list[dict[str, object]]:
    users = [
        {
            "model": "auth.user",
            "pk": 101,
            "fields": {
                "password": make_password(user_passwords[0]),
                "last_login": None,
                "is_superuser": False,
                "username": "alice",
                "first_name": "",
                "last_name": "",
                "email": "alice@example.com",
                "is_staff": False,
                "is_active": True,
                "date_joined": "2026-04-13T10:00:00Z",
                "groups": [],
                "user_permissions": [],
            },
        },
        {
            "model": "auth.user",
            "pk": 102,
            "fields": {
                "password": make_password(user_passwords[1]),
                "last_login": None,
                "is_superuser": False,
                "username": "bob",
                "first_name": "",
                "last_name": "",
                "email": "bob@example.com",
                "is_staff": False,
                "is_active": True,
                "date_joined": "2026-04-13T10:00:00Z",
                "groups": [],
                "user_permissions": [],
            },
        },
        {
            "model": "auth.user",
            "pk": 103,
            "fields": {
                "password": make_password(user_passwords[2]),
                "last_login": None,
                "is_superuser": False,
                "username": "charlie",
                "first_name": "",
                "last_name": "",
                "email": "charlie@example.com",
                "is_staff": False,
                "is_active": True,
                "date_joined": "2026-04-13T10:00:00Z",
                "groups": [],
                "user_permissions": [],
            },
        },
    ]

    articles = [
        {
            "model": "ex00.article",
            "pk": 201,
            "fields": {
                "title": "Django Generic Views",
                "content": "Lorem ipsum dolor sit amet.",
                "author": 101,
                "synopsis": "A short overview of Django generic class-based views.",
                "created": "2026-04-13T10:10:00Z",
            },
        },
        {
            "model": "ex00.article",
            "pk": 202,
            "fields": {
                "title": "ORM Basics",
                "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "author": 102,
                "synopsis": "How to query models with Django ORM.",
                "created": "2026-04-13T10:20:00Z",
            },
        },
        {
            "model": "ex00.article",
            "pk": 203,
            "fields": {
                "title": "Template Rendering",
                "content": "Lorem ipsum dolor sit amet, sed do eiusmod tempor.",
                "author": 103,
                "synopsis": "Rendering dynamic HTML using Django templates.",
                "created": "2026-04-13T10:30:00Z",
            },
        },
        {
            "model": "ex00.article",
            "pk": 204,
            "fields": {
                "title": "Authentication Flow",
                "content": "Lorem ipsum dolor sit amet, ut labore et dolore magna aliqua.",
                "author": 101,
                "synopsis": "A quick explanation of login and session workflow.",
                "created": "2026-04-13T10:40:00Z",
            },
        },
        {
            "model": "ex00.article",
            "pk": 205,
            "fields": {
                "title": "Migrations 101",
                "content": "Lorem ipsum dolor sit amet, quis nostrud exercitation.",
                "author": 102,
                "synopsis": "How and why to create and apply migrations.",
                "created": "2026-04-13T10:50:00Z",
            },
        },
    ]

    return users


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate the ex00 fixture JSON.")
    parser.add_argument("--alice-pass", default="student1", help="Plain password for alice")
    parser.add_argument("--bob-pass", default="student2", help="Plain password for bob")
    parser.add_argument("--charlie-pass", default="student3", help="Plain password for charlie")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output JSON file")
    return parser.parse_args()


def main() -> None:
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "d09.settings")
    django.setup()

    args = parse_args()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fixture = build_fixture([args.alice_pass, args.bob_pass, args.charlie_pass])
    output_path.write_text(json.dumps(fixture, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()