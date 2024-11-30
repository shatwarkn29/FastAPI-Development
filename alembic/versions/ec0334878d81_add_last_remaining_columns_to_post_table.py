"""add last remaining columns to post table

Revision ID: ec0334878d81
Revises: e160e4cb026e
Create Date: 2024-11-30 05:12:20.605124

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec0334878d81'
down_revision: Union[str, None] = 'e160e4cb026e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('published',sa.Boolean(),nullable= False , server_default ='True'))
    op.add_column('posts',
                  sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable = False , server_default = sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
