# Todo API

Simple REST API for managing personal tasks built with FastAPI.

## Features

- User registration and authentication (JWT)
- Create, read, update and delete tasks (CRUD)
- Filter and sort tasks
- Priority and status management
- Secure password hashing with bcrypt

## Tech Stack

- **FastAPI** - web framework
- **SQLAlchemy 2.0** - ORM
- **SQLite** - database
- **JWT** - authentication
- **Pydantic v2** - data validation
- **bcrypt** - password hashing

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd FastAPI-todo-API
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the application:
```bash
uvicorn app.main:app --reload
```

API will be available at http://127.0.0.1:8000

Documentation (Swagger): http://127.0.0.1:8000/docs

## API Endpoints

### Auth

- POST /api/v1/register - Register new user
- POST /api/v1/login - Login user (returns JWT token)

### Tasks

- POST /api/v1/tasks - Create new task
- GET /api/v1/tasks - Get all tasks (with filters)
- PATCH /api/v1/tasks/{task_id} - Update task
- DELETE /api/v1/tasks/{task_id} - Delete task

> **Task endpoints require** `Authorization: Bearer <your-jwt-token>` header.

## Project Structure

app/
├── api/
│   └── v1/
│       ├── users.py
│       └── tasks.py
├── repository/
│       ├── users.py
│       └── tasks.py
├── service/
│       ├── users.py
│       └── tasks.py
├── auth.py
├── config.py
├── database.py
├── dependency.py
├── enums.py
├── main.py
├── models.py
└── schemas.py

## Future Improvements

- Move to PostgreSQL + Docker
- Alembic migrations
- Write tests (pytest)
