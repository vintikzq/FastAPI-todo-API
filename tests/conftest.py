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
    engine = create_engine("sqlite:///./test.db", connect_args={
        "check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='function')
def test_session(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def test_client(test_session):
    def override_get_db():
        yield test_session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture()
def user_data():
    return {'login': 'test_user', 'password': '12345678'}


@pytest.fixture()
def auth_headers(test_client, user_data):
    test_client.post("/api/v1/register", json=user_data)
    response = test_client.post(
        "/api/v1/login", data={'username': user_data.get('login'), 'password': user_data.get('password')})
    token = response.json().get('access_token')
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def test_task(test_client, auth_headers):
    response = test_client.post("/api/v1/tasks", headers=auth_headers,
                                json={'name': 'do smth', 'description': 'tomorrow'})

    assert response.status_code == 201
    return response.json()
