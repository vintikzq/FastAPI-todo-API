from datetime import datetime, timedelta, timezone
from config import settings
from passlib.context import CryptContext
from jose import jwt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password) -> str:
    return pwd_context.hash(password)


def verify_password(password, hashed_password) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(payload: dict):
    data = payload.copy()
    exp_time = datetime.now(timezone.utc) + \
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
    data['exp'] = exp_time
    token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token
