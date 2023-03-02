"""create_registrations_table

Revision ID: 60af0804b470
Revises: 228925d760cb
Create Date: 2023-03-02 09:38:26.747928

"""
from alembic import op
import sqlalchemy as sa
from src.db.settings.config import GUID

# revision identifiers, used by Alembic.
revision = '60af0804b470'
down_revision = '228925d760cb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint('users_document_key', 'users', ['document'])
    op.create_table('registrations',
        sa.Column('id', GUID(), nullable=False),
        sa.Column('document', sa.String(length=11), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=False),
        sa.Column('birthdate', sa.TIMESTAMP(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('service', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['document'], ['users.document']),
        sa.PrimaryKeyConstraint('document', 'service'),
        sa.UniqueConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('registrations')
    op.drop_constraint('users_document_key', 'users')

