"""create client model

Revision ID: 9de5bdcb2b95
Revises: 0b8009009ddd
Create Date: 2022-12-14 10:38:16.127797

"""
from alembic import op
import sqlalchemy as sa
from src.db.settings.config import GUID

# revision identifiers, used by Alembic.
revision = '9de5bdcb2b95'
down_revision = '0b8009009ddd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('clients',
                    sa.Column('id', GUID(), nullable=False, primary_key=True),
                    sa.Column('client_id', sa.String(length=30), nullable=False, unique=True),
                    sa.Column('client_secret', sa.String(length=255), nullable=True),
                    sa.Column('redirect_uri', sa.String(255), nullable=False)
                    )


def downgrade() -> None:
    op.drop_table('clients')
