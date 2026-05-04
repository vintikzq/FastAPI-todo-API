def test_register_should_return_200_and_user_login(test_client, first_user_data):

    response = test_client.post("/api/v1/register", json=first_user_data)

    assert response.status_code == 200
    assert response.json()['login'] == 'test_user'


def test_register_should_return_400_when_user_with_same_login_exist(test_client, first_user_data):

    test_client.post("/api/v1/register", json=first_user_data)
    response = test_client.post("/api/v1/register", json=first_user_data)
    assert response.status_code == 400


def test_login_should_return_200_and_token_type(test_client, first_user_data):

    test_client.post("/api/v1/register", json=first_user_data)

    response = test_client.post(
        "/api/v1/login", data={'username': first_user_data.get('login'), 'password': first_user_data.get('password')})

    assert response.status_code == 200
    assert response.json()['token_type'] == 'bearer'


def test_login_should_return_401_when_password_is_wrong(test_client, first_user_data):
    test_client.post("/api/v1/register", json=first_user_data)

    response = test_client.post(
        "/api/v1/login", data={'username': first_user_data.get('login'), 'password': '12341234'})

    assert response.status_code == 401
    assert response.json() == {'detail': "Incorrect login or password"}


def test_login_should_return_401_when_login_is_wrong(test_client, first_user_data):
    test_client.post("/api/v1/register", json=first_user_data)

    response = test_client.post(
        "/api/v1/login", data={'username': 'some_login', 'password': first_user_data.get('password')})

    assert response.status_code == 401
    assert response.json() == {'detail': "Incorrect login or password"}
