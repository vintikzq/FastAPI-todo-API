from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repository import users as users_repository
from app.schemas import TokenResponse, UserResponse
from app.auth import create_access_token, hash_password, verify_password


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


def authenticate_user(db: Session, login: str, password: str) -> TokenResponse:
    """Authenticate a user and return a JWT access token.    

    Args:
        db (Session): Database session.
        login (str): User login.
        password (str): User plain-text password.

    Raises:
        HTTPException: If the login or password does not match.

    Returns:
        TokenResponse: Object containing the access token and its type.
    """
    user = users_repository.get_user_by_login(db, login)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect login or password"
        )
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect login or password"
        )
    token = create_access_token({'sub': str(user.id)})
    return TokenResponse(access_token=token)
