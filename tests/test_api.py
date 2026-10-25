from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

TEST_ENGINE = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=TEST_ENGINE, autoflush=False, autocommit=False)

@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=TEST_ENGINE)
    Base.metadata.create_all(bind=TEST_ENGINE)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=TEST_ENGINE)


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_read_task(client):
    response = client.post("/api/tasks", json={
        "title": "  Build portfolio  ", "description": "API and UI", "priority": "high",
        "status": "pending", "due_date": "2026-11-01"
    })
    assert response.status_code == 201
    task = response.json()
    assert task["title"] == "Build portfolio"
    assert task["priority"] == "high"
    assert task["due_date"] == "2026-11-01"
    assert client.get(f"/api/tasks/{task['id']}").json()["title"] == "Build portfolio"


def test_list_filter_search_and_priority(client):
    client.post("/api/tasks", json={"title": "Write README", "priority": "low"})
    client.post("/api/tasks", json={"title": "Build API", "priority": "high", "status": "in_progress"})
    assert len(client.get("/api/tasks").json()) == 2
    assert len(client.get("/api/tasks", params={"status": "in_progress"}).json()) == 1
    assert len(client.get("/api/tasks", params={"priority": "low"}).json()) == 1
    assert client.get("/api/tasks", params={"search": "readme"}).json()[0]["title"] == "Write README"


def test_patch_and_delete_task(client):
    created = client.post("/api/tasks", json={"title": "Review tests"}).json()
    task_id = created["id"]
    updated = client.patch(f"/api/tasks/{task_id}", json={"status": "completed", "title": "Review all tests"})
    assert updated.status_code == 200
    assert updated.json()["status"] == "completed"
    assert updated.json()["title"] == "Review all tests"
    assert client.delete(f"/api/tasks/{task_id}").status_code == 204
    assert client.get(f"/api/tasks/{task_id}").status_code == 404


def test_validation_and_not_found(client):
    assert client.post("/api/tasks", json={"title": "   "}).status_code == 422
    assert client.post("/api/tasks", json={"title": "Valid", "priority": "urgent"}).status_code == 422
    assert client.get("/api/tasks/999").status_code == 404
    assert client.patch("/api/tasks/999", json={"status": "completed"}).status_code == 404
    assert client.delete("/api/tasks/999").status_code == 404


def test_patch_rejects_null_required_fields_without_corrupting_task(client):
    task = client.post("/api/tasks", json={"title": "Keep valid record"}).json()
    for field in ("title", "status", "priority"):
        response = client.patch(f"/api/tasks/{task['id']}", json={field: None})
        assert response.status_code == 422
    saved = client.get(f"/api/tasks/{task['id']}").json()
    assert saved["title"] == "Keep valid record"
    assert saved["status"] == "pending"
    assert saved["priority"] == "medium"


def test_static_assets_and_api_docs_are_available(client):
    css = client.get("/static/styles.css")
    js = client.get("/static/app.js")
    docs = client.get("/docs")
    assert css.status_code == 200 and "--" in css.text
    assert js.status_code == 200 and "openModal" in js.text
    assert docs.status_code == 200 and "Swagger UI" in docs.text


def test_dashboard_search_and_status_filter(client):
    client.post("/api/tasks", json={"title": "Write portfolio README", "status": "pending"})
    client.post("/api/tasks", json={"title": "Ship dashboard", "status": "completed"})
    search = client.get("/", params={"search": "portfolio"})
    assert "Write portfolio README" in search.text
    assert "Ship dashboard" not in search.text
    filtered = client.get("/", params={"status_filter": "completed"})
    assert "Ship dashboard" in filtered.text
    assert "Write portfolio README" not in filtered.text


def test_dashboard_and_web_create(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "TaskFlow" in response.text
    assert "Plan less chaotically." in response.text
    created = client.post("/web/tasks", data={
        "title": "Test dashboard form", "description": "Created from the UI",
        "priority": "medium", "due_date": date(2026, 11, 5).isoformat()
    }, follow_redirects=True)
    assert created.status_code == 200
    assert "Test dashboard form" in created.text


def test_web_status_change_and_delete(client):
    task = client.post("/api/tasks", json={"title": "UI workflow"}).json()
    response = client.post(f"/web/tasks/{task['id']}/status", data={"task_status": "completed"}, follow_redirects=True)
    assert response.status_code == 200
    assert "Completed" in response.text
    deleted = client.post(f"/web/tasks/{task['id']}/delete", follow_redirects=True)
    assert deleted.status_code == 200
    assert "UI workflow" not in deleted.text
