import os
import re
from dotenv import load_dotenv
from requests import post
from requests.auth import HTTPBasicAuth

from src.settings.settings import BASE_DIR
from src.exceptions.exceptions import BadRequestException

load_dotenv(os.path.join(BASE_DIR, '../.env'))


def get_auth_totvs(username: str, password: str) -> bool:
    URL_TOTVS = os.getenv('URL_AUTH_TOTVS')

    HEADERS = {
        'Content-Type': 'text/xml;charset=UTF-8',
        'SOAPAction': 'http://www.totvs.com/IwsBase/AutenticaAcesso',
    }

    BODY = '''
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
             xmlns:tot="http://www.totvs.com/">
               <soapenv:Header/>
               <soapenv:Body>
                  <tot:AutenticaAcesso/>
               </soapenv:Body>
            </soapenv:Envelope>
            '''

    response = post(url=URL_TOTVS,
                    headers=HEADERS,
                    data=BODY,
                    auth=HTTPBasicAuth(username=username, password=password))

    if response.status_code != 200:
        raise BadRequestException('Usuário ou senha inválido.')

    result = re.findall(r'<AutenticaAcessoResult>\d', str(response.content))[0] \
        .replace('<AutenticaAcessoResult>', '')

    return result
