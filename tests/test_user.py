from http import HTTPStatus
import pytest
import requests
from app.models.User import User
from app.utils import random_test_data
from tests.conftest import fill_test_data


def test_users(app_url, users):
    for user in users:
        User.model_validate(user)


@pytest.mark.usefixtures('fill_test_data')
def test_users_no_duplicates(users):
    users_ids = [user['id'] for user in users]
    assert len(users_ids) == len(set(users_ids))
    assert len(users_ids) != 0


def test_user(app_url, fill_test_data):
    for user_id in (fill_test_data[0], fill_test_data[-1]):
        response = requests.get(f'{app_url}/api/user/{user_id}')
        assert response.status_code == HTTPStatus.OK
        user = response.json()
        User.model_validate(user)


@pytest.mark.parametrize("user_id", [16, ])
def test_user_non_existent_value(app_url, user_id):
    response = requests.get(f"{app_url}/api/user/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User is not found'}


@pytest.mark.parametrize('user_id', [-1, 0])
def test_user_invalid_value(app_url, user_id):
    response = requests.get(f'{app_url}/api/user/{user_id}')
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_user_after_delete(app_url, deleted_user):
    response = requests.get(f'{app_url}/api/user/{deleted_user['id']}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User is not found'}


def test_get_user_after_create(app_url, created_user):
    response = requests.get(f'{app_url}/api/user/{created_user['id']}')
    user = response.json()

    assert response.status_code == HTTPStatus.OK
    assert user['email'] == created_user['email']
    assert user['first_name'] == created_user['first_name']
    assert user['last_name'] == created_user['last_name']
    assert user['avatar'] == created_user['avatar']

    User.model_validate(user)


def test_delete_non_existent_user(app_url, deleted_user):
    response = requests.delete(f'{app_url}/api/user/{deleted_user['id']}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User is not found'}


def test_patch_non_existent_user(app_url, deleted_user):
    new_user_data = random_test_data.user()
    response = requests.patch(f'{app_url}/api/user/{deleted_user['id']}', json=new_user_data)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User is not found'}


@pytest.mark.parametrize('user_id', [-1, 0])
def test_delete_invalid_id(app_url, user_id):
    response = requests.delete(f'{app_url}/api/user/{user_id}')

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {'detail': 'Invalid user id'}


@pytest.mark.parametrize('user_id', [-1, 0])
def test_patch_invalid_id(app_url, user_id):
    new_user_data = random_test_data.user()
    response = requests.patch(f'{app_url}/api/user/{user_id}', json=new_user_data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {'detail': 'Invalid user id'}
