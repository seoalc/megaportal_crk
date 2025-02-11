"""update users and applications tables

Revision ID: 638f2fd30d5a
Revises: 45fc15269279
Create Date: 2025-02-03 16:54:45.422779

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '638f2fd30d5a'
down_revision: Union[str, None] = '45fc15269279'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('applications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('appearance_date', sa.Date(), nullable=False),
    sa.Column('subscriber_number', sa.Integer(), nullable=False),
    sa.Column('subscriber_addres', sa.String(length=255), nullable=False),
    sa.Column('complaint_text', sa.Text(), nullable=True),
    sa.Column('contact_number', sa.String(length=15), nullable=False),
    sa.Column('solution_description', sa.Text(), nullable=True),
    sa.Column('user_id_created_application', sa.Integer(), nullable=False),
    sa.Column('application_status', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id_created_application'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('applications')
    # ### end Alembic commands ###
