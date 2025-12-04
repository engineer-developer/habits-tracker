"""add table tracking

Revision ID: 7cb148349d7b
Revises: 459cbb6a2e4f
Create Date: 2025-12-01 23:49:48.058993

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7cb148349d7b'
down_revision: Union[str, Sequence[str], None] = '459cbb6a2e4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('tracking',
    sa.Column('alert_time', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('habit_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['habit_id'], ['habits.id'], name=op.f('fk_tracking_habit_id_habits'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_tracking'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('tracking')
