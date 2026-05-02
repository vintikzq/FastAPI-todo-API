from sqlalchemy.orm import Session
from app.models import Tasks
from app.schemas import TaskRequest


def create_task(db: Session, user_id: int, task_data: TaskRequest):

    task = Tasks(owner_id=user_id, **task_data.model_dump())

    db.add(task)
    db.flush()
    return task
