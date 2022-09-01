from unittest.mock import patch

from src.db.cruds.user_crud import UserCRUD
from src.shared.auth.hash_provider import pwd_context
from src.db.models.user_model import UserModel
from src.exceptions.exceptions import BadRequestException
from src.schemas.auth_schema import LoginBase, TokenResponse
from src.controllers.auth_controller import AuthController
from src.tests.settings import BaseTestCase
from src.tests.mocks.auth_mocks import (
    login_incorrect_document,
    login_incorrect_password
)
from src.tests.mocks.user_mocks import user_db_response


class AuthControllerTestClass(BaseTestCase):
    def test_handle_login_with_invalid_document(self):
        '''
          Should raise exception when user not found by document
        '''
        with self.assertRaises(BadRequestException) as error:
            AuthController().handle_login(
                db=self.session,
                data_login=LoginBase(**login_incorrect_document)
            )
        exception = error.exception
        self.assertEqual(
            'Documento ou senha inválidos.',
            exception.detail
        )

    @patch.object(pwd_context, 'verify', return_value=False)
    @patch.object(
        UserCRUD,
        'get_user_document_or_email',
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
            'Documento ou senha inválidos.',
            exception.detail
        )

    @patch.object(pwd_context, 'verify', return_value=True)
    @patch.object(
        UserCRUD,
        'get_user_document_or_email',
        return_value=UserModel(**user_db_response)
    )
    def test_handle_login_with_valid_data(self, UserCRUD_mock, verify_mock):
        '''
          Should return a TokenResponse instance
        '''
        result = AuthController().handle_login(
            db=self.session,
            data_login=LoginBase(**login_incorrect_password)
        )
        self.assertTrue(isinstance(result, TokenResponse))
