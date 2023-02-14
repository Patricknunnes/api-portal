"""create messages-users table

Revision ID: 0d8071819e94
Revises: f1068ec1239d
Create Date: 2023-02-13 07:50:53.821920

"""
from alembic import op
import sqlalchemy as sa
from src.db.settings.config import GUID

# revision identifiers, used by Alembic.
revision = '0d8071819e94'
down_revision = 'f1068ec1239d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('messages_users',
        sa.Column('id', GUID(), nullable=False),
        sa.Column('message_id', GUID(), sa.ForeignKey('messages.id'), nullable=False),
        sa.Column('user_id', GUID(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('message_read', sa.Boolean(), nullable=False, server_default='t'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('message_id', 'user_id'),
        sa.UniqueConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('messages_users')
