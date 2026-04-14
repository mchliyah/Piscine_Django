# d09

Django final exercise project containing:

- `account`: AJAX login/logout page.
- `chat`: authenticated WebSocket chatrooms using jQuery.

## Chat features

- Room list page with links to database-backed rooms.
- Auth-only access to room list and room pages.
- WebSocket messaging (no AJAX) with jQuery frontend.
- Messages persisted in database and displayed in ascending order.
- Join notifications: `<username> has joined the chat` are persisted and broadcast to all users in room.

## Quick start

```bash
source ./env.sh
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

Open:

- `http://127.0.0.1:8000/account/`
- `http://127.0.0.1:8000/chat/`

## Tests

```bash
python manage.py test account chat
```
