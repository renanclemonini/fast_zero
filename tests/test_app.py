from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_read_root_deve_retornar_ok_e_olar_mundo(client):
    response = client.get('/')  # Act / Ação (faz alguma coisa)

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá mundo!'}


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
                'email': 'teste@example.com',
                'id': 1,
                'username': 'teste_123',
            },
        ],
    }


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_update_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.put(
        '/users/1',
        json={
            'username': 'teste_123',
            'email': 'teste@example.com',
            'password': '1234batatinhas',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_update_user_should_return_not_found(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user_with_username_equal(client):
    client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    client.post(
        '/users/',
        json={
            'username': 'alice_teste1',
            'email': 'alice1@example.com',
            'password': 'secret',
        },
    )
    response = client.put(
        '/users/1',
        json={
            'username': 'alice_teste1',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_update_user_with_email_equal(client):
    client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    client.post(
        '/users/',
        json={
            'username': 'alice_teste1',
            'email': 'alice1@example.com',
            'password': 'secret',
        },
    )
    response = client.put(
        '/users/1',
        json={
            'username': 'alice',
            'email': 'alice1@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_delete_user_should_return_not_found(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND


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
