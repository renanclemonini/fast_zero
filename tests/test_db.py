from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='rclemon',
        email='rclemon@test.com',
        password='minhasenha123',
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    result = session.scalar(
        select(User).where(User.email == 'rclemon@test.com')
    )

    assert result.username == 'rclemon'
