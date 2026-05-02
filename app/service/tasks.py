from sqlalchemy.orm import Session
from app.repository import tasks as tasks_repository
from app.models import User
from app.schemas import TaskRequest, TaskResponse


def create_task(db: Session, current_user: User, task_data: TaskRequest):
    task = tasks_repository.create_task(
        db, current_user.id, task_data)
    db.commit()
    return TaskResponse.model_validate(task)
