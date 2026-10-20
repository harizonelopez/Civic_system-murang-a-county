# Civic System — Murang’a County

A Flask-based public service request management system that allows citizens to report local service issues and track their progress. Administrators can review submitted requests, monitor statistics, and update request statuses through a dedicated admin portal.

## Live Demo

**Application:** https://civic-system-muranga-county.onrender.com

**Admin Portal:** https://civic-system-muranga-county.onrender.com/admin/login

## Evaluation Access

The following demo credentials are provided for project evaluation.

| Field           | Details            |
|-----------------|--------------------|
| Admin Email     | `jarvis@gmail.com` |
| Admin Password  | `jarvis123`        |

**Administrator capabilities:**
- View submitted citizen service requests.
- Review request details, categories, descriptions, and locations.
- Update request statuses.
- Monitor service request statistics through the admin dashboard.


## Features

### Citizen Features
- Citizen registration and login.
- Secure password hashing.
- Submit public service requests with a title, category, location, and description.
- Track request progress.
- View request statuses: Pending, In Progress, and Resolved.
- Access a personal dashboard to view submitted requests.

### Administrator Features
- Dedicated administrator login page.
- Protected administrator dashboard.
- View and review submitted requests.
- Update the status of service requests.
- View basic request statistics.

## Technology Stack

- **Backend:** Python, Flask
- **Database:** SQLite
- **ORM:** Flask-SQLAlchemy, SQLAlchemy
- **Authentication:** Flask-Login
- **Forms and Validation:** Flask-WTF, WTForms
- **Frontend:** HTML, CSS, Bootstrap, Jinja2
- **Deployment:** Render

## Run Locally

Python 3.14 is recommended.

### 1. Clone the repository

```powershell
 git clone https://github.com/harizonelopez/Civic_system_murang-a-county.git
 cd Civic_system_murang-a-county
```

### 2. Create a virtual environment

```powershell
 python -m venv .env
```

### 3. Activate the environment

```powershell
 .env\scripts\activate
```

### 4. Install dependencies

```powershell
 pip install -r requirements.txt
```

### 5. Start the application

```powershell
 python app.py
```

Open the local application at:

 https://127.0.0.1:5000

## Evaluation Notes

During evaluation, reviewers can:

1. Open the live application.
2. Register a citizen account and log in.
3. Submit a sample public service request.
4. Open the dedicated admin portal.
5. Log in using the demo credentials above.
6. Review the submitted request and change its status.
7. Verify the updated status through the citizen dashboard.

## Future Improvements

Potential improvements include:
- Email notifications when request statuses change.
- Request search, filtering, and pagination.
- More detailed administrative reporting.
- Audit logs for administrator actions.
- Improved deployment configuration and automated testing.


## Disclaimer

This project was developed for educational purposes to demonstrate web application development, database integration, authentication, access control, and public service request management. It's NOT an official Murang’a County Government system.
