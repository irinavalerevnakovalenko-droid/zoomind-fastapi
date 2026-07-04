"""add order user status index

Revision ID: 217b6ec3b113
Revises: 54c503e094ce
Create Date: 2026-07-04 16:24:07.971376

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '217b6ec3b113'
down_revision: Union[str, Sequence[str], None] = '54c503e094ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        'ix_order_user_status',
        'orders',
        ['user_id', 'status'],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index('ix_order_user_status', table_name='orders')
