from unittest.mock import patch
from jose import jwt

from src.db.cruds.user_crud import UserCRUD
from src.db.models.user_model import UserModel
from src.shared.auth.hash_provider import pwd_context
from src.tests.mocks.auth_mocks import valid_login, login_incorrect_email, login_incorrect_password
from src.tests.mocks.user_mocks import valid_user_id
from src.tests.mocks.user_mocks import user_db_response
from src.tests.settings import ApiBaseTestCase


class AuthRouteTestClass(ApiBaseTestCase):
    @patch.object(pwd_context, 'verify', return_value=True)
    @patch.object(
        UserCRUD,
        'get_user_document_or_email',
        return_value=UserModel(**user_db_response)
    )
    def test_create_token(self, UserCRUD_mock, verify_mock):
        '''
        Test return of token with status 201 when sending correct body on request
        '''
        response = self.client.post('/auth/token', json=valid_login)
        self.assertEqual(201, response.status_code)
        self.assertIsNotNone(response.json()['access_token'])

    def test_create_token_with_incorrect_email(self):
        '''
        Test return of error message with status 400 when incorrect email
        '''
        response = self.client.post('/auth/token', json=login_incorrect_email)
        self.assertEqual(400, response.status_code)
        self.assertEqual({'detail': 'Email ou senha invalidos.'}, response.json())

    @patch.object(pwd_context, 'verify', return_value=False)
    @patch.object(
        UserCRUD,
        'get_user_document_or_email',
        return_value=UserModel(**user_db_response)
    )
    def test_create_token_with_incorrect_password(self, UserCRUD_mock, verify_mock):
        '''
        Test return of error message with status 400 when incorrect password
        '''
        response = self.client.post('/auth/token', json=login_incorrect_password)
        self.assertEqual(400, response.status_code)
        self.assertEqual({'detail': 'Email ou senha invalidos.'}, response.json())


    def test_handle_me_data_with_invalid_token(self):
        '''
        Test return of error message with status 401 when invalid token
        '''
        response = self.client.get('/auth/me', headers={'Authorization': 'Bearer invalid_token'})
        self.assertEqual(401, response.status_code)
        self.assertEqual({'detail': 'Token invalido.'}, response.json())

    @patch.object(jwt, 'decode', return_value={'sub':valid_user_id})
    def test_handle_me_data_with_valid_token_but_no_user_match(self, mock):
        '''
        Test return of error message with status 401 when valid token but no user match
        '''
        response = self.client.get('/auth/me', headers={'Authorization': 'Bearer valid_token'})
        self.assertEqual(401, response.status_code)
        self.assertEqual({'detail': 'Token invalido.'}, response.json())

    @patch.object(UserCRUD, 'get', return_value=user_db_response)
    @patch.object(jwt, 'decode', return_value={'sub':valid_user_id})
    def test_handle_me_data_with_valid_token_but_no_user_match(self, jwt_verify_mock, UserCRUD_mock):
        '''
        Test return of user data with status 200 when valid token and matching user_id
        '''
        response = self.client.get('/auth/me', headers={'Authorization': 'Bearer valid_token'})
        self.assertEqual(200, response.status_code)

        body = response.json()

        for key, value in user_db_response.items():
            if key != 'password':
                self.assertEqual(value, body[key])
            else:
                self.assertTrue(key not in body)
