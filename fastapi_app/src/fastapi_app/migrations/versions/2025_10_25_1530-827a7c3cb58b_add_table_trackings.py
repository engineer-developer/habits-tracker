"""add table trackings

Revision ID: 827a7c3cb58b
Revises: 6c68dba6787c
Create Date: 2025-10-25 15:30:21.040604

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '827a7c3cb58b'
down_revision: Union[str, Sequence[str], None] = '6c68dba6787c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('trackings',
    sa.Column('remind_count', sa.Integer(), nullable=False, comment='Количество напоминаний'),
    sa.Column('remind_time', sa.Time(), nullable=False, comment='Время напоминания'),
    sa.Column('chat_id', sa.Integer(), nullable=False, comment='ID чата'),
    sa.Column('job_id', sa.String(), nullable=False, comment='ID запланированной задачи'),
    sa.Column('habit_id', sa.Integer(), nullable=False, comment='ID привычки'),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.CheckConstraint('remind_count >= 0', name=op.f('ck_trackings_cnt_positive_remind_count')),
    sa.ForeignKeyConstraint(['habit_id'], ['habits.id'], name=op.f('fk_trackings_habit_id_habits'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_trackings'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('trackings')
