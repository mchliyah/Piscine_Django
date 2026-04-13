# Django-3-Sessions

Simple Django training project implementing:
- `ex00`: anonymous session username (42 seconds)
- `ex01`: registration/login/logout
- `ex02`: tips system with `ModelForm`
- `ex03`: upvote/downvote/delete actions
- `ex04`: delete authorization (author or privileged user)
- `ex05`: custom downvote restriction logic
- `ex06`: custom user + reputation-based automation

## Submission Structure
This piscine is delivered as **one evolving project** in a single folder (`ex/` in subject wording),
not one separate Django project per exercise.

- Keep one Django project root.
- Add/extend apps/features progressively across exercises.
- Final state includes all features from `ex00` to `ex06`.

Current app roles:
- `ex00`: anonymous session display name logic
- `ex01`: registration/login/logout pages and form flow
- `ex02`: tip model + homepage listing + tip creation form
- `ex03`: vote/delete endpoints and action handling
- `ex06`: custom user model and reputation authorization rules

## Exercise Progression (Ex04 / Ex05 / Ex06)
This project keeps a **single final codebase** (as requested by the piscine `ex/` turn-in model).

- `ex04` introduced restricted tip deletion (author exception + restricted users).
- `ex05` introduced restricted downvote authorization (author exception + restricted users).
- `ex06` automates those authorizations using reputation with a custom user model.

In the final state, `ex04` and `ex05` restrictions are still respected, but authorization is now computed dynamically by reputation rules from `ex06`:
- Downvote on others' tips unlocked at **15** reputation.
- Delete on others' tips unlocked at **30** reputation.
- Tip author can always downvote/delete their own tip.

## Requirements
- Python 3
- Packages from `requirements.txt`

## Setup
```bash
cd /home/mchliyah/Piscine_Django/Django-3-Sessions
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
cd /home/mchliyah/Piscine_Django/Django-3-Sessions
source .venv/bin/activate
python manage.py migrate
python manage.py runserver
```

## Tests
```bash
cd /home/mchliyah/Piscine_Django/Django-3-Sessions
source .venv/bin/activate
python manage.py test
```

## Manual Link Checks
After running the server, check these links one by one:

1. Home page: `http://127.0.0.1:8000/`
2. Registration page: `http://127.0.0.1:8000/register/`
3. Login page: `http://127.0.0.1:8000/login/`
4. Logout link (only visible when logged in): `http://127.0.0.1:8000/logout/`
5. Ex00 page: `http://127.0.0.1:8000/ex00/`

Quick behavior checklist:
- Anonymous user sees `Registration` and `Log in` links.
- Logged-in user sees `Log out` link and username in greeting.
- Tip form appears only when logged in.
- Posted tips appear in the tips list with author and date.
