from http import HTTPStatus
import pytest
import requests


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
def test_open_base_url(app_url):
    response = requests.get(app_url)
    assert response.status_code == HTTPStatus.OK
