from json import JSONDecodeError
from unittest.mock import patch, MagicMock

from src.tests.mocks.access_mocks import access_1
from src.tests.mocks.role_mocks import role_1
from src.tests.mocks.user_mocks import user_db_response
from src.tests.settings import ApiWithAuthTestCase

from src.db.cruds.access_crud import AccessCRUD
from src.db.cruds.favorite_access_crud import FavoriteAccessCRUD
from src.db.cruds.role_crud import RoleCRUD
from src.db.cruds.user_crud import UserCRUD
from src.db.models.models import RoleModel, UserModel, FavoriteAccessModel


class AccessRouteTestClass(ApiWithAuthTestCase):
    def setUp(self) -> None:
        self.headers = {'Authorization': 'Bearer valid_token'}
        return super().setUp()

    @patch.object(RoleCRUD, 'get', return_value=RoleModel(**role_1))
    def test_list_user_accesses(self, _):
        '''
        Should return status 200 and allowed accesses for user
        '''
        response = self.client.get('/access/me', headers=self.headers)

        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json())

    def test_set_access_as_favorite_with_invalid_access_id(self):
        '''
        Should return status 404 when it's a invalid access_id
        '''
        response = self.client.post(
            '/access/me/favorite/72978d28-c230-4322-93cf-1da13f06d726',
            headers=self.headers
        )

        self.assertEqual(404, response.status_code)
        self.assertEqual({'detail': 'Acesso não encontrado.'}, response.json())

    @patch.object(AccessCRUD, 'get', return_value=access_1)
    def test_set_access_as_favorite_with_invalid_user(self, _):
        '''
        Should return status 404 when it's a invalid access_id
        '''
        response = self.client.post(
            '/access/me/favorite/72978d28-c230-4322-93cf-1da13f06d726',
            headers=self.headers
        )

        self.assertEqual(404, response.status_code)
        self.assertEqual({'detail': 'Usuário não encontrado.'}, response.json())

    @patch.object(FavoriteAccessCRUD, 'get', return_value=FavoriteAccessModel(
        user_id=user_db_response['id'],
        access_id=access_1.id
    ))
    @patch.object(UserCRUD, 'get', return_value=UserModel(**user_db_response))
    @patch.object(AccessCRUD, 'get', return_value=access_1)
    def test_set_access_as_favorite_with_already_set_favorite(self, *_):
        '''
        Should return status 400 when the access is already set as favorite'''
        response = self.client.post(
            '/access/me/favorite/72978d28-c230-4322-93cf-1da13f06d726',
            headers=self.headers
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            {'detail': 'O acesso já foi definido como favorito pelo usuário.'},
            response.json())

    @patch.multiple(
        FavoriteAccessCRUD,
        create=MagicMock(return_value=FavoriteAccessModel(
            user_id=user_db_response['id'],
            access_id=access_1.id
        )),
        get=MagicMock(return_value=None)
    )
    @patch.object(UserCRUD, 'get', return_value=UserModel(**user_db_response))
    @patch.object(AccessCRUD, 'get', return_value=access_1)
    def test_set_access_as_favorite(self, *_):
        '''
        Should return status 201 when the access is set as favorite successfully'''
        response = self.client.post(
            f'/access/me/favorite/{access_1.id}',
            headers=self.headers
        )

        self.assertEqual(201, response.status_code)
        self.assertEqual(response.json()['access_id'], access_1.id)
        self.assertEqual(response.json()['user_id'], user_db_response['id'])

    @patch.object(FavoriteAccessCRUD, 'get', return_value=None)
    def test_unset_favorite_access_when_it_is_not_favorite(self, _):
        '''
        Should return status 404 when access wasn't set as favorite
        '''
        response = self.client.delete(
            '/access/me/favorite/72978d28-c230-4322-93cf-1da13f06d726',
            headers=self.headers
        )

        self.assertEqual(404, response.status_code)
        self.assertEqual({'detail': 'Acesso não favoritado.'}, response.json())

    @patch.multiple(
        FavoriteAccessCRUD,
        get=MagicMock(return_value=FavoriteAccessModel(
            user_id=user_db_response['id'],
            access_id=access_1.id
        )),
        delete=MagicMock(return_value=None)
    )
    def test_unset_favorite_access(self):
        '''
        Should return status 204 when it's unset as favorite successfully
        '''
        response = self.client.delete(
            '/access/me/favorite/72978d28-c230-4322-93cf-1da13f06d726',
            headers=self.headers
        )

        self.assertEqual(204, response.status_code)
        self.assertRaises(JSONDecodeError, response.json)
