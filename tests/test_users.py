from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_users(client, user):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'teste_123',
                'email': 'teste@example.com',
            },
        ],
    }


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_update_user(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'teste_123',
            'email': 'teste@example.com',
            'password': '1234batatinhas',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_update_wrong_user(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.put(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'teste_123',
            'email': 'teste@example.com',
            'password': '1234batatinhas',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() != user_schema


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_wrong_user(client, user, token):
    response = client.delete(
        f'/users/{user.id + 1}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}


def test_read_user_should_return_not_found(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_create_user_should_return_username_invalid(client, user):
    client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice2@example.com',
            'password': 'secret',
        },
    )
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice2@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_user_should_return_email_invalid(client, user):
    client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice2@example.com',
            'password': 'secret',
        },
    )
    response = client.post(
        '/users/',
        json={
            'username': 'alice321',
            'email': 'alice2@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username or email already exists'}
