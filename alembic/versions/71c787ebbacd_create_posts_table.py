"""create posts table

Revision ID: 71c787ebbacd
Revises: 
Create Date: 2022-06-30 06:05:17.551655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71c787ebbacd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), primary_key= True, nullable= False), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass