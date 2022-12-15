from unittest.mock import patch, MagicMock

from src.db.cruds.user_crud import UserCRUD
from src.db.models.models import UserModel
from src.dependencies.sso.validators import ParamsValidator
from src.tests.mocks.user_mocks import totvs_user_db_response
from src.tests.settings import ApiBaseTestCase


class SSORouteTestClass(ApiBaseTestCase):
    auth_params = (
        '?client_id=client1&redirect_uri=valid_uri'
        '&response_type=code&scope=openid&state=jwt_state'
    )
    invalid_request_redirect_uri = 'valid_uri?error=invalid_request&state=jwt_state'

    @patch('src.dependencies.sso.sso_utils.decode_token', return_value=None)
    def test_handle_auth_when_decode_token_returns_none(self, _):
        response = self.client.post(
            f'/sso/auth{self.auth_params}',
            data={'access_key': 'invalid_access_key'}
        )

        self.assertEqual(401, response.status_code)
        self.assertEqual(
            {'detail': 'invalid_token'},
            response.json()
        )

    @patch.object(UserCRUD, 'get', return_value=None)
    @patch('src.dependencies.sso.sso_utils.decode_token', return_value='invalid_user_id')
    def test_handle_auth_when_decode_token_returns_invalid_user_id(self, *_):
        response = self.client.post(
            f'/sso/auth{self.auth_params}',
            data={'access_key': 'invalid_user_id_access_key'}
        )

        self.assertEqual(401, response.status_code)
        self.assertEqual(
            {'detail': 'invalid_token'},
            response.json()
        )

    @patch.object(ParamsValidator, 'validate_authorize_params', return_value=False)
    @patch.object(UserCRUD, 'get', return_value=totvs_user_db_response)
    @patch('src.dependencies.sso.sso_utils.decode_token', return_value=totvs_user_db_response['id'])
    def test_handle_auth_with_invalid_params(self, *_):
        response = self.client.post(
            f'/sso/auth{self.auth_params}',
            data={'access_key': 'access_key'}
        )

        self.assertEqual(307, response.status_code)
        self.assertEqual(self.invalid_request_redirect_uri, response.headers['location'])

    @patch.object(ParamsValidator, 'validate_authorize_params', return_value=True)
    @patch.multiple(
        UserCRUD,
        get=MagicMock(return_value=UserModel(**totvs_user_db_response)),
        patch=MagicMock(return_value=None)
    )
    @patch('src.dependencies.sso.sso_utils.decode_token', return_value=totvs_user_db_response['id'])
    def test_handle_auth_with_valid_params(self, *_):
        response = self.client.post(
            f'/sso/auth{self.auth_params}',
            data={'access_key': 'access_key'}
        )

        self.assertEqual(307, response.status_code)
        self.assertTrue('state=jwt_state&code=' in response.headers['location'])
