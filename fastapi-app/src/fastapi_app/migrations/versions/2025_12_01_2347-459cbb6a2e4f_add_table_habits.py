"""add table habits

Revision ID: 459cbb6a2e4f
Revises: fc03593d8071
Create Date: 2025-12-01 23:47:00.981520

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '459cbb6a2e4f'
down_revision: Union[str, Sequence[str], None] = 'fc03593d8071'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('habits',
    sa.Column('title', sa.String(length=250), nullable=False),
    sa.Column('description', sa.String(), server_default='', nullable=False),
    sa.Column('remind_time', sa.Time(), nullable=False),
    sa.Column('remind_quantity', sa.Integer(), nullable=False),
    sa.Column('completed', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_habits_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_habits'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('habits')
