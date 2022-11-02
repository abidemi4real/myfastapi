"""add column to users table

Revision ID: c8f5d5e7ae4a
Revises: 688e2a8ea74d
Create Date: 2022-10-25 09:15:13.124847

"""
from tokenize import String
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8f5d5e7ae4a'
down_revision = '688e2a8ea74d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column('username', sa.String()))


def downgrade() -> None:
    op.drop_column("users", "username")
