from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependency import get_current_user, get_db
from app.models import User
from app.schemas import TaskRequest, TaskResponse
from app.service import tasks as tasks_service

router = APIRouter()


@router.post('/task', response_model=TaskResponse, summary="Create new task ")
def create_task(payload: TaskRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return tasks_service.create_task(db, current_user, payload)
