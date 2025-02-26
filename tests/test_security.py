from http import HTTPStatus

from jwt import decode

from fast_zero.security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
)


def test_jwt():
    data = {
        'sub': 'test@test.com',
    }
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded['sub'] == data['sub']
    assert decoded['exp']


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.username, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_get_token_with_erro(client, user):
    response = client.post(
        '/token',
        data={'username': user.username, 'password': user.password},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token_invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_current_user_not_found(client):
    data = {'no-username': 'test'}
    token = create_access_token(data)
    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_current_user_does_not_exists(client):
    data = {'sub': 'baleiaazul364'}
    token = create_access_token(data)
    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
