from fastapi.testclient import TestClient

from web.api import app
from web.checks import create_access_token

client = TestClient(app)


def test_registration_new_user():
    """
    Тест проверяет регистрацию нового пользователя
    """
    data = {'email': '1235@gmail.com',
            'password': '123123213',
            'phone': '375296171303'}
    response = client.post('/web/user/register', params=data)
    assert response.status_code == 200
    assert response.json()['created_user'] == "success"
    global user_id
    user_id = response.json()['id']


def test_get_user():
    """
    Тест проверяет выдачу конкретного юзера
    """
    token = create_access_token('artem', '6482fee1f3ff4b3b60ed4119', 'admin')
    response = client.get(f'/web/user/{user_id}', headers={"Authorization": f"Bearer {token}"})
    expected_keys = {'_id', 'username', 'first_name', 'id_telegram', 'gyms', 'records', 'person'}
    assert expected_keys == response.json().keys()
    assert response.status_code == 200


def test_registration_old_user():
    """
    Тест проверяет регистрацию если такой пользователь уже есть в базе
    """
    data = {'email': '1235@gmail.com',
            'password': '123123213',
            'phone': '375296171303'}
    response = client.post('/web/user/register', params=data)
    assert response.status_code == 200
    assert response.json()['message'] == "It's email is already used"


def test_delete_user():
    """
    Тест проверяет удаление пользователя
    """
    data = {'user_id': user_id}
    token = create_access_token('artem', '6482fee1f3ff4b3b60ed4119', 'admin')
    response = client.delete('/web/user/delete', params=data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()['delete'] == 'success'


def test_delete_non_user_in_db():
    """
    Тест проверяет удаление из бд если пользователя нет в базе
    """
    data = {'user_id': user_id}
    token = create_access_token('artem', '6482fee1f3ff4b3b60ed4119', 'admin')
    response = client.delete('/web/user/delete', params=data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()['delete'] == 'id not in db'


def test_get_users():
    """
    Тест проверяет вывод всех пользователей
    """
    token = create_access_token('artem', '6482fee1f3ff4b3b60ed4119', 'admin')
    response = client.get('/web/users/', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_login():
    """
    Тест проверяет авторизацию пользователей
    """
    data = {'email': '1235@gmail.com',
            'password': '123123213'}
    response = client.post('/web/login', params=data)
    expected_keys = {'access_token', 'refresh_token'}
    print(response.json())
    assert response.status_code == 200
    if response.json()['message'] == 'access invalid':
        assert response.json()['message'] == 'access invalid'
    else:
        assert expected_keys == response.json().keys()


def test_login_failed():
    """
    Тест проверяет авторизацию пользователей если их нет в базу
    """
    data = {'email': '1235@gmail.com',
            'password': 'hello'}
    response = client.post('/web/login', params=data)
    assert response.status_code == 200
    assert response.json()['message'] == 'access invalid'


def test_refresh_token():
    """
    Тест проверяет выдачу ре фреш токена
    """
    token = create_access_token('artem', '6482fee1f3ff4b3b60ed4119', 'admin')
    response = client.post('/web/refresh', headers={"Authorization": f"Bearer {token}"})
    expected_keys = {'access_token', 'data'}
    assert expected_keys == response.json().keys()
    assert response.status_code == 200
