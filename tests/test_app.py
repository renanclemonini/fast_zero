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


def test_update_user_not_authorized(client):
    # Criando dois usuários (usuário atual e o usuário a ser atualizado)
    user1 = {
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'secret',
    }
    user2 = {
        'username': 'bob',
        'email': 'bob@example.com',
        'password': 'secret',
    }

    # Criar o primeiro usuário (alice)
    response1 = client.post('/users/', json=user1)
    assert response1.status_code == HTTPStatus.CREATED

    # Criar o segundo usuário (bob)
    response2 = client.post('/users/', json=user2)
    assert response2.status_code == HTTPStatus.CREATED

    # Gerar o token para o usuário alice
    token_response = client.post(
        '/token',
        data={
            'username': user1['username'],
            'password': user1['password'],
        },
    )
    access_token = token_response.json().get('access_token')

    # Headers de autorização para alice
    headers = {'Authorization': f'Bearer {access_token}'}

    # Tentar atualizar o usuário bob (id diferente de alice)
    update_data = {
        'username': 'bob_updated',
        'email': 'bob_updated@example.com',
        'password': 'new_secret',
    }
    response = client.put('/users/2', headers=headers, json=update_data)

    # Verificar se a resposta foi "Not enough permission"
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Not enough permission'}


def test_delete_user(client, token):
    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_authorized(client):
    # Criando dois usuários (usuário atual e usuário a ser deletado)
    user1 = {
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'secret',
    }
    user2 = {
        'username': 'bob',
        'email': 'bob@example.com',
        'password': 'secret',
    }

    # Criar o primeiro usuário (alice)
    response1 = client.post('/users/', json=user1)
    assert response1.status_code == HTTPStatus.CREATED

    # Criar o segundo usuário (bob)
    response2 = client.post('/users/', json=user2)
    assert response2.status_code == HTTPStatus.CREATED

    # Gerar o token para o usuário alice
    token_response = client.post(
        '/token',
        data={
            'username': user1['username'],
            'password': user1['password'],
        },
    )
    access_token = token_response.json().get('access_token')

    # Headers de autorização para alice
    headers = {'Authorization': f'Bearer {access_token}'}

    # Tentar deletar o usuário bob (id diferente de alice)
    response = client.delete('/users/2', headers=headers)

    # Verificar se a resposta foi "Unauthorized" (403)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
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
