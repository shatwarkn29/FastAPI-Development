"""Create post table

Revision ID: 21de1349d3bf
Revises: 
Create Date: 2024-11-20 08:40:34.579762

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21de1349d3bf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable= False , primary_key= True),
                    sa.Column('title',sa.String(),nullable= False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
