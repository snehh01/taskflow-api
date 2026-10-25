# TaskFlow — Task Management REST API

**A task management application.**

TaskFlow combines a REST API with a responsive web dashboard for creating, tracking, searching, filtering, and updating tasks. It includes Pydantic validation, database integration, and automated tests.

**Release classification: **v1.1.0 (QA-hardened release)**

TaskFlow is a Python/FastAPI task manager with a polished, responsive web dashboard. It demonstrates CRUD APIs, validation, SQLAlchemy database integration, filtering/search, HTML form workflows, and automated tests. The interface is built with **Jinja2 templates, HTML, CSS, and vanilla JavaScript** — not Streamlit.


## Dashboard Preview

![TaskFlow dashboard overview](screenshots/Dashboard.png)

![TaskFlow task management interface](screenshots/Dashboard2.png)


## Features

- Create, list, view, update, and delete tasks through a REST API.
- Task fields: title, description, status (`pending`, `in_progress`, `completed`), priority (`low`, `medium`, `high`), due date, and creation timestamp.
- Filter tasks by status or priority and search by title.
- Responsive dashboard with summary cards, search/filter controls, animated task entry, create-task modal, status updates, and delete confirmation.
- SQLite by default so the app runs locally without database setup; configurable PostgreSQL support.
- Pydantic validation, clear 404 responses, health check, and Swagger/OpenAPI docs.
- Automated tests for core API and UI workflows.

## Stack

Python 3.11+ · FastAPI · SQLAlchemy 2 · Pydantic v2 · Jinja2 · python-dotenv · SQLite / PostgreSQL · Pytest · HTML/CSS/JavaScript

## Run locally (Windows PowerShell)

1. Install Python 3.11 or newer and open this project folder in VS Code.
2. Create and activate a virtual environment:

   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt and run `\.venv\Scripts\activate.bat`, or run `.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.venv\Scripts\python.exe -m uvicorn app.main:app --reload` without activating.

3. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Start the server:

   ```powershell
   python -m uvicorn app.main:app --reload --reload-dir app
   ```

5. Open the dashboard at **http://127.0.0.1:8000**.
   - API documentation: http://127.0.0.1:8000/docs
   - Alternative API docs: http://127.0.0.1:8000/redoc
   - Health check: http://127.0.0.1:8000/health

The SQLite database `taskflow.db` is created automatically in the working directory on first startup. It is ignored by Git. The Google Fonts link is optional; if offline, the app falls back to system fonts. To use a `.env` file, copy `.env.example` to `.env` and edit `DATABASE_URL`; the project loads it automatically. Environment variables set by your shell or hosting provider take precedence.

## PostgreSQL configuration (optional)

1. Create a PostgreSQL database, for example `taskflow`.
2. Copy `.env.example` to `.env` and set `DATABASE_URL`. For example:

   ```text
   DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/taskflow
   ```

3. Install the PostgreSQL driver with `pip install "psycopg[binary]"`.
4. Export the environment variable in PowerShell before starting the app:

   ```powershell
   $env:DATABASE_URL="postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/taskflow"
   python -m uvicorn app.main:app --reload --reload-dir app
   ```

Replace the example credentials with your own. Do not commit `.env` or credentials. For a portfolio deployment, configure `DATABASE_URL` in the hosting provider's environment settings.

## Run tests

```powershell
python -m pytest -v
```

Tests use an isolated in-memory SQLite database. They cover health, CRUD, search and filtering, validation, missing records, null-field PATCH protection, static assets, API docs, and dashboard create/update/delete workflows. The local app database is not used by the test fixtures.


## Upload to GitHub

1. Create an empty **public** repository named `taskflow-api` on GitHub. Do not initialize it with a README or license because those are already included here.
2. Open this project folder in VS Code and run:

   ```powershell
   git init
   git add .
   git status
   git commit -m "Release TaskFlow API v1.0.1"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/taskflow-api.git
   git push -u origin main
   ```

3. Replace `YOUR_USERNAME` with your GitHub username. Review `git status` before committing. Never commit `.env`, credentials, `.venv`, or `taskflow.db`; these are excluded by `.gitignore`.
4. In the repository description, use: **A FastAPI task manager with SQLAlchemy, validation, a responsive Jinja2 dashboard, and automated tests.**

## API quick reference

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Service health |
| `POST` | `/api/tasks` | Create a task |
| `GET` | `/api/tasks` | List tasks; optional `status`, `priority`, `search` filters |
| `GET` | `/api/tasks/{task_id}` | Get one task |
| `PATCH` | `/api/tasks/{task_id}` | Update supplied fields |
| `DELETE` | `/api/tasks/{task_id}` | Delete a task |

Example JSON for `POST /api/tasks`:

```json
{
  "title": "Prepare portfolio demo",
  "description": "Run the tests and explain the API flow",
  "status": "pending",
  "priority": "high",
  "due_date": "2026-11-01"
}
```

## Project structure

```text
taskflow-api/
├── app/
│   ├── main.py              # API endpoints and dashboard routes
│   ├── database.py          # SQLAlchemy engine and sessions
│   ├── models.py            # Database model
│   ├── schemas.py           # Request/response validation
│   ├── templates/
│   │   └── dashboard.html   # Jinja2 dashboard UI
│   └── static/
│       ├── styles.css       # Responsive design and motion
│       └── app.js           # Modal interactions
├── tests/
│   └── test_api.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Release verification

Run `python -m pytest -v` before pushing. The QA-hardened release expands the test suite to cover required-field null updates, static asset delivery, API docs availability, and dashboard filtering in addition to the original core workflows.

## Verification notes

This release is intended as a first-version fresher portfolio project. The included automated test suite verifies core API and dashboard flows. Before presenting it as production software, add authentication/authorization, database migrations (for example Alembic), CSRF protection for browser forms, rate limiting, structured logging, and deployment-specific security settings. It is not an authenticated multi-user task manager in this version.


## Interface redesign (v1.1.0)

The dashboard now uses a premium, high-contrast visual system inspired by modern product sites: near-black surfaces, acid-lime accents, oversized Space Grotesk typography, restrained motion, responsive task cards, animated progress artwork, and a redesigned task-creation modal. This is an original TaskFlow interface rather than a copy of Pass98. The existing FastAPI routes and task workflows are preserved.

For Windows development, use `--reload-dir app` so Uvicorn watches application code instead of repeatedly reacting to files installed in `.venv`.
