from unittest.mock import patch

from src.db.cruds.user_crud import UserCRUD
from src.dependencies.totvs.soap_api import TotvsWebServer
from src.db.models.user_model import UserModel
from src.exceptions.exceptions import BadRequestException
from src.schemas.auth_schema import LoginBase, ResponseSsoTotvs, TokenResponse
from src.schemas.user_schema import UserResponse
from src.controllers.auth_controller import AuthController
from src.tests.settings import BaseTestCase
from src.tests.mocks.auth_mocks import (
    login_incorrect_username,
    login_incorrect_password,
    valid_login
)
from src.tests.mocks.user_mocks import user_db_response, totvs_user_db_response


class AuthControllerTestClass(BaseTestCase):
    def test_handle_login_with_invalid_username(self):
        '''
          Should raise exception when user is not found by username
        '''
        with self.assertRaises(BadRequestException) as error:
            AuthController().handle_login(
                db=self.session,
                data_login=LoginBase(**login_incorrect_username)
            )
        exception = error.exception
        self.assertEqual(
            'Usuário ou senha inválidos.',
            exception.detail
        )

    @patch('src.controllers.auth_controller.verify_password', return_value=False)
    @patch.object(
        UserCRUD,
        'get_user_by_username_or_email',
        return_value=UserModel(**user_db_response)
    )
    def test_handle_login_with_invalid_password(
        self,
        UserCRUD_mock,
        verify_mock
    ):
        '''
          Should raise exception when invalid password
        '''
        with self.assertRaises(BadRequestException) as error:
            AuthController().handle_login(
                db=self.session,
                data_login=LoginBase(**login_incorrect_password)
            )
        exception = error.exception
        self.assertEqual(
            'Usuário ou senha inválidos.',
            exception.detail
        )

    @patch('src.controllers.auth_controller.verify_password', return_value=True)
    @patch.object(
        UserCRUD,
        'get_user_by_username_or_email',
        return_value=UserModel(**user_db_response)
    )
    def test_handle_login_with_valid_non_totvs_user(self, UserCRUD_mock, verify_mock):
        '''
        Should return a TokenResponse instance
        '''
        result = AuthController().handle_login(
            db=self.session,
            data_login=LoginBase(**valid_login)
        )
        self.assertTrue(isinstance(result, TokenResponse))

    @patch.object(UserCRUD, 'patch')
    @patch.object(
        UserCRUD,
        'get_user_by_username_or_email',
        return_value=UserModel(**totvs_user_db_response)
    )
    @patch.object(TotvsWebServer, 'get_auth_totvs', return_value=True)
    def test_handle_login_with_totvs_user(
        self,
        get_totvs_mock,
        get_user_mock,
        patch_mock
    ):
        '''
        Should return a TokenResponse instance and patch the password hash in db
        '''
        result = AuthController().handle_login(
            db=self.session,
            data_login=LoginBase(**valid_login)
        )
        self.assertTrue(isinstance(result, TokenResponse))
        self.assertTrue(patch_mock.called)

    @patch.object(
        UserCRUD,
        'get_user_by_username_or_email',
        return_value=UserModel(**totvs_user_db_response)
    )
    @patch('src.dependencies.totvs.soap_api.post')
    def test_handle_login_with_totvs_user_invalid_pass(
        self,
        totvs_auth_mock,
        get_user_mock
    ):
        '''
          Should raise exception when invalid password
        '''
        with self.assertRaises(BadRequestException) as error:
            AuthController().handle_login(
                db=self.session,
                data_login=LoginBase(**login_incorrect_password)
            )
        exception = error.exception
        self.assertEqual(
            'Usuário ou senha inválidos.',
            exception.detail
        )

    @patch.object(
        UserCRUD,
        'get',
        return_value=UserModel(**user_db_response)
    )
    def test_handle_sso_totvs_with_non_totvs_user(self, get_mock):
        '''
        Should return ResponseSsoTotvs instance with all fields values as None
        '''
        result = AuthController().handle_sso_totvs(
            db=self.session,
            profile=UserResponse(**user_db_response)
        )
        self.assertTrue(isinstance(result, ResponseSsoTotvs))
        self.assertEqual(result.user_name, None)
        self.assertEqual(result.key_totvs, None)

    @patch('src.controllers.auth_controller.decode_password', return_value='key_totvs')
    @patch.object(
        UserCRUD,
        'get',
        return_value=UserModel(**totvs_user_db_response)
    )
    def test_handle_sso_totvs_with_totvs_user(self, get_mock, decode_mock):
        '''
        Should return ResponseSsoTotvs instance with username and key_totvs
        '''
        result = AuthController().handle_sso_totvs(
            db=self.session,
            profile=UserResponse(**totvs_user_db_response)
        )
        self.assertTrue(isinstance(result, ResponseSsoTotvs))
        self.assertEqual(result.user_name, totvs_user_db_response['username'])
        self.assertEqual(result.key_totvs, 'key_totvs')
