from contextlib import asynccontextmanager
from datetime import date
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, Form, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Task
from .schemas import TaskCreate, TaskRead, TaskUpdate

BASE_DIR = Path(__file__).resolve().parent

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="TaskFlow API",
    description="A task management REST API with a lightweight web dashboard.",
    version="1.1.0",
    lifespan=lifespan,
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")
DbSession = Annotated[Session, Depends(get_db)]

@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok", "service": "TaskFlow API"}

@app.post("/api/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate, db: DbSession):
    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@app.get("/api/tasks", response_model=list[TaskRead], tags=["tasks"])
def list_tasks(
    db: DbSession,
    task_status: Annotated[str | None, Query(alias="status", pattern="^(pending|in_progress|completed)$")] = None,
    priority: Annotated[str | None, Query(pattern="^(low|medium|high)$")] = None,
    search: Annotated[str | None, Query(max_length=120)] = None,
):
    statement = select(Task)
    if task_status:
        statement = statement.where(Task.status == task_status)
    if priority:
        statement = statement.where(Task.priority == priority)
    if search:
        statement = statement.where(Task.title.ilike(f"%{search.strip()}%"))
    return list(db.scalars(statement.order_by(Task.id.desc())).all())

@app.get("/api/tasks/{task_id}", response_model=TaskRead, tags=["tasks"])
def get_task(task_id: int, db: DbSession):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/api/tasks/{task_id}", response_model=TaskRead, tags=["tasks"])
def update_task(task_id: int, payload: TaskUpdate, db: DbSession):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: int, db: DbSession):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return None

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def dashboard(request: Request, db: DbSession, status_filter: str = "all", search: str = ""):
    statement = select(Task)
    if status_filter in {"pending", "in_progress", "completed"}:
        statement = statement.where(Task.status == status_filter)
    if search.strip():
        statement = statement.where(Task.title.ilike(f"%{search.strip()}%"))
    tasks = list(db.scalars(statement.order_by(Task.id.desc())).all())
    total = db.scalar(select(func.count()).select_from(Task)) or 0
    completed = db.scalar(select(func.count()).select_from(Task).where(Task.status == "completed")) or 0
    active = db.scalar(select(func.count()).select_from(Task).where(Task.status == "in_progress")) or 0
    pending = db.scalar(select(func.count()).select_from(Task).where(Task.status == "pending")) or 0
    return templates.TemplateResponse(request=request, name="dashboard.html", context={
        "tasks": tasks, "total": total, "completed": completed, "active": active,
        "pending": pending, "status_filter": status_filter, "search": search,
        "today": date.today().isoformat(),
    })

@app.post("/web/tasks", include_in_schema=False)
def create_task_from_web(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()] = "",
    priority: Annotated[str, Form()] = "medium",
    due_date: Annotated[str, Form()] = "",
    db: Session = Depends(get_db),
):
    try:
        payload = TaskCreate(title=title, description=description.strip() or None, priority=priority,
                             due_date=date.fromisoformat(due_date) if due_date else None)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    db.add(Task(**payload.model_dump()))
    db.commit()
    return RedirectResponse(url="/?created=1", status_code=303)

@app.post("/web/tasks/{task_id}/status", include_in_schema=False)
def change_task_status(task_id: int, task_status: Annotated[str, Form()], db: Session = Depends(get_db)):
    if task_status not in {"pending", "in_progress", "completed"}:
        raise HTTPException(status_code=422, detail="Invalid status")
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = task_status
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.post("/web/tasks/{task_id}/delete", include_in_schema=False)
def delete_task_from_web(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return RedirectResponse(url="/", status_code=303)
