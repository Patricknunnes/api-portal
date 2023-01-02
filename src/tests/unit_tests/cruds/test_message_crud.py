from src.db.cruds.message_crud import MessageCRUD
from src.db.models.models import MessageModel
from src.tests.mocks.message_mocks import message
from src.tests.settings import BaseTestCase


class MessageCRUDTestClass(BaseTestCase):
    def test_create(self):
        '''Should return created message'''
        result = MessageCRUD().create(db=self.session, data=message)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, MessageModel)

    def test_messages_count(self):
        result = MessageCRUD().count_records(db=self.session)
        self.assertEqual(result, 1)

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
        self.assertIsNotNone(result)
        self.assertIsInstance(result, MessageModel)

    def test_patch(self):
        '''Should update message'''
        new_title = 'another title'
        message_from_db = MessageCRUD().handle_list(db=self.session)['results'][0]

        self.assertNotEqual(message_from_db.title, new_title)

        MessageCRUD().patch(db=self.session, object_id=message_from_db.id, data={'title': new_title})

        result = MessageCRUD().get(db=self.session, id=message_from_db.id)

        self.assertEqual(result.title, new_title)

    def test_get_message_without_match(self):
        '''Should return None when id not found'''
        result = MessageCRUD().get(
            db=self.session,
            id='88888ecb-2b9a-486c-b26a-17e198592206'
        )
        self.assertIsNone(result)
    
    def test_delete(self):
        '''Should delete message'''
        MessageCRUD().create(db=self.session, data=message)
        message_from_db = MessageCRUD().handle_list(db=self.session)['results'][1]

        MessageCRUD().delete(db=self.session, object_id=message_from_db.id)

        result = MessageCRUD().get(db=self.session, id=message_from_db.id)

        self.assertIsNone(result)
