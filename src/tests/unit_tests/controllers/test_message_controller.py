from unittest.mock import patch
from datetime import datetime

from src.tests.settings import BaseTestCase
from src.tests.mocks.message_mocks import (
    message_with_invalid_string_as_date,
    message_with_invalid_format_date,
    message_with_expiration_date_past,
    message_with_role_id,
    message_with_user_id
)
from src.exceptions.exceptions import BadRequestException, NotFoundException
from src.schemas.message_schema import MessageCreate
from src.controllers.message_controller import MessageController
from src.db.cruds.role_crud import RoleCRUD
from src.db.cruds.user_crud import UserCRUD


class MessageControllerTestClass(BaseTestCase):
    def test_handle_list(self):
        '''
          Should return list with all messages
        '''
        result = MessageController().handle_list(db=self.session)

        self.assertEqual(result, {'page': 1, 'total': 0, 'results': []})

    def test_handle_create_with_invalid_string_as_expiration_date(self):
        '''
        Trying to create a message with a invalid string as expiration_date must raise an error
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
        Trying to create a message with a invalid format for expiration_date must raise an error
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
                data=MessageCreate(**message_with_expiration_date_past)
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
                data=MessageCreate(**message_with_role_id)
            )
        exception = error.exception
        self.assertEqual(
            'Cargo não encontrado.',
            exception.detail
        )

    @patch.object(UserCRUD, 'get', return_value=None)
    def test_handle_create_with_not_found_role(self, _):
        '''
        Trying to create a message with an invalid user_id must raise an error
        '''
        with self.assertRaises(NotFoundException) as error:
            MessageController().handle_create(
                db=self.session,
                data=MessageCreate(**message_with_user_id)
            )
        exception = error.exception
        self.assertEqual(
            'Usuário não encontrado.',
            exception.detail
        )
