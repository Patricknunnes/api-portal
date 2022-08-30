from unittest.mock import MagicMock, patch

from src.exceptions.exceptions import NotFoundException
from src.exceptions.exceptions import BadRequestException
from src.controllers.user_controller import UserController
from src.controllers.role_controller import RoleController
from src.db.cruds.role_crud import RoleCRUD
from src.db.cruds.user_crud import UserCRUD
from src.schemas.user_schema import UserBase, UserUpdate
from src.tests.mocks.user_mocks import (
    user_create_data,
    invalid_phone,
    invalid_document,
    user_db_response,
    invalid_user_create_data,
    user_create_data_no_phone,
    user_db_response_no_phone,
    invalid_user_id,
    valid_user_id,
    user_update_data
)
from src.tests.mocks.role_mocks import invalid_role_id
from src.tests.settings import BaseTestCase


class UserControllerTestClass(BaseTestCase):
    @patch.object(RoleCRUD, 'get', return_value=None)
    def test_handle_create_when_role_id_not_found(self, mock):
        '''
          Should raise exception when role id not found
        '''
        user_info_with_invalid_role_id = {**user_create_data, 'role_id': invalid_role_id}

        with self.assertRaises(NotFoundException) as error:
            UserController().handle_create(
                db=self.session,
                data=UserBase(**user_info_with_invalid_role_id)
            )

        exception = error.exception
        self.assertEqual('Role não encontrada.', exception.detail)

    @patch.object(RoleController, 'handle_get', return_value=None)
    def test_handle_create_when_invalid_phone(self, mock):
        '''
          Should raise exception when invalid phone
        '''
        user_info_with_invalid_phone = {**user_create_data, 'phone': invalid_phone}

        with self.assertRaises(BadRequestException) as error:
            UserController().handle_create(
                db=self.session,
                data=UserBase(**user_info_with_invalid_phone)
            )

        exception = error.exception
        self.assertEqual('Telefone invalido.', exception.detail)

    @patch.object(RoleController, 'handle_get', return_value=None)
    def test_handle_create_when_invalid_document(self, mock):
        '''
          Should raise exception when invalid document
        '''
        user_info_with_invalid_document = {
            **user_create_data,
            'document': invalid_document
        }

        with self.assertRaises(BadRequestException) as error:
            UserController().handle_create(
                db=self.session,
                data=UserBase(**user_info_with_invalid_document)
            )

        exception = error.exception
        self.assertEqual('Documento invalido.', exception.detail)

    @patch.object(UserCRUD, 'get_user_document_or_email', return_value=user_db_response)
    @patch.object(RoleController, 'handle_get', return_value=None)
    def test_handle_create_when_document_or_email_in_use(
        self,
        RoleController_mock,
        UserCRUD_mock
    ):
        '''
          Should raise exception when document or email already in use
        '''
        with self.assertRaises(BadRequestException) as error:
            UserController().handle_create(
                db=self.session,
                data=UserBase(**user_create_data)
            )

        exception = error.exception
        self.assertEqual('Documento ou Email já cadastrado.', exception.detail)

    @patch.object(RoleController, 'handle_get', return_value=None)
    def test_handle_create_when_fields_missing(self, RoleController_mock):
        '''
          Should raise exception when required fields are missing
        '''
        with self.assertRaises(BadRequestException) as error:
            UserController().handle_create(
                db=self.session,
                data=UserBase(**invalid_user_create_data)
            )

        exception = error.exception
        self.assertEqual('Campos obrigatorios: (name, password) .', exception.detail)

    @patch.object(UserCRUD, 'create', return_value=user_db_response)
    @patch.object(RoleController, 'handle_get', return_value=None)
    def test_handle_create_when_valid_user_data(self, RoleController_mock, UserCRUD_mock):
        '''
          Should return created user when valid user data
        '''
        result = UserController().handle_create(
            db=self.session,
            data=UserBase(**user_create_data)
        )
        self.assertEqual(user_db_response, result)

    @patch.object(UserCRUD, 'create', return_value=user_db_response_no_phone)
    @patch.object(RoleController, 'handle_get', return_value=None)
    def test_handle_create_when_valid_user_data_but_no_phone(
        self,
        RoleController_mock,
        UserCRUD_mock
    ):
        '''
          Should return created user when valid user data without phone
        '''
        result = UserController().handle_create(
            db=self.session,
            data=UserBase(**user_create_data_no_phone)
        )
        self.assertEqual(user_db_response_no_phone, result)

    def test_handle_patch_when_user_id_not_found(self):
        '''
          Should raise exception when user id not found
        '''
        with self.assertRaises(NotFoundException) as error:
            UserController().handle_patch(
                db=self.session,
                object_id=invalid_user_id,
                data=UserUpdate(),
            )

        exception = error.exception
        self.assertEqual('Usuário não encontrado.', exception.detail)

    @patch.multiple(
        UserCRUD,
        get=MagicMock(return_value=user_db_response),
        patch=MagicMock(return_value=None)
    )
    @patch.object(RoleController, 'handle_get', return_value=None)
    def test_handle_patch_when_all_possible_fields_change(
        self,
        RoleController_mock,
        **UserCRUD_mocks
    ):
        '''
          Should return None when valid user id and change all fields
        '''
        result = UserController().handle_patch(
            db=self.session,
            object_id=valid_user_id,
            data=UserUpdate(**user_update_data),
        )

        self.assertIsNone(result)

    @patch.multiple(
        UserCRUD,
        get=MagicMock(return_value=user_db_response),
        patch=MagicMock(return_value=None)
    )
    def test_handle_patch_when_no_data_change(
        self,
        **mocks
    ):
        '''
          Should return None when valid user id and no data to patch
        '''
        result = UserController().handle_patch(
            db=self.session,
            object_id=valid_user_id,
            data=UserUpdate(),
        )

        self.assertIsNone(result)