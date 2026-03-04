"""add content column to post table

Revision ID: cf0843b33b7d
Revises: 9a925c3c16d5
Create Date: 2026-03-03 17:28:56.504091

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf0843b33b7d'
down_revision: Union[str, Sequence[str], None] = '9a925c3c16d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))   
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
