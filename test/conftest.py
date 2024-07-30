import os
from http import HTTPStatus

import dotenv
import pytest
import requests


@pytest.fixture(autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture()
def app_url():
    return os.getenv('APP_URL')


@pytest.fixture()
def users(app_url):
    response = requests.get(f'{app_url}/api/users/all')
    assert response.status_code == HTTPStatus.OK
    return response.json()
