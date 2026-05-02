from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status
from app.enums import TodoStatus
from app.repository import tasks as tasks_repository
from app.models import User
from app.schemas import TaskRequest, TaskResponse


def create_task(db: Session, current_user: User, task_data: TaskRequest) -> TaskResponse:
    task = tasks_repository.create_task(
        db, current_user.id, task_data)
    db.commit()
    return TaskResponse.model_validate(task)


def get_all_tasks(db: Session, current_user: User, status: TodoStatus | None, sort_by_creation_date: bool, limit: int, offset: int) -> list[TaskResponse]:
    """Retrieve and validate a list of tasks for the current user.

    Args:
        db (Session): Database session.
        current_user (User): The authenticated user object.
        status (TodoStatus | None): Optional status filter.
        sort_by_creation_date (bool): Flag to enable date sorting.
        limit (int): Pagination limit.
        offset (int): Pagination offset.

    Returns:
        list[TaskResponse]: Validated list of tasks ready for API response.
    """
    tasks = tasks_repository.get_all_tasks(
        db, current_user.id, sort_by_creation_date, status, limit, offset)
    return [TaskResponse.model_validate(task) for task in tasks]
