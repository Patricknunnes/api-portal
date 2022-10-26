from unittest.mock import patch, MagicMock

from src.exceptions.exceptions import BadRequestException
from src.tests.mocks.totvs_mocks import RESPONSE_AUTH
from src.tests.settings import BaseTestCase
from src.dependencies.totvs.soap_api import TotvsWebServer
from src.tests.mocks.auth_mocks import login_incorrect_username, valid_login


class TotvsWebServerTestClass(BaseTestCase):
    @patch('src.dependencies.totvs.soap_api.post')
    def test_handle_login_totvs_with_invalid_data(self, mock_post):
        '''
            Should raise exception when get invalid login data
        '''

        with self.assertRaises(BadRequestException) as error:
            TotvsWebServer().get_auth_totvs(
                username=login_incorrect_username.get('username'),
                password=login_incorrect_username.get('password')
            )
        exception = error.exception
        self.assertEqual(
            'Usuário ou senha inválidos.',
            exception.detail
        )

    @patch('src.dependencies.totvs.soap_api.post')
    def test_handle_response_totvs(self, mock_post):
        '''
           Should return 1 when get valid login data
        '''

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = RESPONSE_AUTH

        mock_post.return_value = mock_response

        result_auth = TotvsWebServer().get_auth_totvs(
            username=valid_login.get('username'),
            password=valid_login.get('password')
        )
        self.assertTrue(result_auth)

        self.assertEqual(int(TotvsWebServer().clean_response(text=RESPONSE_AUTH)), 1)
