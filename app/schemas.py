from datetime import date, datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

TaskStatus = Literal["pending", "in_progress", "completed"]
TaskPriority = Literal["low", "medium", "high"]

class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    status: TaskStatus = "pending"
    priority: TaskPriority = "medium"
    due_date: date | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Title cannot be blank.")
        return value

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: date | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()
            if not value:
                raise ValueError("Title cannot be blank.")
        return value

    @model_validator(mode="after")
    def non_nullable_fields_cannot_be_null(self):
        # Omitted fields are allowed in PATCH; explicitly nulling required DB columns is not.
        for field_name in ("title", "status", "priority"):
            if field_name in self.model_fields_set and getattr(self, field_name) is None:
                raise ValueError(f"{field_name} cannot be null.")
        return self

class TaskRead(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
