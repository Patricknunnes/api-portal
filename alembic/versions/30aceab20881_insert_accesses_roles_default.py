"""insert_accesses_roles_default

Revision ID: 30aceab20881
Revises: 0213b8e4a209
Create Date: 2023-02-14 10:29:28.212421

"""
from alembic import op
import sqlalchemy as sa
from src.db.settings.config import GUID

# revision identifiers, used by Alembic.
revision = '30aceab20881'
down_revision = '0213b8e4a209'
branch_labels = None
depends_on = None


def upgrade() -> None:
    accesses_roles = sa.table('accesses_roles',
        sa.column('id', GUID()),
        sa.column('access_id', GUID()),
        sa.column('role_id', GUID())
    )

    admin = '953dc20c-dcbc-4166-9441-8d94716346b3'
    professor = '69fe9d12-36d2-4454-b820-551b6e9058f0'
    student = '41354ecb-2b9a-446c-b26a-15e193592206'

    totvs = 'f0234972-d4e4-4a98-9487-7ac77d821448'
    canvas = 'ca8cf585-5514-42ad-a233-5d934b569f14'
    minha_biblioteca = 'fec63a7f-029f-4217-9916-b29db4593143'
    office = 'b76540b2-de16-447b-ad13-fd33720aa346'

    op.bulk_insert(accesses_roles, [
        {
            'id': 'aef94fef-8ace-4d46-8a89-1aae97c5805f',
            'access_id': totvs,
            'role_id': admin
        },
        {
            'id': '106a9e91-b7a0-45ad-963a-665286d59408',
            'access_id': totvs,
            'role_id': student
        },
        {
            'id': 'ef7ac5a6-244e-40a7-b9fe-6c6ac88741a4',
            'access_id': totvs,
            'role_id': professor
        },
        {
            'id': '130a130a-9c08-459d-8c5e-64625eadf1aa',
            'access_id': minha_biblioteca,
            'role_id': professor
        },
        {
            'id': '4250f568-1c1b-49ce-b783-5d4f68270598',
            'access_id': minha_biblioteca,
            'role_id': student
        },
        {
            'id': '5fe4658f-e86f-4ba2-a8f8-01e7a0d0099f',
            'access_id': canvas,
            'role_id': professor
        },
        {
            'id': '7ef8a4ec-43c3-4f13-b400-a571ad5ffea4',
            'access_id': canvas,
            'role_id': student
        },
        {
            'id': 'b9426517-5e98-4b74-aa15-e3a4d35a4776',
            'access_id': office,
            'role_id': student
        },
        {
            'id': '8b2a328d-6174-48bd-81fe-052bf03c6c15',
            'access_id': office,
            'role_id': professor
        },
        {
            'id': 'd3fc2365-c252-4939-9655-08dbd66af471',
            'access_id': office,
            'role_id': admin
        }
    ])


def downgrade() -> None:
    op.execute('TRUNCATE TABLE accesses_roles;')
