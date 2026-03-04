"""add foreign key to post table

Revision ID: 436687d1c03a
Revises: 1be223974db2
Create Date: 2026-03-03 20:02:59.090087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '436687d1c03a'
down_revision: Union[str, Sequence[str], None] = '1be223974db2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', 'posts', 'users', ['owner_id'], ['id'], ondelete='CASCADE')    

    pass


def downgrade() -> None:
    op.drop_column('posts', 'owner_id')
    """Downgrade schema."""
    pass
