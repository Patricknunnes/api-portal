"""insert_first_accesses

Revision ID: d0062de93bf5
Revises: 53a6b497cf5f
Create Date: 2023-02-14 08:49:00.019943

"""
from alembic import op
import sqlalchemy as sa
from src.db.settings.config import GUID

# revision identifiers, used by Alembic.
revision = 'd0062de93bf5'
down_revision = '53a6b497cf5f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    accesses = sa.table('accesses',
        sa.column('id', GUID()),
        sa.column('title', sa.String),
        sa.column('description', sa.String),
        sa.column('icon_path', sa.String),
        sa.column('link_path', sa.String))

    op.bulk_insert(accesses, [
        {
            'id': 'ca8cf585-5514-42ad-a233-5d934b569f14',
            'title': 'Aulas e Conteúdo',
            'description': 'Acesso a sua sala virtual e a todos os materiais disponibilizados.',
            'icon_path': 'M8,12H16V14H8V12M10,20H6V4H13V9H18V12.1L20,10.1V8L14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H10V20M8,18H12.1L13,17.1V16H8V18M20.2,13C20.3,13 20.5,13.1 20.6,13.2L21.9,14.5C22.1,14.7 22.1,15.1 21.9,15.3L20.9,16.3L18.8,14.2L19.8,13.2C19.9,13.1 20,13 20.2,13M20.2,16.9L14.1,23H12V20.9L18.1,14.8L20.2,16.9Z',
            'link_path': 'https://idor.test.instructure.com/login/openid_connect'
        },
        {
            'id': 'fec63a7f-029f-4217-9916-b29db4593143',
            'title': 'Biblioteca',
            'description': 'Acesse a biblioteca virtual do IDOR.',
            'icon_path': 'M19 2L14 6.5V17.5L19 13V2M6.5 5C4.55 5 2.45 5.4 1 6.5V21.16C1 21.41 1.25 21.66 1.5 21.66C1.6 21.66 1.65 21.59 1.75 21.59C3.1 20.94 5.05 20.5 6.5 20.5C8.45 20.5 10.55 20.9 12 22C13.35 21.15 15.8 20.5 17.5 20.5C19.15 20.5 20.85 20.81 22.25 21.56C22.35 21.61 22.4 21.59 22.5 21.59C22.75 21.59 23 21.34 23 21.09V6.5C22.4 6.05 21.75 5.75 21 5.5V19C19.9 18.65 18.7 18.5 17.5 18.5C15.8 18.5 13.35 19.15 12 20V6.5C10.55 5.4 8.45 5 6.5 5Z',
            'link_path': 'https://dliportal.zbra.com.br/Login.aspx?key=idor'
        },
        {
            'id': 'b76540b2-de16-447b-ad13-fd33720aa346',
            'title': 'Office 365',
            'description': 'Acesso a e-mails e ao pacote completo do Office 365.',
            'icon_path': '/src/assets/icon-office-365.svg',
            'link_path': 'http://office.idor.org/'
        },
        {
            'id': 'f0234972-d4e4-4a98-9487-7ac77d821448',
            'title': 'Acadêmico e Financeiro',
            'description': 'Secretaria digital: requerimento de documentos, 2ª via de boleto e informações acadêmicas.',
            'icon_path': 'M21 10H17V8L12.5 6.2V4H15V2H11.5V6.2L7 8V10H3C2.45 10 2 10.45 2 11V22H10V17H14V22H22V11C22 10.45 21.55 10 21 10M8 20H4V17H8V20M8 15H4V12H8V15M12 8C12.55 8 13 8.45 13 9S12.55 10 12 10 11 9.55 11 9 11.45 8 12 8M14 15H10V12H14V15M20 20H16V17H20V20M20 15H16V12H20V15Z',
            'link_path': '/sso/totvs'
        }
    ])

def downgrade() -> None:
    op.execute('TRUNCATE TABLE accesses;')
