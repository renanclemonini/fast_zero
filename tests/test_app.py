from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_olar_mundo(client):
    response = client.get('/')  # Act / Ação (faz alguma coisa)

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá mundo!'}
