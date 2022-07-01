"""add more columns to posts

Revision ID: fc8b1ed5aae3
Revises: 4007a5a6c6c6
Create Date: 2022-06-30 09:03:22.666026

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc8b1ed5aae3'
down_revision = '4007a5a6c6c6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(),nullable=False, server_default="True")),
    op.add_column("posts", sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
