"""edit table tracking

Revision ID: b5e9840b1e32
Revises: 7cb148349d7b
Create Date: 2025-12-02 02:28:10.828703

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b5e9840b1e32'
down_revision: Union[str, Sequence[str], None] = '7cb148349d7b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('tracking', sa.Column('execution_time', postgresql.TIMESTAMP(timezone=True), nullable=False))
    op.drop_column('tracking', 'alert_time')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('tracking', sa.Column('alert_time', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False))
    op.drop_column('tracking', 'execution_time')
