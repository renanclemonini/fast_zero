from datetime import datetime

from pytz import timezone
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


def get_sao_paulo_time():
    sao_paulo_tz = timezone('America/Sao_Paulo')
    return datetime.now(sao_paulo_tz)


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, default=get_sao_paulo_time
    )
    update_at: Mapped[datetime] = mapped_column(
        init=False, default=get_sao_paulo_time, onupdate=get_sao_paulo_time
    )
