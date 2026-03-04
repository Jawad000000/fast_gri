"""add last few columns to post table

Revision ID: dd34a463853c
Revises: 436687d1c03a
Create Date: 2026-03-03 20:08:51.396409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd34a463853c'
down_revision: Union[str, Sequence[str], None] = '436687d1c03a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default=sa.text('true')))
    op.add_column('posts', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
