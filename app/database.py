"""Database setup. SQLite works out of the box; set DATABASE_URL for PostgreSQL."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Load project-level .env without overriding environment variables set by the host.
load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=False)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./taskflow.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
