from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.service import users as users_service
from app.dependency import get_db
from app.schemas import TokenResponse, UserRequest, UserResponse

router = APIRouter()


@router.post('/register', response_model=UserResponse)
def create_user(payload: UserRequest, db: Session = Depends(get_db)):
    return users_service.create_user(db, payload.login, payload.password)


@router.post('/login', response_model=TokenResponse)
def login_user(payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return users_service.authenticate_user(db, payload.username, payload.password)
