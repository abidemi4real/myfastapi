"""add foreign key for posts

Revision ID: 4007a5a6c6c6
Revises: 84611877cd1d
Create Date: 2022-06-30 08:50:47.671462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4007a5a6c6c6'
down_revision = '84611877cd1d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("post_owner_fk", source_table="posts", referent_table="users", local_cols=['owner_id'],
    remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_owner_fk", "posts")
    op.drop_column("posts", "owner_id")
    pass
