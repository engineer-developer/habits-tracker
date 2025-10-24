"""add table habits

Revision ID: 40375ca12763
Revises: 394f1a8cdbf1
Create Date: 2025-10-24 03:45:32.573390

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40375ca12763'
down_revision: Union[str, Sequence[str], None] = '394f1a8cdbf1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('habits',
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(), server_default='', nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_habits')),
    sa.UniqueConstraint('name', name=op.f('uq_habits_name_'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('habits')
