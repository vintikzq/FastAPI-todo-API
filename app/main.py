from fastapi import FastAPI
from app.api.v1.users import router as users_router
from app.api.v1.tasks import router as tasks_router
from app.database import Base
from .database import engine
app = FastAPI()

app.include_router(users_router, prefix="/api/v1", tags=['users'])
app.include_router(tasks_router, prefix="/api/v1", tags=['tasks'])

Base.metadata.create_all(bind=engine)
