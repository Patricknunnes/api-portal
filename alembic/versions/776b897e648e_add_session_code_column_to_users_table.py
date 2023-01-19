"""add session code column to users table

Revision ID: 776b897e648e
Revises: 9de5bdcb2b95
Create Date: 2022-12-14 10:58:35.848849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '776b897e648e'
down_revision = '9de5bdcb2b95'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('session_code', sa.String(length=25), nullable=True, unique=True))


def downgrade() -> None:
    op.drop_column('users', 'session_code')
