from typing import Generator

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.database import SessionLocal
from app.models import User
from app.repository.users import get_user_by_id


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(credentials: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        token = jwt.decode(credentials, settings.SECRET_KEY,
                           [settings.ALGORITHM])
        user_id = token.get('sub')
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token is invalid"
        )
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="User is not authorized"
        )
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User is not authorized"
        )
    return user
