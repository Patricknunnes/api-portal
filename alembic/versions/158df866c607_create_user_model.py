"""create_user_model

Revision ID: 158df866c607
Revises: 42b251ef1bbc
Create Date: 2022-09-21 10:02:54.777026

"""
from alembic import op
import sqlalchemy as sa
from src.db.settings.config import GUID

# revision identifiers, used by Alembic.
revision = '158df866c607'
down_revision = '42b251ef1bbc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', GUID(), nullable=False),
                    sa.Column('role_id', GUID(), nullable=True),
                    sa.Column('name', sa.String(length=150), nullable=False),
                    sa.Column('email', sa.String(length=150), nullable=False),
                    sa.Column('document', sa.String(length=11), nullable=False),
                    sa.Column('phone', sa.String(length=12), nullable=True),
                    sa.Column('username', sa.String(length=50), nullable=False),
                    sa.Column('password', sa.String(length=255), nullable=False),
                    sa.Column('image', sa.String(), nullable=True),
                    sa.Column('is_totvs', sa.Boolean(), nullable=False),
                    sa.Column('canvas_id', sa.Integer(), nullable=True),
                    sa.Column('last_sync', sa.TIMESTAMP(), nullable=True),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
                    sa.Column('session_code', sa.String(length=25), nullable=True),
                    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('canvas_id'),
                    sa.UniqueConstraint('username'),
                    sa.UniqueConstraint('session_code')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
