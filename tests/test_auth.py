from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_get_token_with_erro(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': user.password},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
