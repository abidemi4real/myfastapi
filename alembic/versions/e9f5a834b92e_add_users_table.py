"""add users table

Revision ID: e9f5a834b92e
Revises: 5f68f7ec7189
Create Date: 2022-06-30 06:27:49.314841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9f5a834b92e'
down_revision = '5f68f7ec7189'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False), sa.Column('email', sa.String(), nullable=False), sa.Column('password', sa.String(), nullable=False), sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email'))
    pass

def downgrade() -> None:
    op.drop_table("users")
    pass
