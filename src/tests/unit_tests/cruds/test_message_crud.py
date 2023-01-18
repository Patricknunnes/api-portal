from datetime import datetime

from src.db.cruds.message_crud import MessageCRUD
from src.db.models.models import MessageModel
from src.tests.mocks.message_mocks import message
from src.tests.mocks.role_mocks import roles
from src.tests.mocks.user_mocks import user_db_response
from src.tests.settings import BaseTestCase


class MessageCRUDTestClass(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.default_message = MessageCRUD().create(db=self.session, data=message)

    def tearDown(self) -> None:
        MessageCRUD().delete(db=self.session, object_id=self.default_message.id)
        return super().tearDown()

    def test_create(self):
        '''Should return created message with created_at as datetime and updated_at should
        be None'''
        result = MessageCRUD().create(db=self.session, data=message)

        self.assertIsInstance(result, MessageModel)
        self.assertIsInstance(result.created_at, datetime)
        self.assertIsNone(result.updated_at)

        MessageCRUD().delete(db=self.session, object_id=result.id)

    def test_messages_count(self):
        self.assertEqual(MessageCRUD().count_records(db=self.session), 1)

    def test_messages_list(self):
        '''
        Should return page info with list
        '''
        result = MessageCRUD().handle_list(db=self.session)
        self.assertEqual(result['page'], 1)
        self.assertEqual(result['total'], 1)
        self.assertEqual(len(result['results']), 1)

    def test_get_message_with_match(self):
        '''Should return message found'''
        messages = MessageCRUD().handle_list(db=self.session)['results']
        result = MessageCRUD().get(
            db=self.session,
            id=messages[0].id
        )
        self.assertEqual(result, self.default_message)

    def test_patch(self):
        '''Should update message, set datetime to updated_at and not modify created_at
        value'''
        new_title = 'another title'
        message_from_db = MessageCRUD().handle_list(db=self.session)['results'][0]

        self.assertNotEqual(message_from_db.title, new_title)
        self.assertIsNone(message_from_db.updated_at)

        MessageCRUD().patch(
            db=self.session,
            object_id=message_from_db.id,
            data={'title': new_title}
        )

        result = MessageCRUD().get(db=self.session, id=message_from_db.id)

        self.assertEqual(result.title, new_title)
        self.assertIsInstance(message_from_db.updated_at, datetime)
        self.assertEqual(message_from_db.created_at, result.created_at)

    def test_get_message_without_match(self):
        '''Should return None when id not found'''
        result = MessageCRUD().get(
            db=self.session,
            id='88888ecb-2b9a-486c-b26a-17e198592206'
        )
        self.assertIsNone(result)

    def test_delete(self):
        '''Should delete message'''
        new_message = MessageCRUD().create(db=self.session, data=message)

        self.assertEqual(MessageCRUD().count_records(db=self.session), 2)

        MessageCRUD().delete(db=self.session, object_id=new_message.id)

        self.assertEqual(MessageCRUD().count_records(db=self.session), 1)

        result = MessageCRUD().get(db=self.session, id=new_message.id)

        self.assertIsNone(result)

    def test_list_per_permissions_with_expired_message(self):
        '''
        When there are messages with expiration_date,
        the ones with past dates should not be listed
        '''
        message_expired = MessageCRUD().create(
            db=self.session,
            data=dict(
                **message,
                expiration_date=datetime.strptime('1900-01-01', '%Y-%m-%d')
            )
        )
        message_not_expired = MessageCRUD().create(
            db=self.session,
            data=dict(
                **message,
                expiration_date=datetime.strptime('3000-01-01', '%Y-%m-%d')
            )
        )

        message_to_another_role = MessageCRUD().create(
            db=self.session,
            data=dict(
                **message,
                role_permission='5545ccbe-9e27-4d3f-b26d-5aa546690612'
            )
        )

        message_to_another_user = MessageCRUD().create(
            db=self.session,
            data=dict(
                **message,
                user_permission='5545ccbe-9e27-4d3f-b26d-5aa546690612'
            )
        )

        result = MessageCRUD().list_per_permissions(
            db=self.session,
            role_permission=roles[0]['id'],
            user_permission=user_db_response['id']
        )

        self.assertEqual(MessageCRUD().count_records(db=self.session), 5)

        self.assertEqual(result['total'], 2)
        self.assertEqual(result['page'], 1)
        self.assertEqual(len(result['results']), 2)
        self.assertEqual(result['results'][0], self.default_message)
        self.assertEqual(result['results'][1], message_not_expired)

        MessageCRUD().delete(db=self.session, object_id=message_expired.id)
        MessageCRUD().delete(db=self.session, object_id=message_not_expired.id)
        MessageCRUD().delete(db=self.session, object_id=message_to_another_role.id)
        MessageCRUD().delete(db=self.session, object_id=message_to_another_user.id)
