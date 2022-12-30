"""create message model

Revision ID: 3929f7bd1d81
Revises: 61a172f66d6d
Create Date: 2022-12-30 11:18:34.750209

"""
from alembic import op
import sqlalchemy as sa
from src.db.settings.config import GUID

# revision identifiers, used by Alembic.
revision = '3929f7bd1d81'
down_revision = '61a172f66d6d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('messages',
                    sa.Column('id', GUID(), primary_key=True),
                    sa.Column('title', sa.String(length=50), nullable=False),
                    sa.Column('text', sa.String(), nullable=False),
                    sa.Column('expiration_date', sa.TIMESTAMP, nullable=True),
                    sa.Column('role_permission', GUID(), sa.ForeignKey('roles.id'), nullable=True),
                    sa.Column('user_permission', GUID(), sa.ForeignKey('users.id'), nullable=True)
                    )


def downgrade() -> None:
    op.drop_table('messages')
