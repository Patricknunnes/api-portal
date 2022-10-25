from src.db.cruds.user_crud import UserCRUD
from src.tests.settings import BaseTestCase
from src.db.models.user_model import UserModel
from src.tests.mocks.user_mocks import (
    user_create_data,
    invalid_username,
    invalid_user_id,
    user_update_data
)


class UserCrudTestClass(BaseTestCase):
    def test_create(self):
        '''Should return created user'''
        result = UserCRUD().create(db=self.session, data=user_create_data)
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, UserModel))

    def test_get_user_with_unregistered_email(self):
        '''Should return None with unregistered email'''
        result = UserCRUD().get_user_by_username_or_email(
            db=self.session,
            email='unregistered@email.com'
        )
        self.assertIsNone(result)

    def test_get_user_with_unregistered_username(self):
        '''Should return None with unregistered username'''
        result = UserCRUD().get_user_by_username_or_email(
            db=self.session,
            username=invalid_username
        )
        self.assertIsNone(result)

    def test_get_user_with_registered_username(self):
        '''Should return user with registered username'''
        result = UserCRUD().get_user_by_username_or_email(
            db=self.session,
            username=user_create_data['username']
        )
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, UserModel))

    def test_get_user_with_registered_email(self):
        '''Should return user with registered email'''
        result = UserCRUD().get_user_by_username_or_email(
            db=self.session,
            email=user_create_data['email']
        )
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, UserModel))

    def test_get_user_with_registered_email_but_unregistered_username(self):
        '''
        Should return user when just one info match
        '''
        result = UserCRUD().get_user_by_username_or_email(
            db=self.session,
            email=user_create_data['email'],
            username=invalid_username
        )
        self.assertIsNotNone(result)

    def test_list(self):
        '''
          Should return list
        '''
        result = UserCRUD().list(db=self.session)
        self.assertEqual(type(result), list)

    def test_get_without_match(self):
        '''
        Should return None when no user id match
        '''
        result = UserCRUD().get(db=self.session, id=invalid_user_id)
        self.assertIsNone(result)

    def test_get_with_match(self):
        '''
        Should return user when user id match
        '''
        user_id = UserCRUD().list(db=self.session)[0].id
        result = UserCRUD().get(db=self.session, id=user_id)
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, UserModel))

    def test_patch(self):
        '''
        Should return None and update data
        '''
        user_before_update = UserCRUD().list(db=self.session)[0]
        user_name = user_before_update.name

        result = UserCRUD().patch(
            db=self.session,
            object_id=user_before_update.id,
            data=user_update_data
        )
        self.assertIsNone(result)

        user_after_update = UserCRUD().get(db=self.session, id=user_before_update.id)
        self.assertNotEqual(user_name, user_after_update.name)
