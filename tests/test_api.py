from http import HTTPStatus

import requests


def test_user_method_not_allowed_error(app_url):
    response = requests.head(f'{app_url}/api/users/')
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
