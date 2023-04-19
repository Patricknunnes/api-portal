"""insert admin permission to user and role lists

Revision ID: f1068ec1239d
Revises: 2d593c5d1637
Create Date: 2023-02-06 09:03:56.719805

"""
from alembic import op
import sqlalchemy as sa
from src.db.settings.config import GUID


# revision identifiers, used by Alembic.
revision = 'f1068ec1239d'
down_revision = '2d593c5d1637'
branch_labels = None
depends_on = None

admin_id = '953dc20c-dcbc-4166-9441-8d94716346b3'
list_user_permission_id = 'c7e3adfe-b768-41e5-a75a-72550261476f'
list_role_permission_id = '85753c22-91c6-451b-9744-bbc204d142c5'


def upgrade() -> None:
    connection = op.get_bind()

    res_user = connection.execute(
        "SELECT id from public.routes WHERE method = 'get' AND path = '/user'"
    )
    list_user_route_id = res_user.first()[0]

    res_role = connection.execute(
        "SELECT id from public.routes WHERE method = 'get' AND path = '/role'"
    )
    list_role_route_id = res_role.first()[0]

    permissions = sa.table('permissions',
                           sa.column('id', GUID()),
                           sa.column('role_id', GUID()),
                           sa.column('route_id', GUID())
                           )

    op.bulk_insert(permissions, [
        {
            'id': list_user_permission_id,
            'role_id': admin_id,
            'route_id': list_user_route_id,
        },
        {
            'id': list_role_permission_id,
            'role_id': admin_id,
            'route_id': list_role_route_id,
        }
    ])


def downgrade() -> None:
    op.execute(f"DELETE FROM public.permissions WHERE id IN {list_user_permission_id, list_role_permission_id}")
