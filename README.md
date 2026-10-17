# Public Service Request System

A small Flask application for reporting and tracking local public service issues. Citizens can create accounts, submit requests, and follow progress. Administrators can review submissions and update their status.

## Features

- Citizen registration and login
- Secure password hashing
- Submit requests with category, location, title, and description
- Track Pending, In Progress, and Resolved statuses
- Admin dashboard with basic counts
- CSRF protection on forms
- SQLite for local development; PostgreSQL can be configured for deployment

## Run locally

Python 3.11 or newer is recommended.

```powershell
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
$env:SECRET_KEY="a-long-random-local-secret"
$env:ADMIN_EMAIL="admin@example.com"
$env:ADMIN_PASSWORD="Choose-A-Strong-Password"
.venv\Scripts\python app.py
```

Open `http://127.0.0.1:5000`.

## Deploy on Render

1. Push this project to a GitHub repository.
2. In Render, create a **New Web Service** and connect the repository.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Add environment variables:
   - `SECRET_KEY`: a long random secret
   - `ADMIN_EMAIL`: the administrator login email
   - `ADMIN_PASSWORD`: a strong administrator password
   - `DATABASE_URL`: a PostgreSQL connection string if you have a persistent database
6. Deploy and open the public URL.

**Important:** Render's free web services have an ephemeral filesystem. The default SQLite database may be reset after restarts or deploys. For data you need to keep, connect a PostgreSQL database and set `DATABASE_URL`. Do not use the demo admin password in a real deployment.

## Project structure

```text
public_service_request_system/
├── app.py
├── requirements.txt
├── render.yaml
├── README.md
├── .gitignore
├── static/
│   └── css/
│       └── style.css
└── templates/
```

## Evaluation notes

The main workflow is: register as a citizen, submit a request, sign in with the administrator account, and change the request status. The code is intentionally kept in a single application module so it is easy to follow during a short project build.
