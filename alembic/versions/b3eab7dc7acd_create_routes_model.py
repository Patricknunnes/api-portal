"""create_routes_model

Revision ID: b3eab7dc7acd
Revises: 03f8af2314be
Create Date: 2022-09-21 10:07:24.797831

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa
from src.db.settings.config import GUID

# revision identifiers, used by Alembic.
revision = 'b3eab7dc7acd'
down_revision = '03f8af2314be'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('routes',
                    sa.Column('id', GUID(), nullable=True),
                    sa.Column('method', sa.String(length=30), nullable=False),
                    sa.Column('path', sa.String(length=100), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
                    sa.PrimaryKeyConstraint('method', 'path')
                    )
    with op.batch_alter_table('routes', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_routes_id'), ['id'], unique=True)

    routes = sa.table('routes',
                      sa.column('id', GUID()),
                      sa.column('method', sa.String),
                      sa.column('path', sa.String)
                      )

    op.bulk_insert(routes, [
        {
            'id': uuid4(),
            'method': 'get',
            'path': '/role',
        },
        {
            'id': uuid4(),
            'method': 'get',
            'path': '/role/{id}',
        },
        {
            'id': uuid4(),
            'method': 'get',
            'path': '/user',
        },
        {
            'id': uuid4(),
            'method': 'get',
            'path': '/user/{id}',
        },
        {
            'id': uuid4(),
            'method': 'post',
            'path': '/user',
        },
        {
            'id': uuid4(),
            'method': 'patch',
            'path': '/user/{id}',
        },
    ])

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('routes', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_routes_id'))

    op.drop_table('routes')
    # ### end Alembic commands ###
