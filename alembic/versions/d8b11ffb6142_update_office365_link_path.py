"""update_office365_link_path

Revision ID: d8b11ffb6142
Revises: 60af0804b470
Create Date: 2023-03-03 19:21:41.270090

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd8b11ffb6142'
down_revision = '60af0804b470'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("UPDATE public.accesses SET link_path = '/sso/office365' WHERE id = 'b76540b2-de16-447b-ad13-fd33720aa346'")


def downgrade() -> None:
    op.execute("UPDATE public.accesses SET link_path = 'http://office.idor.org/' WHERE id = 'b76540b2-de16-447b-ad13-fd33720aa346'")
