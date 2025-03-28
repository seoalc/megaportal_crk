"""Added closed text to applications

Revision ID: 86e0d06f4bf9
Revises: 4bfcac40e851
Create Date: 2025-03-14 10:51:04.888586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86e0d06f4bf9'
down_revision: Union[str, None] = '4bfcac40e851'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('applications', sa.Column('closed_text', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('applications', 'closed_text')
    # ### end Alembic commands ###
