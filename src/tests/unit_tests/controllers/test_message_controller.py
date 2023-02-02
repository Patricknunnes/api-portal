from unittest.mock import patch
from datetime import datetime

from src.tests.settings import BaseTestCase
from src.tests.mocks.message_mocks import (
    message_with_all_fields,
    message_with_expiration_date,
    message_with_invalid_format_date,
    message_with_invalid_string_as_date,
    message_with_max_length_title,
    message_with_role_permission,
    message_with_too_long_title,
    message_with_user_permission,
    message,
    uuid_test
)
from src.tests.mocks.role_mocks import roles
from src.tests.mocks.user_mocks import user_db_response

from src.controllers.message_controller import MessageController
from src.db.cruds.message_crud import MessageCRUD
from src.db.cruds.role_crud import RoleCRUD
from src.db.cruds.user_crud import UserCRUD
from src.exceptions.exceptions import BadRequestException, NotFoundException
from src.schemas.message_schema import MessageCreate, MessageUpdate
from src.schemas.user_schema import UserResponse


class MessageControllerTestClass(BaseTestCase):
    def test_handle_list(self):
        '''
          Should return list with all messages
        '''
        result = MessageController().handle_list(db=self.session)

        self.assertEqual(result, {'page': 1, 'total': 0, 'results': []})

    def test_handle_create_with_invalid_string_as_expiration_date(self):
        '''
        Trying to create a message with a invalid string as
        expiration_date must raise an error
        '''
        with self.assertRaises(BadRequestException) as error:
            MessageController().handle_create(
                db=self.session,
                data=MessageCreate(**message_with_invalid_string_as_date)
            )
        exception = error.exception
        self.assertEqual(
            'Data de expiração inválida. Siga o formato YYYY-MM-DD.',
            exception.detail
        )

    def test_handle_create_with_invalid_date_format(self):
        '''
        Trying to create a message with a invalid format for
        expiration_date must raise an error
        '''
        with self.assertRaises(BadRequestException) as error:
            MessageController().handle_create(
                db=self.session,
                data=MessageCreate(**message_with_invalid_format_date)
            )
        exception = error.exception
        self.assertEqual(
            'Data de expiração inválida. Siga o formato YYYY-MM-DD.',
            exception.detail
        )

    @patch('src.controllers.message_controller.datetime', wraps=datetime)
    def test_handle_create_with_day_past(self, datetime_mock):
        '''
        Trying to create a message with a date past as expiration_date must raise an error
        '''
        with self.assertRaises(BadRequestException) as error:
            datetime_mock.now.return_value = datetime.strptime('2100-01-01', '%Y-%m-%d')
            MessageController().handle_create(
                db=self.session,
                data=MessageCreate(**message_with_expiration_date)
            )
        exception = error.exception
        self.assertEqual(
            'A data de expiração deve ser uma data futura.',
            exception.detail
        )

    @patch.object(RoleCRUD, 'get', return_value=None)
    def test_handle_create_with_not_found_role(self, _):
        '''
        Trying to create a message with an invalid role_id must raise an error
        '''
        with self.assertRaises(NotFoundException) as error:
            MessageController().handle_create(
                db=self.session,
                data=MessageCreate(**message_with_role_permission)
            )
        exception = error.exception
        self.assertEqual(
            'Cargo não encontrado.',
            exception.detail
        )

    @patch.object(UserCRUD, 'get', return_value=None)
    def test_handle_create_with_not_found_user(self, _):
        '''
        Trying to create a message with an invalid user_id must raise an error
        '''
        with self.assertRaises(NotFoundException) as error:
            MessageController().handle_create(
                db=self.session,
                data=MessageCreate(**message_with_user_permission)
            )
        exception = error.exception
        self.assertEqual(
            'Usuário não encontrado.',
            exception.detail
        )

    @patch.object(MessageCRUD, 'create')
    def test_handle_create_without_optional_fields(self, create_mock):
        '''
        Trying to create a message without the optional fields
        will call MessageCRUD.create
        '''
        MessageController().handle_create(
            db=self.session,
            data=MessageCreate(**message)
        )
        create_mock.assert_called()

    def test_handle_create_with_too_long_title(self):
        '''
        Trying to create a message with title longer than 50 characters
        must raise an error
        '''
        with self.assertRaises(BadRequestException) as error:
            MessageController().handle_create(
                db=self.session,
                data=MessageCreate(
                    title=message_with_too_long_title['title'],
                    text='any text',
                    created_by=uuid_test
                )
            )
        exception = error.exception
        self.assertEqual(
            'O título pode ter no máximo 50 caracteres.',
            exception.detail
        )

    @patch.object(MessageCRUD, 'create')
    def test_handle_create_with_max_length_title(self, create_mock):
        '''
        Trying to create a message with title 50-characters long
        will call MessageCRUD.create
        '''
        MessageController().handle_create(
            db=self.session,
            data=MessageCreate(
                title=message_with_max_length_title['title'],
                text='any text',
                created_by=uuid_test
            )
        )
        create_mock.assert_called()

    @patch.object(RoleCRUD, 'get', return_value=roles[0])
    @patch.object(UserCRUD, 'get', return_value=user_db_response)
    @patch('src.controllers.message_controller.datetime', wraps=datetime)
    @patch.object(MessageCRUD, 'create')
    def test_handle_create_with_all_fields(self, create_mock, datetime_mock, *_):
        '''
        Trying to create a message with all the optional fields
        will call MessageCRUD.create
        '''
        datetime_mock.now.return_value = datetime.strptime('2000-01-01', '%Y-%m-%d')
        MessageController().handle_create(
            db=self.session,
            data=MessageCreate(**message_with_all_fields)
        )
        create_mock.assert_called()

    def test_handle_patch_with_invalid_string_as_expiration_date(self):
        '''
        Trying to patch a message with a invalid string as
        expiration_date must raise an error
        '''
        with self.assertRaises(BadRequestException) as error:
            MessageController().handle_patch(
                db=self.session,
                data=MessageUpdate(**message_with_invalid_string_as_date),
                object_id=uuid_test
            )
        exception = error.exception
        self.assertEqual(
            'Data de expiração inválida. Siga o formato YYYY-MM-DD.',
            exception.detail
        )

    def test_handle_patch_with_invalid_date_format(self):
        '''
        Trying to patch a message with a invalid format for
        expiration_date must raise an error
        '''
        with self.assertRaises(BadRequestException) as error:
            MessageController().handle_patch(
                db=self.session,
                data=MessageUpdate(**message_with_invalid_format_date),
                object_id=uuid_test
            )
        exception = error.exception
        self.assertEqual(
            'Data de expiração inválida. Siga o formato YYYY-MM-DD.',
            exception.detail
        )

    @patch('src.controllers.message_controller.datetime', wraps=datetime)
    def test_handle_patch_with_day_past(self, datetime_mock):
        '''
        Trying to patch a message with a date past as expiration_date must raise an error
        '''
        with self.assertRaises(BadRequestException) as error:
            datetime_mock.now.return_value = datetime.strptime('2100-01-01', '%Y-%m-%d')
            MessageController().handle_patch(
                db=self.session,
                data=MessageUpdate(**message_with_expiration_date),
                object_id=uuid_test
            )
        exception = error.exception
        self.assertEqual(
            'A data de expiração deve ser uma data futura.',
            exception.detail
        )

    @patch.object(RoleCRUD, 'get', return_value=None)
    def test_handle_patch_with_not_found_role(self, _):
        '''
        Trying to patch a message with an invalid role_id must raise an error
        '''
        with self.assertRaises(NotFoundException) as error:
            MessageController().handle_patch(
                db=self.session,
                data=MessageUpdate(**message_with_role_permission),
                object_id=uuid_test
            )
        exception = error.exception
        self.assertEqual(
            'Cargo não encontrado.',
            exception.detail
        )

    @patch.object(UserCRUD, 'get', return_value=None)
    def test_handle_patch_with_not_found_user(self, _):
        '''
        Trying to patch a message with an invalid user_id must raise an error
        '''
        with self.assertRaises(NotFoundException) as error:
            MessageController().handle_patch(
                db=self.session,
                data=MessageUpdate(**message_with_user_permission),
                object_id=uuid_test
            )
        exception = error.exception
        self.assertEqual(
            'Usuário não encontrado.',
            exception.detail
        )

    def test_handle_patch_with_invalid_id(self):
        '''
        Trying to patch a message with an invalid id must raise an error
        '''
        with self.assertRaises(NotFoundException) as error:
            MessageController().handle_patch(
                db=self.session,
                data=MessageUpdate(title='new title', updated_by=uuid_test),
                object_id=uuid_test
            )
        exception = error.exception
        self.assertEqual(
            'Mensagem não encontrada',
            exception.detail
        )

    @patch.object(RoleCRUD, 'get', return_value=roles[0])
    @patch.object(MessageCRUD, 'get', return_value=message)
    @patch.object(MessageCRUD, 'patch', return_value=None)
    def test_handle_patch_without_title_and_text(self, patch_mock, *_):
        '''
        Trying to patch a message without title and text will call MessageCRUD.patch
        '''
        MessageController().handle_patch(
            db=self.session,
            data=MessageUpdate(role_permission=uuid_test, updated_by=uuid_test),
            object_id=uuid_test
        )
        patch_mock.assert_called()

    @patch.object(RoleCRUD, 'get', return_value=roles[0])
    @patch.object(UserCRUD, 'get', return_value=user_db_response)
    @patch.object(MessageCRUD, 'get', return_value=message)
    @patch('src.controllers.message_controller.datetime', wraps=datetime)
    @patch.object(MessageCRUD, 'patch')
    def test_handle_patch_with_all_fields(self, patch_mock, datetime_mock, *_):
        '''
        Trying to patch a message with all fields, will call MessageCRUD.patch
        '''
        datetime_mock.now.return_value = datetime.strptime('2000-01-01', '%Y-%m-%d')
        MessageController().handle_patch(
            db=self.session,
            data=MessageUpdate(**message_with_all_fields),
            object_id=uuid_test
        )
        patch_mock.assert_called()

    @patch.object(MessageCRUD, 'list_per_permissions')
    def test_handle_list_per_permissions_with_no_is_important_value(self, list_mock):
        '''
        Assert MessageController's handle_list_per_permission method calls
        MessageCRUD's list_per_permissions with expected parameters when
        is_important is not passed
        '''
        user = UserResponse(**user_db_response)
        MessageController().handle_list_per_permissions(
            db=self.session,
            user=user,
            limit=10,
            page=2
        )
        list_mock.assert_called_with(
            db=self.session,
            role_permission=user.role.id,
            user_permission=user.id,
            page=2,
            limit=10,
            is_important=None
        )

    @patch.object(MessageCRUD, 'list_per_permissions')
    def test_handle_list_per_permissions_with_is_important_as_bool(self, list_mock):
        '''
        Assert MessageController's handle_list_per_permission method calls
        MessageCRUD's list_per_permissions with expected parameters when
        is_important is a bool
        '''
        user = UserResponse(**user_db_response)
        MessageController().handle_list_per_permissions(
            db=self.session,
            user=user,
            limit=10,
            page=2,
            is_important=True
        )
        list_mock.assert_called_with(
            db=self.session,
            role_permission=user.role.id,
            user_permission=user.id,
            page=2,
            limit=10,
            is_important=True
        )
