"""create-refresh-token-table

Revision ID: ff2f0af73aaf
Revises: 2caba5973b7c
Create Date: 2023-03-30 15:16:46.143724

"""
from alembic import op
import sqlalchemy as sa
from src.db.settings.config import GUID

# revision identifiers, used by Alembic.
revision = 'ff2f0af73aaf'
down_revision = '2caba5973b7c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('tokens',
                    sa.Column('id', GUID(), primary_key=True),
                    sa.Column('user_id', GUID(), sa.ForeignKey('users.id'), nullable=False),
                    sa.Column('token_hash', sa.String(), nullable=False),
                    sa.Column('expiration_date', sa.TIMESTAMP, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('token_hash')
                    )


def downgrade() -> None:
    op.drop_table('tokens')
