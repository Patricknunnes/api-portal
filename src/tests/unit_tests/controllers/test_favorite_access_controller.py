from unittest.mock import patch

from src.tests.mocks.access_mocks import access_1
from src.tests.mocks.user_mocks import user_db_response, valid_user_id, invalid_user_id
from src.tests.settings import BaseTestCase

from src.db.cruds.access_crud import AccessCRUD
from src.exceptions.exceptions import NotFoundException, BadRequestException
from src.db.cruds.favorite_access_crud import FavoriteAccessCRUD
from src.controllers.favorite_access_controller import FavoriteAccessController
from src.schemas.favorite_access_schema import FavoriteAccessPrimaryKeys
from src.db.cruds.user_crud import UserCRUD
from src.db.models.models import UserModel, FavoriteAccessModel


class FavoriteAccessControllerTestClass(BaseTestCase):
    def test_handle_create_with_invalid_access_id(self):
        '''
        Should raise an error when it's called with invalid access_id
        '''
        with self.assertRaises(NotFoundException) as error:
            FavoriteAccessController().handle_create(
                db=self.session,
                data=FavoriteAccessPrimaryKeys(
                    access_id=access_1.id, user_id=valid_user_id))
        exception = error.exception
        self.assertEqual('Acesso não encontrado.', exception.detail)

    @patch.object(AccessCRUD, 'get', return_value=access_1)
    def test_handle_create_with_invalid_user_id(self, _):
        '''
        Should raise an error when it's called with invalid user_id
        '''
        with self.assertRaises(NotFoundException) as error:
            FavoriteAccessController().handle_create(
                db=self.session,
                data=FavoriteAccessPrimaryKeys(
                    access_id=access_1.id, user_id=invalid_user_id))
        exception = error.exception
        self.assertEqual('Usuário não encontrado.', exception.detail)

    @patch.object(FavoriteAccessCRUD, 'get', return_value=FavoriteAccessModel(
        user_id=user_db_response['id'],
        access_id=access_1.id
    ))
    @patch.object(UserCRUD, 'get', return_value=UserModel(**user_db_response))
    @patch.object(AccessCRUD, 'get', return_value=access_1)
    def test_handle_create_when_duplicated(self, *_):
        '''
        Should raise an error when its duplicated
        '''
        with self.assertRaises(BadRequestException) as error:
            FavoriteAccessController().handle_create(
                db=self.session,
                data=FavoriteAccessPrimaryKeys(
                    access_id=access_1.id, user_id=invalid_user_id))
        exception = error.exception
        self.assertEqual(
            'O acesso já foi definido como favorito pelo usuário.',
            exception.detail)

    @patch.object(FavoriteAccessCRUD, 'get', return_value=None)
    @patch.object(UserCRUD, 'get', return_value=UserModel(**user_db_response))
    @patch.object(AccessCRUD, 'get', return_value=access_1)
    @patch.object(FavoriteAccessCRUD, 'create', return_value=FavoriteAccessModel(
        user_id=user_db_response['id'],
        access_id=access_1.id
    ))
    def test_handle_create(self, create_mock, *_):
        '''
        Should return the created row
        '''
        result = FavoriteAccessController().handle_create(
            db=self.session,
            data=FavoriteAccessPrimaryKeys(
                access_id=access_1.id, user_id=invalid_user_id))
        self.assertEqual(create_mock(), result)

    @patch.object(FavoriteAccessCRUD, 'get', return_value=None)
    def test_handle_delete_when_already_unset(self, *_):
        '''
        Should raise an error when access is not set as favorite
        '''
        with self.assertRaises(NotFoundException) as error:
            FavoriteAccessController().handle_delete(
                db=self.session,
                data=FavoriteAccessPrimaryKeys(
                    access_id=access_1.id, user_id=invalid_user_id))
        exception = error.exception
        self.assertEqual('Acesso não favoritado.', exception.detail)

    @patch.object(FavoriteAccessCRUD, 'get', return_value=FavoriteAccessModel(
        user_id=user_db_response['id'],
        access_id=access_1.id
    ))
    @patch.object(FavoriteAccessCRUD, 'delete', return_value='deleted')
    def test_handle_delete(self, *_):
        '''
        Should return the crud_class' delete method result
        '''
        result = FavoriteAccessController().handle_delete(
            db=self.session,
            data=FavoriteAccessPrimaryKeys(
                access_id=access_1.id, user_id=invalid_user_id))
        self.assertEqual('deleted', result)
