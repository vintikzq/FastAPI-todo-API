def test_create_task_success(test_client, auth_headers):
    response = test_client.post("/api/v1/tasks", headers=auth_headers,
                                json={'name': 'do smth', 'description': 'tomorrow'})
    assert response.status_code == 201
    assert response.json().get('id') is not None
    assert response.json().get('name') == 'do smth'


def test_create_task_unauthorized(test_client):
    response = test_client.post("/api/v1/tasks",
                                json={'name': 'unauthorized task'})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_all_tasks_success(test_client, auth_headers, test_task):

    response = test_client.get("/api/v1/tasks", headers=auth_headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]['name'] == 'do smth'


def test_get_all_tasks_unauthorized(test_client):
    response = test_client.get("/api/v1/tasks")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_delete_task_success(test_client, auth_headers, test_task):
    task_id = test_task['id']

    response = test_client.delete(
        f"/api/v1/tasks/{task_id}", headers=auth_headers)

    assert response.status_code == 204


def test_delete_task_unauthorized(test_client):
    response = test_client.delete(
        "/api/v1/tasks/1")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_patch_task_success(test_client, auth_headers, test_task):
    task_id = test_task['id']

    response = test_client.patch(
        f"/api/v1/tasks/{task_id}", headers=auth_headers, json={'name': 'nothing'})

    assert response.status_code == 200
    # new name - nothing, description - tommorow when task create
    assert response.json()['name'] == 'nothing'
    assert response.json()['description'] == 'tomorrow'


def test_patch_task_unauthorized(test_client):
    response = test_client.patch(
        "/api/v1/tasks/1", json={'name': 'nothing'})

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
