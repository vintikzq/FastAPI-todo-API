import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.dependency import get_db
from app.main import app
from app.database import Base

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False)


@pytest.fixture(scope='session')
def test_engine():
    """
    Creates a test database engine once per test session.
    Creates all tables before tests and drops them after all tests are finished.
    """
    engine = create_engine("sqlite:///./test.db", connect_args={
        "check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='function')
def test_session(test_engine):
    """
    Creates a new database session for each test function.
    Uses transaction + rollback pattern to keep tests isolated.
    """
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def test_client(test_session):
    """
    Creates a TestClient with overridden database dependency.
    Clears dependency overrides after each test.
    """
    def override_get_db():
        yield test_session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture()
def first_user_data():
    """Returns registration data for the first test user."""
    return {'login': 'test_user', 'password': '12345678'}


@pytest.fixture()
def second_user_data():
    """Returns registration data for the second test user (used for ownership tests)."""
    return {'login': 'second_test_user', 'password': '12345678'}


@pytest.fixture()
def base_patch_data():
    return {'name': "Updated task name", 'priority': "medium"}


@pytest.fixture()
def base_task_data():
    return {'name': 'Buy flowers',
            'description': "Don't forget water the flowers",
            'priority': 'high'}


@pytest.fixture()
def auth_headers_first_user(test_client, first_user_data):
    """Creates and returns auth headers for the first test user."""
    test_client.post("/api/v1/register", json=first_user_data)
    response = test_client.post(
        "/api/v1/login", data={'username': first_user_data.get('login'), 'password': first_user_data.get('password')})
    token = response.json().get('access_token')
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def auth_headers_second_user(test_client, second_user_data):
    """Creates and returns auth headers for the second test user."""
    test_client.post("/api/v1/register", json=second_user_data)
    response = test_client.post(
        "/api/v1/login", data={'username': second_user_data.get('login'), 'password': second_user_data.get('password')})
    token = response.json().get('access_token')
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def test_task(test_client, auth_headers_first_user):
    """
    Creates a test task owned by the first user.
    Used in most task-related tests.
    """
    response = test_client.post("/api/v1/tasks", headers=auth_headers_first_user,
                                json={'name': 'do smth', 'description': 'tomorrow'})

    assert response.status_code == 201
    return response.json()
