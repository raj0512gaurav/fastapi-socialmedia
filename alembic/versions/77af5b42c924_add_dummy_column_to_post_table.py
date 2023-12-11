"""add dummy column to post table

Revision ID: 77af5b42c924
Revises: 
Create Date: 2023-12-10 18:44:05.965585

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77af5b42c924'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('dummy', sa.Integer()))

def downgrade() -> None:
    op.drop_column('posts', 'dummy')
