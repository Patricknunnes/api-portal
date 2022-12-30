from src.db.cruds.message_crud import MessageCRUD
from src.db.models.models import MessageModel
from src.tests.mocks.message_mocks import message_one, message_two
from src.tests.settings import BaseTestCase


class MessageCRUDTestClass(BaseTestCase):
    def test_create(self):
        '''Should return created message'''
        result = MessageCRUD().create(db=self.session, data=message_one)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, MessageModel)

    def test_list(self):
        '''Should return message list'''
        result = MessageCRUD().list(db=self.session)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_get_message_with_match(self):
        '''Should return message found'''
        result = MessageCRUD().get(
            db=self.session,
            id=message_one['id']
        )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, MessageModel)

    def test_patch(self):
        '''Should update message'''
        new_title = 'another title'
        result = MessageCRUD().get(db=self.session, id=message_one['id'])

        self.assertNotEqual(result.title, new_title)

        MessageCRUD().patch(db=self.session, object_id=message_one['id'], data={'title': new_title})

        result = MessageCRUD().get(db=self.session, id=message_one['id'])

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
        MessageCRUD().create(db=self.session, data=message_two)
        result = MessageCRUD().get(db=self.session, id=message_two['id'])

        self.assertIsNotNone(result)

        MessageCRUD().delete(db=self.session, object_id=message_two['id'])

        result = MessageCRUD().get(db=self.session, id=message_two['id'])

        self.assertIsNone(result)
