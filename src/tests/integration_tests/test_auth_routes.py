from unittest.mock import patch
from jose import jwt

from src.db.cruds.user_crud import UserCRUD
from src.dependencies.totvs.soap_api import TotvsWebServer
from src.db.models.user_model import UserModel
from src.schemas.user_schema import UserResponse
from src.tests.mocks.auth_mocks import (
    valid_login,
    login_incorrect_document,
    login_incorrect_password
)
from src.tests.mocks.user_mocks import valid_user_id
from src.tests.mocks.user_mocks import user_db_response, totvs_user_db_response
from src.tests.settings import ApiBaseTestCase


class AuthRouteTestClass(ApiBaseTestCase):
    @patch('src.controllers.auth_controller.verify_password', return_value=True)
    @patch.object(
        UserCRUD,
        'get_user_document_or_email',
        return_value=UserModel(**user_db_response)
    )
    def test_create_token_non_totvs(self, UserCRUD_mock, verify_mock):
        '''
        Should return token and status 201 when logging in as non totvs user
        '''
        response = self.client.post('/auth/token', json=valid_login)
        self.assertEqual(201, response.status_code)
        self.assertIsNotNone(response.json()['access_token'])

    @patch.object(TotvsWebServer, 'get_auth_totvs', return_value=True)
    @patch.object(UserCRUD, 'patch')
    @patch.object(
        UserCRUD,
        'get_user_document_or_email',
        return_value=UserModel(**totvs_user_db_response)
    )
    def test_create_token_totvs_user(self, get_mock, patch_mock, totvs_auth_mock):
        '''
        Should return token and status 201 when logging in as totvs user
        '''
        response = self.client.post('/auth/token', json=valid_login)
        self.assertEqual(201, response.status_code)
        self.assertIsNotNone(response.json()['access_token'])
        self.assertTrue(patch_mock.called)

    def test_create_token_with_incorrect_document(self):
        '''
        Should return error message and status 400 when incorrect document
        '''
        response = self.client.post('/auth/token', json=login_incorrect_document)
        self.assertEqual(400, response.status_code)
        self.assertEqual({'detail': 'Documento ou senha inválidos.'}, response.json())

    @patch('src.controllers.auth_controller.verify_password', return_value=False)
    @patch.object(
        UserCRUD,
        'get_user_document_or_email',
        return_value=UserModel(**user_db_response)
    )
    def test_create_token_with_incorrect_password_non_totvs_user(self, UserCRUD_mock, verify_mock):
        '''
        Should return error message and status 400 when trying to login in as non totvs user with invalid password
        '''
        response = self.client.post('/auth/token', json=login_incorrect_password)
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            {'detail': 'Documento ou senha inválidos.'},
            response.json()
        )

    @patch('src.dependencies.totvs.soap_api.post')
    @patch.object(
        UserCRUD,
        'get_user_document_or_email',
        return_value=UserModel(**totvs_user_db_response)
    )
    def test_create_token_with_incorrect_password_totvs_user(self, get_mock, totvs_post_mock):
        '''
        Should return error message and status 400 when trying to login in as totvs user with invalid password
        '''
        response = self.client.post('/auth/token', json=login_incorrect_password)
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            {'detail': 'Documento ou senha inválidos.'},
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

    @patch.object(UserCRUD, 'get', return_value=UserResponse(**user_db_response))
    @patch.object(jwt, 'decode', return_value={'sub': valid_user_id})
    def test_handle_me_data_with_valid_token_and_user_match(
        self,
        jwt_verify_mock,
        UserCRUD_mock
    ):
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
