from unittest.mock import patch

from src.tests.mocks.message_mocks import message_created_with_all_fields
from src.tests.mocks.message_user_mocks import message_user
from src.tests.mocks.user_mocks import user_db_response
from src.tests.settings import BaseTestCase

from src.controllers.message_user_controller import MessageUserController
from src.db.cruds.message_crud import MessageCRUD
from src.db.cruds.message_user_crud import MessageUserCRUD
from src.db.cruds.user_crud import UserCRUD
from src.exceptions.exceptions import NotFoundException, BadRequestException
from src.schemas.message_user_schema import MessageUserPrimaryKeys


class MessageControllerTestClass(BaseTestCase):
    @patch.object(MessageCRUD, 'get', return_value=None)
    def test_handle_create_with_not_found_message(self, _):
        '''
        Trying to create a message_user relationship with
        an invalid message_id must raise an error
        '''
        with self.assertRaises(NotFoundException) as error:
            MessageUserController().handle_create(
                db=self.session,
                data=MessageUserPrimaryKeys(**message_user)
            )
        exception = error.exception
        self.assertEqual('Mensagem não encontrada.', exception.detail)

    @patch.object(MessageCRUD, 'get', return_value=message_created_with_all_fields)
    @patch.object(UserCRUD, 'get', return_value=None)
    def test_handle_create_with_not_found_user(self, *_):
        '''
        Trying to create a message_user relationship with
        an invalid user_id must raise an error
        '''
        with self.assertRaises(NotFoundException) as error:
            MessageUserController().handle_create(
                db=self.session,
                data=MessageUserPrimaryKeys(**message_user)
            )
        exception = error.exception
        self.assertEqual('Usuário não encontrado.', exception.detail)

    @patch.object(MessageCRUD, 'get', return_value=message_created_with_all_fields)
    @patch.object(UserCRUD, 'get', return_value=user_db_response)
    @patch.object(MessageUserCRUD, 'get', return_value=message_user)
    def test_handle_create_with_message_user_already_registered(self, *_):
        '''
        Trying to create a message_user relationship already registered
        must raise an error
        '''
        with self.assertRaises(BadRequestException) as error:
            MessageUserController().handle_create(
                db=self.session,
                data=MessageUserPrimaryKeys(**message_user)
            )
        exception = error.exception
        self.assertEqual('A mensagem já foi marcada como lida.', exception.detail)

    @patch.object(MessageCRUD, 'get', return_value=message_created_with_all_fields)
    @patch.object(UserCRUD, 'get', return_value=user_db_response)
    @patch.object(MessageUserCRUD, 'get', return_value=None)
    @patch.object(MessageUserCRUD, 'create')
    def test_handle_create_without_optional_fields(self, create_mock, *_):
        '''
        Trying to create a message_user should call MessageUserCRUD create method
        '''
        MessageUserController().handle_create(
            db=self.session,
            data=MessageUserPrimaryKeys(**message_user)
        )
        create_mock.assert_called()

    @patch.object(MessageUserCRUD, 'get')
    def test_handle_get(self, get_mock):
        '''handle_get method should call MessageUserCRUD get method'''
        MessageUserController().handle_get(db=self.session, data=message_user)
        get_mock.assert_called()
