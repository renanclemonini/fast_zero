"""gerando metadata updated at

Revision ID: 0bb6590a41f6
Revises: 978f56d0c97f
Create Date: 2025-02-08 21:20:36.712268

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0bb6590a41f6'
down_revision: Union[str, None] = '978f56d0c97f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('update_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'update_at')
    # ### end Alembic commands ###
