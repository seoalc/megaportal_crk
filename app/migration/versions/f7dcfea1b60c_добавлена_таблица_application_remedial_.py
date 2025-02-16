"""Добавлена таблица application_remedial_users

Revision ID: f7dcfea1b60c
Revises: 
Create Date: 2025-02-13 16:50:28.828460

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'f7dcfea1b60c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('application_remedial_users',
    sa.Column('application_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['application_id'], ['applications.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('application_id', 'user_id')
    )
    op.alter_column('applications', 'application_status',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.drop_column('applications', 'remedial_user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('applications', sa.Column('remedial_user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.alter_column('applications', 'application_status',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.drop_table('application_remedial_users')
    # ### end Alembic commands ###
