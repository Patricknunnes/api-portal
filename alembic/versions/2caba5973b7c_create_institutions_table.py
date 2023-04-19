"""create-institutions-table

Revision ID: 2caba5973b7c
Revises: 228925d760cb
Create Date: 2023-03-27 15:29:44.732660

"""
from alembic import op
import sqlalchemy as sa
from src.db.settings.config import GUID

# revision identifiers, used by Alembic.
revision = '2caba5973b7c'
down_revision = '228925d760cb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    institutions = op.create_table('institutions',
                    sa.Column('id', GUID()),
                    sa.Column('name', sa.String(length=50), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )

    op.bulk_insert(institutions, [
        {
            'id': '02650041-db4b-43bf-8579-7adf2fb73ef2',
            'name': 'UNINEVES'
        },
        {
            'id': 'dcef34bf-2cc6-4d67-b6af-803e7e33d0f3',
            'name': 'IDOR'
        }
    ])

    op.add_column('users', sa.Column(
        'institution_id',
        GUID(),
        sa.ForeignKey('institutions.id'),
        nullable=False,
        server_default='dcef34bf-2cc6-4d67-b6af-803e7e33d0f3'
    ))

    op.add_column('divergences', sa.Column(
        'institution_id',
        GUID(),
        sa.ForeignKey('institutions.id'),
        nullable=False,
        server_default='dcef34bf-2cc6-4d67-b6af-803e7e33d0f3'
    ))


def downgrade() -> None:
    op.drop_column('users', 'institution_id')
    op.drop_column('divergences', 'institution_id')
    op.drop_table('institutions')
