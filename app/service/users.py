from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repository import users as users_repository
from app.schemas import UserResponse
from app.auth import hash_password


def create_user(db: Session, login: str, password: str) -> UserResponse:
    if users_repository.get_user_by_login(db, login) is not None:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )
    hashed_password = hash_password(password)
    user = users_repository.create_user(db, login, hashed_password)
    db.commit()
    return UserResponse.model_validate(user)
