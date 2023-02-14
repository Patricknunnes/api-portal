"""create access table

Revision ID: 53a6b497cf5f
Revises: 0d8071819e94
Create Date: 2023-02-14 08:33:10.631527

"""
from alembic import op
import sqlalchemy as sa
from src.db.settings.config import GUID

# revision identifiers, used by Alembic.
revision = '53a6b497cf5f'
down_revision = '0d8071819e94'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('accesses',
        sa.Column('id', GUID(), primary_key=True),
        sa.Column('title', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(150), nullable=False),
        sa.Column('icon_path', sa.String(), nullable=False),
        sa.Column('link_path', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('accesses')
