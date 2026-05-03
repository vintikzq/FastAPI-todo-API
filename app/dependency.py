from typing import Generator

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.database import SessionLocal
from app.models import User
from app.repository.users import get_user_by_id


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(credentials: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Validate the JWT token and return the current user.

    Args:
        credentials (str, optional): JWT access token from Authorization header. Defaults to Depends(oauth2_scheme).
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If token is invalid, expired, or the user does not exist.

    Returns:
        User: The authenticated User model instance.
    """
    try:
        token = jwt.decode(credentials, settings.SECRET_KEY,
                           [settings.ALGORITHM])
        user_id_str: str | None = token.get('sub')
        if user_id_str is None:
            raise HTTPException(
                status_code=401,
                detail="User is not authorized"
            )
        user_id = int(user_id_str)
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Token is invalid"
        )

    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User is not authorized"
        )
    return user
