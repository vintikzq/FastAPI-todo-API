from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.enums import TodoPriority, TodoStatus


class UserRequest(BaseModel):
    login: str = Field(..., min_length=3, max_length=127)
    password: str = Field(..., min_length=8, max_length=20)

    @field_validator('login')
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("User name cannot be empty")
        return v


class UserResponse(BaseModel):
    id: int
    login: str

    model_config = ConfigDict(from_attributes=True)


class TaskRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=127)
    status: TodoStatus = TodoStatus.PENDING
    priority: TodoPriority = TodoPriority.LOW
    due_date: datetime | None = None
    description: str | None = Field(None, max_length=1024)


class TaskResponse(BaseModel):
    id: int
    name: str
    status: TodoStatus
    priority: TodoPriority
    description: str | None
    due_date: datetime | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
