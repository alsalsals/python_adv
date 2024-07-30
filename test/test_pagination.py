import math
from http import HTTPStatus
import pytest
import requests


@pytest.mark.parametrize('page, size', [(1, 4), (2, 5)])
def test_users_pagination(app_url, users, page, size):
    response = requests.get(f'{app_url}/api/users?page={page}&size={size}')
    assert response.status_code == HTTPStatus.OK
    assert response.json()['size'] == size
    assert response.json()['page'] == page
    assert response.json()['pages'] == math.ceil(len(users)/size)
    assert response.json()['total'] == len(users)


@pytest.mark.parametrize('size', [4, 100])
def test_users_size_with_pagination(app_url, size):
    response = requests.get(f'{app_url}/api/users?page=1&size={size}')
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['items']) == size


@pytest.mark.parametrize('page, size', [(10000, 40), (20, 100)])
def test_users_pagination_high_page_and_size(app_url, users, page, size):
    response = requests.get(f'{app_url}/api/users?page={page}&size={size}')
    assert response.status_code == HTTPStatus.OK
    assert response.json()['size'] == size
    assert response.json()['page'] == page
    assert response.json()['pages'] == math.ceil(len(users)/size)
    assert response.json()['total'] == len(users)
    assert response.json()['items'] == []


@pytest.mark.parametrize(
    'page, size',
    [(0, 4), (4, 0), (-1, 4), (4, -1), ('asd', 1), (1, 'asd'), (1, 200)]
)
def test_users_pagination_with_invalid_data(app_url, page, size):
    response = requests.get(f'{app_url}/api/users?page={page}&size={size}')
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize('size', [100,])
def test_users_response_size(app_url, users, size):
    response = requests.get(f'{app_url}/api/users?page=1&size={size}')
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['items']) == len(users)


def test_users_different_pages(app_url):
    response_first = requests.get(f'{app_url}/api/users?page=1&size=1')
    response_second = requests.get(f'{app_url}/api/users?page=2&size=1')
    assert response_first.status_code == HTTPStatus.OK
    assert response_first.json()['items'] != response_second.json()['items']
