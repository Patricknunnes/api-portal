from unittest.mock import patch, MagicMock

from src.db.cruds.user_crud import UserCRUD
from src.db.models.models import UserModel
from src.dependencies.sso.validators import ParamsValidator
from src.tests.mocks.user_mocks import totvs_user_db_response
from src.dependencies.sso.sso_utils import current_user
from src.tests.mocks.client_mocks import valid_token_request_body
from src.tests.settings import ApiBaseTestCase

from src.main import app


class SSORouteTestClass(ApiBaseTestCase):
    auth_params = (
        '?client_id=client1&redirect_uri=valid_uri'
        '&response_type=code&scope=openid&state=jwt_state'
    )
    invalid_request_redirect_uri = 'valid_uri?error=invalid_request&state=jwt_state'

    def setUp(self) -> None:
        self.token_request_body = valid_token_request_body
        return super().setUp()

    def tearDown(self) -> None:
        self.token_request_body = valid_token_request_body
        return super().tearDown()

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
    @patch(
        'src.dependencies.sso.sso_utils.decode_token',
        return_value=totvs_user_db_response['id']
    )
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
    @patch(
        'src.dependencies.sso.sso_utils.decode_token',
        return_value=totvs_user_db_response['id']
    )
    def test_handle_auth_with_valid_params(self, *_):
        response = self.client.post(
            f'/sso/auth{self.auth_params}',
            data={'access_key': 'access_key'}
        )

        self.assertEqual(307, response.status_code)
        self.assertTrue('state=jwt_state&code=' in response.headers['location'])

    @patch.object(ParamsValidator, 'validate_token_params', return_value=False)
    def test_handle_token_with_invalid_body(self, _):
        self.token_request_body['grant_type'] = 'invalid_type'
        response = self.client.post('/sso/token', data=self.token_request_body)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'detail': 'invalid_request'}, response.json())

    @patch.object(ParamsValidator, 'validate_token_params', return_value=True)
    @patch.object(UserCRUD, 'get', return_value=None)
    def test_handle_token_with_invalid_code(self, *_):
        self.token_request_body['code'] = 'invalid_code'
        response = self.client.post('/sso/token', data=self.token_request_body)

        self.assertEqual(400, response.status_code)
        self.assertEqual({'detail': 'invalid_request'}, response.json())

    @patch('src.dependencies.sso.routes.create_access_token', return_value='token')
    @patch.object(UserCRUD, 'get', return_value=UserModel(**totvs_user_db_response))
    @patch.object(ParamsValidator, 'validate_token_params', return_value=True)
    def test_handle_token_with_valid_code(self, *_):
        response = self.client.post('/sso/token', data=self.token_request_body)

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.headers['Cache-Control'], 'no-store')
        self.assertEqual(response.headers['Pragma'], 'no-cache')
        self.assertEqual(
            {
                'access_token': 'token',
                'token_type': 'Bearer',
                'expires_in': 1800,
                'id_token': 'token'
            },
            response.json()
        )

    def test_handle_user_info_without_token(self):
        response = self.client.get('/sso/user_info')

        self.assertEqual(401, response.status_code)
        self.assertEqual({'detail': 'Not authenticated'}, response.json())

    def test_handle_user_info_with_invalid_token(self):
        response = self.client.get(
            '/sso/user_info',
            headers={'Authorization': 'Bearer invalid_token'}
        )

        self.assertEqual(401, response.status_code)
        self.assertEqual({'detail': 'invalid_token'}, response.json())

    def test_handle_user_info_with_valid_token(self):
        app.dependency_overrides[current_user] = (
            lambda: UserModel(**totvs_user_db_response)
        )
        response = self.client.get(
            '/sso/user_info',
            headers={'Authorization': 'Bearer valid_token'}
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {
                'sub': totvs_user_db_response['username'],
                'name': totvs_user_db_response['name'],
                'email': totvs_user_db_response['email']
            },
            response.json()
        )
