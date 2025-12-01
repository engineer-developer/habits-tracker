"""remove field is_active, add field completed

Revision ID: 4237cc29a494
Revises: 9f7a18d598c9
Create Date: 2025-12-01 20:51:41.099682

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4237cc29a494'
down_revision: Union[str, Sequence[str], None] = '9f7a18d598c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('habits', sa.Column('completed', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    op.drop_column('habits', 'is_active')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('habits', sa.Column('is_active', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=False))
    op.drop_column('habits', 'completed')
