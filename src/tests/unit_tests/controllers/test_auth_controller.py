from datetime import datetime, timedelta
from unittest.mock import patch
from uuid import uuid4

from src.db.cruds.user_crud import UserCRUD
from src.db.cruds.token_crud import TokenCRUD
from src.dependencies.totvs.soap_api import TotvsWebServer
from src.db.models.models import UserModel, TokenModel
from src.exceptions.exceptions import (
    BadRequestException,
    NotFoundException,
    UnAuthorizedException
)
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
    def test_handle_login_with_invalid_password(self, *_):
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
    @patch.object(
        TokenCRUD,
        'create',
        return_value=TokenModel(id=uuid4())
    )
    @patch.object(TotvsWebServer, 'get_auth_totvs')
    def test_handle_login_with_valid_non_totvs_user(
        self,
        totvs_mock,
        create_session_mock,
        *_
    ):
        '''
        Should return a TokenResponse instance without trying to log in with TOTVS
        '''
        result = AuthController().handle_login(
            db=self.session,
            data_login=LoginBase(**valid_login)
        )
        totvs_mock.assert_not_called()
        create_session_mock.assert_called()
        self.assertTrue(isinstance(result, TokenResponse))

    @patch.object(
        UserCRUD,
        'get_user_by_username_or_email',
        return_value=UserModel(**totvs_user_db_response)
    )
    @patch.object(
        TokenCRUD,
        'create',
        return_value=TokenModel(id=uuid4())
    )
    @patch.object(TotvsWebServer, 'get_auth_totvs', return_value=True)
    @patch.object(UserCRUD, 'patch')
    def test_handle_login_with_totvs_user(
        self,
        patch_mock,
        totvs_mock,
        create_session_mock,
        *_
    ):
        '''
        Should log in with TOTVS, return a TokenResponse instance and
        patch the password hash in db
        '''
        result = AuthController().handle_login(
            db=self.session,
            data_login=LoginBase(**valid_login)
        )
        self.assertTrue(isinstance(result, TokenResponse))
        patch_mock.assert_called()
        totvs_mock.assert_called()
        create_session_mock.assert_called()

    @patch.object(
        UserCRUD,
        'get_user_by_username_or_email',
        return_value=UserModel(**totvs_user_db_response)
    )
    @patch('src.dependencies.totvs.soap_api.post')
    def test_handle_login_with_totvs_user_invalid_pass(self, *_):
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
    def test_handle_sso_totvs_with_non_totvs_user(self, _):
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
    def test_handle_sso_totvs_with_totvs_user(self, *_):
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

    @patch(
        'src.controllers.auth_controller.decode_password',
        return_value='valid_refresh_token')
    @patch.object(TokenCRUD, 'get', return_value=TokenModel(
        expiration_date=datetime.utcnow() + timedelta(days=1)))
    @patch.object(TokenCRUD, 'patch')
    def test_handle_refresh_token_successfully(self, patch_session_mock, *_):
        '''
        Should return a dict with the new access_token and the new refresh_token
        '''
        result = AuthController().handle_refresh_token(
            db=self.session, session_id=uuid4(), refresh_token='valid_refresh_token')

        self.assertIsNotNone(result['access_token'])
        self.assertIsNotNone(result['refresh_token'])

        patch_session_mock.assert_called()

    def test_handle_refresh_token_with_not_found_session(self):
        '''
        Should raise an error
        '''

        with self.assertRaises(NotFoundException) as error:
            AuthController().handle_refresh_token(
                db=self.session, session_id=uuid4(), refresh_token='valid_refresh_token')
        exception = error.exception
        self.assertEqual('Sessão não encontrada.', exception.detail)

    @patch(
        'src.controllers.auth_controller.decode_password',
        return_value='valid_refresh_token'
    )
    @patch.object(TokenCRUD, 'get', return_value=TokenModel(
        expiration_date=datetime.utcnow() + timedelta(days=1)))
    @patch.object(TokenCRUD, 'delete')
    def test_handle_refresh_token_with_invalid_refresh_token(
        self,
        delete_session_mock,
        *_
    ):
        '''
        Should raise an error
        '''

        with self.assertRaises(UnAuthorizedException) as error:
            AuthController().handle_refresh_token(
                db=self.session, session_id=uuid4(), refresh_token='invalid_token')
        exception = error.exception
        self.assertEqual('Token de atualização inválido.', exception.detail)
        delete_session_mock.assert_called()

    @patch(
        'src.controllers.auth_controller.decode_password',
        return_value='valid_refresh_token'
    )
    @patch.object(TokenCRUD, 'get', return_value=TokenModel(
        expiration_date=datetime.utcnow() - timedelta(days=1)))
    @patch.object(TokenCRUD, 'delete')
    def test_handle_refresh_token_with_expired_refresh_token(
        self,
        delete_session_mock,
        *_
    ):
        '''
        Should raise an error
        '''

        with self.assertRaises(UnAuthorizedException) as error:
            AuthController().handle_refresh_token(
                db=self.session, session_id=uuid4(), refresh_token='valid_refresh_token')
        exception = error.exception
        self.assertEqual('Token de atualização inválido.', exception.detail)
        delete_session_mock.assert_called()
