"""add content table to post table

Revision ID: 7960e9c0e733
Revises: e65cf8727196
Create Date: 2025-12-30 19:26:50.877229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7960e9c0e733'
down_revision: Union[str, Sequence[str], None] = 'e65cf8727196'
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
