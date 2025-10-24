"""add table habits

Revision ID: 6c68dba6787c
Revises: 394f1a8cdbf1
Create Date: 2025-10-24 23:18:43.560366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c68dba6787c'
down_revision: Union[str, Sequence[str], None] = '394f1a8cdbf1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('habits',
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(), server_default='', nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_habits_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_habits'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('habits')
