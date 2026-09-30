# Aakaar CR '26

An independent Aakaar College Representative portal using the supplied retro frontend and a Django backend.

## What works

- CR registration, login, logout, and password reset
- Participant profile and personal dashboard
- Admin-managed task publishing, deadlines, submissions, file/link evidence, review state, and point awards
- Automatically calculated public leaderboard
- Contact-message inbox in Django admin
- PostgreSQL-ready Render deployment configuration

## Local run

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-prod.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

Open `http://127.0.0.1:8000/`. Add tasks and review submissions at `/admin/` after setting the three `DJANGO_SUPERUSER_*` variables.

## Render

The included `render.yaml` provisions a separate service named `aakaar-cr-retro-demo` and a separate PostgreSQL database. Before deploying, set the `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, and `DJANGO_SUPERUSER_PASSWORD` environment variables in Render. Configure the SMTP variables too if password-reset emails should be delivered externally.
