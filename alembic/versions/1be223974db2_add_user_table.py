"""add user table

Revision ID: 1be223974db2
Revises: cf0843b33b7d
Create Date: 2026-03-03 19:43:09.741934

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1be223974db2'
down_revision: Union[str, Sequence[str], None] = 'cf0843b33b7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("users", sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    sa.UniqueConstraint('email', name='uq_users_email'),
    sa.PrimaryKeyConstraint('id'))

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
