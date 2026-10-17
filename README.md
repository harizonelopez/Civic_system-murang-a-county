# Civic System

A small Flask application for reporting and tracking local public service issues. Citizens can create accounts, submit requests, and follow progress. Administrators can review submissions and update their status.

## Features

- Citizen registration and login
- Secure password submission and hashing
- Submit requests with category, location, title, and description
- Track Pending, In Progress, and Resolved statuses
- Admin dashboard with basic counts
- CSRF protection on forms
- SQLite for local development; PostgreSQL can be configured for deployment

## Run locally

Python 3.12 is recommended.

```powershell
py -m venv .venv
.venv\Scripts\python app.py
```

Open `http://127.0.0.1:5000`.


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
