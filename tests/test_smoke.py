from http import HTTPStatus
import pytest
import requests

from app.models.User import UserCreate, User, UserUpdate
from app.utils import random_test_data
from tests.conftest import created_user


@pytest.mark.smoke
def test_server_ping(app_url):
    response = requests.get(f'{app_url}/ping')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "pong"}


@pytest.mark.smoke
def test_server_status(app_url):
    response = requests.get(app_url)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Service is running"}


@pytest.mark.smoke
def test_db_status(app_url):
    response = requests.get(f'{app_url}/status')
    assert response.status_code == HTTPStatus.OK
    assert response.json()


@pytest.mark.smoke
def test_create_user(app_url):
    user_data = random_test_data.user()
    response = requests.post(f'{app_url}/api/user/', json=user_data)

    assert response.status_code == HTTPStatus.CREATED
    user_created = response.json()

    assert user_created['email'] == user_data['email']
    assert user_created['first_name'] == user_data['first_name']
    assert user_created['last_name'] == user_data['last_name']
    assert user_created['avatar'] == user_data['avatar']
    UserCreate.model_validate(user_created)
    User.model_validate(user_created)


@pytest.mark.smoke
def test_delete_user(app_url, created_user):
    user_id = created_user['id']
    response = requests.delete(f'{app_url}/api/user/{user_id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


@pytest.mark.smoke
def test_patch_user(app_url, created_user):
    new_user_data = random_test_data.user()
    response = requests.patch(
        f'{app_url}/api/user/{created_user["id"]}', json=new_user_data
    )

    updated_user = response.json()

    assert response.status_code == HTTPStatus.OK
    assert updated_user['email'] == new_user_data['email']
    assert updated_user['first_name'] == new_user_data['first_name']
    assert updated_user['last_name'] == new_user_data['last_name']
    assert updated_user['avatar'] == new_user_data['avatar']

    assert created_user['email'] != new_user_data['email']
    assert created_user['first_name'] != new_user_data['first_name']
    assert created_user['last_name'] != new_user_data['last_name']
    assert created_user['avatar'] != new_user_data['avatar']

    UserUpdate.model_validate(updated_user)
    User.model_validate(updated_user)
