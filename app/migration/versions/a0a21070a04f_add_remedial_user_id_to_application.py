"""Add remedial_user_id to Application

Revision ID: a0a21070a04f
Revises: 638f2fd30d5a
Create Date: 2025-02-07 15:41:38.927724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a0a21070a04f'
down_revision: Union[str, None] = '638f2fd30d5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
