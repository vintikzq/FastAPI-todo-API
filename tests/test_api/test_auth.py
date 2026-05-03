def test_register_success(test_client, user_data):

    response = test_client.post("/api/v1/register", json=user_data)

    assert response.status_code == 200
    assert response.json()['login'] == 'test_user'


def test_register_duplicate_user(test_client, user_data):

    test_client.post("/api/v1/register", json=user_data)
    response = test_client.post("/api/v1/register", json=user_data)
    assert response.status_code == 400


def test_login_success(test_client, user_data):

    test_client.post("/api/v1/register", json=user_data)

    response = test_client.post(
        "/api/v1/login", data={'username': user_data.get('login'), 'password': user_data.get('password')})

    assert response.status_code == 200
    assert response.json()['token_type'] == 'bearer'


def test_password_invalid(test_client, user_data):
    test_client.post("/api/v1/register", json=user_data)

    response = test_client.post(
        "/api/v1/login", data={'username': user_data.get('login'), 'password': '12341234'})

    assert response.status_code == 401
    assert response.json() == {'detail': "Incorrect login or password"}


def test_login_invalid(test_client, user_data):
    test_client.post("/api/v1/register", json=user_data)

    response = test_client.post(
        "/api/v1/login", data={'username': 'some_login', 'password': user_data.get('password')})

    assert response.status_code == 401
    assert response.json() == {'detail': "Incorrect login or password"}
