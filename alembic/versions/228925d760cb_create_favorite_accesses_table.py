"""create favorite_accesses table

Revision ID: 228925d760cb
Revises: 30aceab20881
Create Date: 2023-02-14 14:46:40.819956

"""
from alembic import op
import sqlalchemy as sa
from src.db.settings.config import GUID

# revision identifiers, used by Alembic.
revision = '228925d760cb'
down_revision = '30aceab20881'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('favorite_accesses',
        sa.Column('id', GUID(), nullable=False),
        sa.Column('access_id', GUID(), sa.ForeignKey('accesses.id'), nullable=False),
        sa.Column('user_id', GUID(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('access_id', 'user_id'),
        sa.UniqueConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('favorite_accesses')
