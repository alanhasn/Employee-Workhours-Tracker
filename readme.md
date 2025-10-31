# Employee Workhours

Small Django app to track employee work entries, optional extra hours, and provide simple analytics per employee (monthly and yearly totals).

## Overview

This repository contains a Django (5.2.x) application that records employee work entries and computes durations and extra hours. It includes an analytics view that aggregates work totals per employee and a simple admin login flow.

Key features:
- Create, edit, and delete work entries
- Track extra hours and total hours per entry
- Dashboard and paginated lists of entries
- Analytics page with monthly and yearly totals
- Admin login required for the app views

## Tech Stack

- Python 3.12.x
- Django 5.2.x
- SQLite (development)
- Tailwind (CDN in templates) for styling
- Chart.js for analytics charts

## Repository layout (key files)

- `workhours/` — Django project package
	- `settings.py`, `urls.py`, `wsgi.py`, `asgi.py`
- `tracker/` — main app
	- `models.py` — WorkEntry model and logic for duration/total hours
	- `forms.py` — forms for work entries and filters
	- `views.py` — dashboard, CRUD views, analytics, and login view
	- `urls.py` — app routes (the app is served under `/app/`)
	- `templates/tracker/` — templates including `dashboard.html`, `workentry_form.html`, `analytics.html`, `login.html`
	- `templatetags/tracker_filters.py` — `format_hours` and `format_decimal_hours` template filters

## Setup (development, Windows / PowerShell)

1. Create a virtual environment and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Apply migrations:

```powershell
python workhours\manage.py migrate
```

4. Create a superuser (recommended) or use the development account created during initial work. To create a new superuser run:

```powershell
python workhours\manage.py createsuperuser
```

5. Run the development server:

```powershell
python workhours\manage.py runserver
```

Open http://127.0.0.1:8000/ — the project redirects to `/app/` where the login page is shown first.

## Usage

- Log in via `/app/` (admin login). After login you can access the dashboard, add/edit/delete entries, and view analytics at `/app/analytics/`.
- Templates use named URL patterns so routes are served under `/app/` (see `workhours/urls.py` and `tracker/urls.py`).

## Tests

There are no automated tests included by default. To add tests, create `tests.py` files in the `tracker` app and run:

```powershell
python workhours\manage.py test
```