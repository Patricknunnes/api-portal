from src.db.cruds.message_user_crud import MessageUserCRUD
from src.db.models.models import MessageUserModel
from src.tests.mocks.message_user_mocks import message_user
from src.tests.settings import BaseTestCase


class MessageCRUDTestClass(BaseTestCase):
    def test_create(self):
        '''Should return created message_user data with message_read as True'''
        result = MessageUserCRUD().create(db=self.session, data=message_user)

        self.assertIsInstance(result, MessageUserModel)
        self.assertTrue(result.message_read)

        MessageUserCRUD().delete(db=self.session, object_id=result.id)

    def test_get_when_there_is_data_match(self):
        '''Should return message_user relationship row'''
        result = MessageUserCRUD().create(db=self.session, data=message_user)
        row = MessageUserCRUD().get(db=self.session, **message_user)

        self.assertIsInstance(row, MessageUserModel)
        self.assertTrue(row.message_read)

        MessageUserCRUD().delete(db=self.session, object_id=result.id)

    def test_get_when_there_is_no_data_match(self):
        '''Should return None when there is no match'''
        result = MessageUserCRUD().get(db=self.session, **message_user)

        self.assertIsNone(result)
