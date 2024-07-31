import json
import os
from http import HTTPStatus

import dotenv
import pytest
import requests

from app.utils import random_test_data, path


@pytest.fixture(scope='session', autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope='session')
def app_url():
    return os.getenv('APP_URL')


@pytest.fixture()
def users(app_url):
    response = requests.get(f'{app_url}/api/users/all')
    assert response.status_code == HTTPStatus.OK
    return response.json()


@pytest.fixture(scope="module")
def fill_test_data(app_url):
    import os
    print(os.getcwd())
    with open(path.current_dir('users.json')) as f:
        test_data_users = json.load(f)
    api_users = []
    for user in test_data_users:
        response = requests.post(f"{app_url}/api/user", json=user)
        api_users.append(response.json())

    print(api_users)
    user_ids = [user["id"] for user in api_users]
    print(user_ids)

    yield user_ids

    for user_id in user_ids:
        requests.delete(f"{app_url}/api/user/{user_id}")


@pytest.fixture()
def created_user(app_url):
    user_test_data = random_test_data.user()
    response = requests.post(f'{app_url}/api/user/', json=user_test_data)
    assert response.status_code == HTTPStatus.CREATED
    return response.json()


@pytest.fixture()
def deleted_user(app_url, created_user):
    user_id = created_user['id']
    response = requests.delete(f'{app_url}/api/user/{user_id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}
    return created_user
