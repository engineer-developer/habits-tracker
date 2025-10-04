"""add table users

Revision ID: be78f310ef4b
Revises: e22f5bdf0639
Create Date: 2025-10-04 00:21:58.895178

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be78f310ef4b'
down_revision: Union[str, Sequence[str], None] = 'e22f5bdf0639'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('telegram_id', sa.BigInteger(), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('telegram_id', name=op.f('uq_users_telegram_id_'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
