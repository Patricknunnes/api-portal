"""insert message permissions

Revision ID: 874e886ca28e
Revises: 3929f7bd1d81
Create Date: 2023-01-02 12:39:35.643644

"""
from alembic import op
import sqlalchemy as sa
from src.db.settings.config import GUID


# revision identifiers, used by Alembic.
revision = '874e886ca28e'
down_revision = '3929f7bd1d81'
branch_labels = None
depends_on = None

list_route_id = '5545ccbe-9e27-4d3f-b26d-aaa5466906c6'
list_permission_id = 'd8959e57-cfb1-417a-91dc-3af0ee0264d2'
create_route_id = '5545ccbe-9e27-4d3f-b26d-aaa5466906c7'
create_permission_id = 'd8959e57-cfb1-417a-91dc-3af0ee0264b2'
delete_route_id = '5545ccbe-9e27-4d3f-b26d-aaa5466906c1'
delete_permission_id = 'd8959e57-cfb1-417a-91dc-3af0ee1264b2'
patch_route_id = '5545ccbe-9e27-4d3f-b26d-aaa5496906c1'
patch_permission_id = 'd8959e57-cfb1-417a-91dc-3bf0ee1264b2'


def upgrade() -> None:
    routes = sa.table('routes',
                      sa.column('id', GUID()),
                      sa.column('method', sa.String),
                      sa.column('path', sa.String)
                      )

    op.bulk_insert(routes, [
        {
            'id': list_route_id,
            'method': 'get',
            'path': '/message',
        },
        {
            'id': create_route_id,
            'method': 'post',
            'path': '/message',
        },
        {
            'id': delete_route_id,
            'method': 'delete',
            'path': '/message/{id}',
        },
        {
            'id': patch_route_id,
            'method': 'patch',
            'path': '/message/{id}',
        }
    ])

    permissions = sa.table('permissions',
                           sa.column('id', GUID()),
                           sa.column('role_id', GUID()),
                           sa.column('route_id', GUID())
                           )
    
    op.bulk_insert(permissions, [
        {
            'id': list_permission_id,
            'role_id': '953dc20c-dcbc-4166-9441-8d94716346b3',
            'route_id': list_route_id,
        },
        {
            'id': create_permission_id,
            'role_id': '953dc20c-dcbc-4166-9441-8d94716346b3',
            'route_id': create_route_id,
        },
        {
            'id': delete_permission_id,
            'role_id': '953dc20c-dcbc-4166-9441-8d94716346b3',
            'route_id': delete_route_id,
        },
        {
            'id': patch_permission_id,
            'role_id': '953dc20c-dcbc-4166-9441-8d94716346b3',
            'route_id': patch_route_id,
        }
    ])

def downgrade() -> None:
    route_id_list = [
        list_route_id,
        create_route_id,
        delete_route_id,
        patch_route_id
    ]
    permission_id_list = [
        list_permission_id,
        create_permission_id,
        delete_permission_id,
        patch_permission_id
    ]

    op.execute(f"DELETE FROM public.permissions WHERE id in {list_permission_id, create_permission_id, delete_permission_id, patch_permission_id}")
    op.execute(f"DELETE FROM public.routes WHERE id in {list_route_id, create_route_id, delete_route_id, patch_route_id}")
