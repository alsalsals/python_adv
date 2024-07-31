from http import HTTPStatus
import pytest
import requests
from models.User import User


def test_users(app_url):
    response = requests.get(f'{app_url}/api/users/all')
    assert response.status_code == HTTPStatus.OK

    users = response.json()
    for user in users:
        User.model_validate(user)


def test_users_no_duplicates(users):
    users_ids = [user['id'] for user in users]
    assert len(users_ids) == len(set(users_ids))


@pytest.mark.parametrize("user_id", [1, 6, 12])
def test_user(app_url, user_id):
    response = requests.get(f'{app_url}/api/user/{user_id}')
    assert response.status_code == HTTPStatus.OK

    users = response.json()
    User.model_validate(users)


@pytest.mark.parametrize("user_id", [16,])
def test_user_non_existent_value(app_url, user_id):
    response = requests.get(f"{app_url}/api/user/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0])
def test_user_invalid_value(app_url, user_id):
    response = requests.get(f"{app_url}/api/user/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
