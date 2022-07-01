"""add column content to posts table

Revision ID: 5f68f7ec7189
Revises: 71c787ebbacd
Create Date: 2022-06-30 06:13:30.512359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f68f7ec7189'
down_revision = '71c787ebbacd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
