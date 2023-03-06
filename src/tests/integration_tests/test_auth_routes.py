from unittest.mock import patch
from jose import jwt
import json

from src.db.cruds.user_crud import UserCRUD
from src.dependencies.totvs.soap_api import TotvsWebServer
from src.db.models.user_model import UserModel
from src.schemas.user_schema import UserResponse, UserMe
from src.tests.mocks.auth_mocks import (
    valid_login,
    login_incorrect_username,
    login_incorrect_password
)
from src.tests.mocks.user_mocks import valid_user_id
from src.tests.mocks.user_mocks import user_db_response, totvs_user_db_response
from src.tests.settings import ApiBaseTestCase


class AuthRouteTestClass(ApiBaseTestCase):
    @patch('src.controllers.auth_controller.verify_password', return_value=True)
    @patch.object(
        UserCRUD,
        'get_user_by_username_or_email',
        return_value=UserModel(**user_db_response)
    )
    def test_create_token_non_totvs(self, *_):
        '''
        Should return token and status 201 when logging in as non totvs user
        '''
        response = self.client.post('/auth/token', json=valid_login)
        self.assertEqual(201, response.status_code)
        self.assertIsNotNone(response.json()['access_token'])

        user_response = response.json()['user']
        expected_user = user_db_response
        expected_user.update(document='547******03')
        expected_user_dict = json.loads(UserMe(**expected_user).json())

        for key, value in user_response.items():
            self.assertEqual(value, expected_user_dict[key])

    @patch.object(TotvsWebServer, 'get_auth_totvs', return_value=True)
    @patch.object(
        UserCRUD,
        'get_user_by_username_or_email',
        return_value=UserModel(**totvs_user_db_response)
    )
    @patch.object(UserCRUD, 'patch')
    def test_create_token_totvs_user(self, patch_mock, *_):
        '''
        Should return token and status 201 when logging in as totvs user
        '''
        response = self.client.post('/auth/token', json=valid_login)
        self.assertEqual(201, response.status_code)
        self.assertIsNotNone(response.json()['access_token'])
        patch_mock.assert_called()

        user_response = response.json()['user']
        expected_user = totvs_user_db_response
        expected_user.update(document='389******76')
        expected_user_dict = json.loads(UserMe(**expected_user).json())

        for key, value in user_response.items():
            self.assertEqual(value, expected_user_dict[key])

    def test_create_token_with_incorrect_document(self):
        '''
        Should return error message and status 400 when incorrect document
        '''
        response = self.client.post('/auth/token', json=login_incorrect_username)
        self.assertEqual(400, response.status_code)
        self.assertEqual({'detail': 'Usuário ou senha inválidos.'}, response.json())

    @patch('src.controllers.auth_controller.verify_password', return_value=False)
    @patch.object(
        UserCRUD,
        'get_user_by_username_or_email',
        return_value=UserModel(**user_db_response)
    )
    def test_create_token_with_incorrect_password_non_totvs_user(self, *_):
        '''
        Should return error message and status 400 when trying to login in
        as non totvs user with invalid password
        '''
        response = self.client.post('/auth/token', json=login_incorrect_password)
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            {'detail': 'Usuário ou senha inválidos.'},
            response.json()
        )

    @patch('src.dependencies.totvs.soap_api.post')
    @patch.object(
        UserCRUD,
        'get_user_by_username_or_email',
        return_value=UserModel(**totvs_user_db_response)
    )
    def test_create_token_with_incorrect_password_totvs_user(self, *_):
        '''
        Should return error message and status 400 when trying to login in
        as totvs user with invalid password
        '''
        response = self.client.post('/auth/token', json=login_incorrect_password)
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            {'detail': 'Usuário ou senha inválidos.'},
            response.json()
        )

    def test_handle_me_data_with_invalid_token(self):
        '''
        Should return error message and status 401 when invalid token
        '''
        response = self.client.get(
            '/auth/me',
            headers={'Authorization': 'Bearer invalid_token'}
        )
        self.assertEqual(401, response.status_code)
        self.assertEqual(self.invalid_token_msg, response.json())

    @patch.object(jwt, 'decode', return_value={'sub': valid_user_id})
    def test_handle_me_data_with_valid_token_but_no_user_match(self, mock):
        '''
        Should return error message and status 401
        when valid token but no user match
        '''
        response = self.client.get(
            '/auth/me',
            headers={'Authorization': 'Bearer valid_token'}
        )
        self.assertEqual(401, response.status_code)
        self.assertEqual(self.invalid_token_msg, response.json())

    @patch.object(UserCRUD, 'get', return_value=UserModel(**user_db_response))
    @patch.object(jwt, 'decode', return_value={'sub': valid_user_id})
    def test_handle_me_data_with_valid_token_and_user_match(self, *_):
        '''
        Should return user data and status 200
        when valid token and matching user_id
        '''
        response = self.client.get(
            '/auth/me',
            headers={'Authorization': 'Bearer valid_token'}
        )
        self.assertEqual(200, response.status_code)

        body = response.json()

        for key, value in user_db_response.items():
            if key != 'password':
                self.assertEqual(value, body[key])
            else:
                self.assertTrue(key not in body)

    @patch.object(jwt, 'decode', return_value={'sub': valid_user_id})
    @patch.object(UserCRUD, 'get', return_value=UserModel(**user_db_response))
    def test_handle_sso_totvs_as_non_totvs_user(self, *_):
        '''
        Should return sso totvs data and status 200 with all fields None
        '''
        response = self.client.get(
            '/auth/sso/totvs',
            headers={'Authorization': 'Bearer valid_token'}
        )
        self.assertEqual(200, response.status_code)
        body = response.json()
        for key in body:
            self.assertEqual(body[key], None)

    @patch('src.controllers.auth_controller.decode_password', return_value='key_totvs')
    @patch.object(jwt, 'decode', return_value={'sub': valid_user_id})
    @patch.object(
        UserCRUD,
        'get',
        side_effect=[
            UserResponse(**totvs_user_db_response),
            UserModel(**totvs_user_db_response)
        ]
    )
    def test_handle_sso_totvs_as_totvs_user(self, *_):
        '''
        Should return sso totvs data and status 200
        '''
        response = self.client.get(
            '/auth/sso/totvs',
            headers={'Authorization': 'Bearer valid_token'}
        )
        self.assertEqual(200, response.status_code)
        body = response.json()
        self.assertEqual(body['user_name'], 'totvs_user')
        self.assertEqual(body['key_totvs'], 'key_totvs')
