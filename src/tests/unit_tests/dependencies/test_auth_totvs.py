from unittest.mock import patch

from src.exceptions.exceptions import BadRequestException
from src.tests.mocks.totvs_mocks import RESPONSE_AUTH
from src.tests.settings import BaseTestCase
from src.dependencies.totvs.soap_api import TotvsWebServer
from src.tests.mocks.user_mocks import user_create_data


class TotvsWebServerTestClass(BaseTestCase):

    @patch('src.dependencies.totvs.soap_api.post')
    def test_handle_login_totvs_with_invalid_datas(self, mock_post):
        '''
            Should raise exception when user datas not found
        '''

        with self.assertRaises(BadRequestException) as error:
            TotvsWebServer().get_auth_totvs(username=user_create_data.get('username'),
                                            password=user_create_data.get('password'))
        exception = error.exception
        self.assertEqual(
            'Documento ou senha inválidos.',
            exception.detail
        )

    @patch.object(TotvsWebServer, 'get_auth_totvs', return_value=RESPONSE_AUTH)
    def test_handle_response_totvs(self, TotvsWebServer_mock):
        '''
            Should return 1
        '''

        result = TotvsWebServer().clean_response(text=RESPONSE_AUTH)
        self.assertEqual(int(result), 1)
