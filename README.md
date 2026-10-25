# TaskFlow — Task Management REST API

TaskFlow is a task management application built with FastAPI, SQLAlchemy, and Python. It provides a REST API and a responsive web dashboard for creating, organizing, searching, filtering, updating, and deleting tasks.

## Features

- Create, view, update, and delete tasks.
- Track task status: `pending`, `in_progress`, or `completed`.
- Set task priority: `low`, `medium`, or `high`.
- Add descriptions and due dates.
- Search tasks by title.
- Filter tasks by status and priority.
- View task summaries and progress through the dashboard.
- Validate requests using Pydantic.
- Access interactive API documentation through Swagger UI.
- Run automated tests for API endpoints and dashboard workflows.
- Use SQLite by default, with configurable PostgreSQL support.

## Dashboard Preview

![TaskFlow dashboard](screenshots/Dashboard.png)

![TaskFlow task management interface](screenshots/Dashboard2.png)

## Technology Stack

- **Language:** Python 3.11+
- **Backend:** FastAPI
- **Database ORM:** SQLAlchemy 2
- **Validation:** Pydantic v2
- **Database:** SQLite / PostgreSQL
- **Templates:** Jinja2
- **Frontend:** HTML, CSS, JavaScript
- **Testing:** Pytest, HTTPX
- **Server:** Uvicorn

## Getting Started

### Prerequisites

- Python 3.11 or newer
- Git
- Visual Studio Code or another code editor

### 1. Clone the repository

```powershell
git clone https://github.com/snehh01/taskflow-api.git
cd taskflow-api
```

### 2. Create a virtual environment

```powershell
py -3.11 -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run the following commands without activating the environment:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --reload-dir app
```

### 3. Install dependencies

With the virtual environment activated, run:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the application

```powershell
python -m uvicorn app.main:app --reload --reload-dir app
```

### 5. Open the application

Once the server starts, open these URLs in your browser:

| Resource | URL |
|---|---|
| Web dashboard | http://127.0.0.1:8000 |
| Swagger API documentation | http://127.0.0.1:8000/docs |
| ReDoc API documentation | http://127.0.0.1:8000/redoc |
| Health check | http://127.0.0.1:8000/health |

The SQLite database file, `taskflow.db`, is created automatically when the application starts. It is excluded from Git.

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Check application health |
| `POST` | `/api/tasks` | Create a task |
| `GET` | `/api/tasks` | Retrieve tasks |
| `GET` | `/api/tasks/{task_id}` | Retrieve a task by ID |
| `PATCH` | `/api/tasks/{task_id}` | Update selected task fields |
| `DELETE` | `/api/tasks/{task_id}` | Delete a task |

### Query Parameters

The task listing endpoint supports optional filters:

- `status` — filter by task status.
- `priority` — filter by priority.
- `search` — search task titles.

Example:

```http
GET /api/tasks?status=pending&priority=high
```

### Example Request

Create a task using `POST /api/tasks`:

```json
{
  "title": "Review API documentation",
  "description": "Review endpoints and validation rules",
  "status": "pending",
  "priority": "high",
  "due_date": "2026-11-01"
}
```

Send the request with the `Content-Type: application/json` header.

## Database Configuration

SQLite is used by default, so no separate database server is required for local development.

To configure PostgreSQL:

1. Create a PostgreSQL database.
2. Copy `.env.example` to `.env`.
3. Set the database connection string in `.env`:

```text
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/taskflow
```

4. Install the PostgreSQL driver:

```powershell
pip install "psycopg[binary]"
```

5. Start the application:

```powershell
python -m uvicorn app.main:app --reload --reload-dir app
```

Replace the example credentials with your own. Keep `.env` and all database credentials out of version control. When deploying, configure `DATABASE_URL` through the hosting environment's settings.

## Running Tests

Run the test suite with:

```powershell
python -m pytest -v
```

The tests use an isolated in-memory SQLite database. They cover:

- Application health checks
- Task creation, retrieval, updates, and deletion
- Search and filtering
- Request validation and invalid inputs
- Missing task responses
- Protection against null values for required fields
- Dashboard routes and static assets
- API documentation availability
- Dashboard task creation, status updates, and deletion

The test database is separate from the application's local database.

## Project Structure

```text
taskflow-api/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── templates/
│   │   └── dashboard.html
│   └── static/
│       ├── styles.css
│       └── app.js
├── screenshots/
│   ├── Dashboard.png
│   └── Dashboard2.png
├── tests/
│   └── test_api.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Implementation Notes

- SQLAlchemy handles database models and database operations.
- Pydantic schemas validate incoming request data.
- FastAPI exposes the REST endpoints and serves the dashboard.
- Jinja2 renders the dashboard templates.
- HTML, CSS, and JavaScript handle the browser interface and interactions.
- Environment variables allow database configuration without hardcoding credentials.

## Current Scope

TaskFlow supports task management through its REST API and browser dashboard. The current implementation does not include user authentication or authorization, database migration tooling, CSRF protection for browser forms, or rate limiting. These features should be considered before deploying the application in a multi-user production environment.

## License

No license has been specified yet. Contact the repository owner for permission before redistributing or reusing this code.
