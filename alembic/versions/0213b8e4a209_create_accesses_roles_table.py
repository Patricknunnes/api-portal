"""create accesses roles table

Revision ID: 0213b8e4a209
Revises: d0062de93bf5
Create Date: 2023-02-14 10:24:34.052139

"""
from alembic import op
import sqlalchemy as sa
from src.db.settings.config import GUID

# revision identifiers, used by Alembic.
revision = '0213b8e4a209'
down_revision = 'd0062de93bf5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('accesses_roles',
        sa.Column('id', GUID(), nullable=False),
        sa.Column('access_id', GUID(), sa.ForeignKey('accesses.id'), nullable=False),
        sa.Column('role_id', GUID(), sa.ForeignKey('roles.id'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('access_id', 'role_id'),
        sa.UniqueConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('accesses_roles')
