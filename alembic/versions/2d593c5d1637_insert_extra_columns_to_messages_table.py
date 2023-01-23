"""insert-extra-columns-to-messages-table

Revision ID: 2d593c5d1637
Revises: 874e886ca28e
Create Date: 2023-01-18 13:48:56.558964

"""
from alembic import op
import sqlalchemy as sa
from src.db.settings.config import GUID


# revision identifiers, used by Alembic.
revision = '2d593c5d1637'
down_revision = '874e886ca28e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('messages', sa.Column(
        'is_important',
        sa.Boolean(),
        nullable=False,
        server_default='f'
    ))
    op.add_column('messages', sa.Column(
        'created_at',
        sa.TIMESTAMP(),
        server_default=sa.text('now()'),
        nullable=True
    ))
    op.add_column('messages', sa.Column('updated_at', sa.TIMESTAMP(), nullable=True))
    op.add_column('messages', sa.Column(
        'created_by',
        GUID(),
        sa.ForeignKey('users.id'),
        nullable=True
    ))
    op.add_column('messages', sa.Column(
        'updated_by',
        GUID(),
        sa.ForeignKey('users.id'),
        nullable=True
    ))


def downgrade() -> None:
    op.drop_column('messages', 'is_important')
    op.drop_column('messages', 'created_at')
    op.drop_column('messages', 'created_by')
    op.drop_column('messages', 'updated_at')
    op.drop_column('messages', 'updated_by')
