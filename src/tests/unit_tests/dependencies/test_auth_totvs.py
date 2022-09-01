from unittest.mock import patch, MagicMock

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

    @patch('src.dependencies.totvs.soap_api.post')
    def test_handle_response_totvs(self, mock_post):
        '''
           Should return 1
        '''

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = RESPONSE_AUTH

        mock_post.return_value = mock_response

        result_auth = TotvsWebServer().get_auth_totvs(username='Teste',
                                                      password='password')
        self.assertTrue(result_auth)

        self.assertEqual(int(TotvsWebServer().clean_response(text=RESPONSE_AUTH)), 1)
