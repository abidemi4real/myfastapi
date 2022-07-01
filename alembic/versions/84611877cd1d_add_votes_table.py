"""add votes table

Revision ID: 84611877cd1d
Revises: e9f5a834b92e
Create Date: 2022-06-30 08:27:21.197099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84611877cd1d'
down_revision = 'e9f5a834b92e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    #op.create_table('votes', sa.Column('user_id', sa.Integer(), nullable=False, primary_key=True), 
    #sa.Column('post_id', sa.Integer(), nullable=False, primary_key=True))
    #op.create_foreign_key("post_user_fk", source_table="posts", referent_table="users", local_cols=['id'], remote_cols=['id'], ondelete="CASCADE")
    #op.create_foreign_key("user_post_fk", source_table="users", referent_table="posts", local_cols=['id'], remote_cols=['id'], ondelete="CASCADE")
    pass

def downgrade() -> None:
    #op.drop_table("votes")
    pass