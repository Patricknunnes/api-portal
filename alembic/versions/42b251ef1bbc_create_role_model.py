"""create_role_model

Revision ID: 42b251ef1bbc
Revises: 
Create Date: 2022-09-21 10:02:08.057334

"""
from alembic import op
import sqlalchemy as sa
from src.db.settings.config import GUID

# revision identifiers, used by Alembic.
revision = '42b251ef1bbc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
                    sa.Column('id', GUID(), nullable=False),
                    sa.Column('name', sa.String(length=30), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )

    role = sa.table('roles',
                    sa.column('id', GUID()),
                    sa.column('name', sa.String),
                    )

    op.bulk_insert(role, [
        {
            'id': '5a1a0a10-4973-4ced-94e6-119ce277630d',
            'name': 'root'
        },
        {
            'id': '953dc20c-dcbc-4166-9441-8d94716346b3',
            'name': 'colaborador'
        },
        {
            'id': '69fe9d12-36d2-4454-b820-551b6e9058f0',
            'name': 'professor'
        },
        {
            'id': '41354ecb-2b9a-446c-b26a-15e193592206',
            'name': 'aluno'
        },
    ])


# ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles')
    # ### end Alembic commands ###
