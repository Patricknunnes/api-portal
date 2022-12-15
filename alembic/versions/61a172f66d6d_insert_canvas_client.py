"""insert canvas client

Revision ID: 61a172f66d6d
Revises: 776b897e648e
Create Date: 2022-12-14 11:34:28.605171

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from src.db.settings.config import GUID


# revision identifiers, used by Alembic.
revision = '61a172f66d6d'
down_revision = '776b897e648e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    clients_table = sa.table(
        'clients',
        sa.column('id', GUID()),
        sa.column('client_id', sa.String),
        sa.column('client_secret', sa.String),
        sa.column('redirect_uri', sa.String)
    )

    op.bulk_insert(clients_table, [
        {
            'id': uuid4(),
            'client_id': 'canvas',
            'redirect_uri': 'https://sso.test.canvaslms.com/login/oauth2/callback'
        }
    ])


def downgrade() -> None:
    op.execute('TRUNCATE TABLE clients;')
