import os
import re
from dotenv import load_dotenv
from requests import post
from requests.auth import HTTPBasicAuth

from src.settings.settings import BASE_DIR
from src.exceptions.exceptions import BadRequestException

load_dotenv(os.path.join(BASE_DIR, '../.env'))


class TotvsWebServer:

    def get_auth_totvs(self, username: str, password: str) -> bool:
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

        response = post(url=os.getenv('URL_AUTH_TOTVS'),
                        headers=HEADERS,
                        data=BODY,
                        auth=HTTPBasicAuth(username=username, password=password))

        if response.status_code != 200 or self.clean_response(
            text=str(response.content)
        ) != 1:
            raise BadRequestException('Documento ou senha inválidos.')

        return True

    def clean_response(self, text: str):
        result = re.findall(r'<AutenticaAcessoResult>\d', text)[0] \
            .replace('<AutenticaAcessoResult>', '')
        return int(result)
