from unittest.mock import patch
from src.tests.settings import ApiBaseTestCase
from src.db.cruds.role_crud import RoleCRUD
from src.tests.mocks.role_mocks import roles, invalid_role_id, valid_role_id


class RoleRouteTestClass(ApiBaseTestCase):
    @patch.object(RoleCRUD, 'list', return_value=roles)
    def test_get_roles(self, mock):
        '''
          Test return of all roles with status 200
        '''
        response = self.client.get('/role')
        self.assertEqual(200, response.status_code)
        self.assertEqual(roles, response.json())


    @patch.object(RoleCRUD, 'get', return_value=roles[0])
    def test_get_role_by_id_when_id_found(self, mock):
        '''
          Test return of single role with status 200 when id found
        '''
        response = self.client.get(f'/role/{valid_role_id}')
        self.assertEqual(200, response.status_code)
        self.assertEqual(roles[0], response.json())


    @patch.object(RoleCRUD, 'get', return_value=None)
    def test_get_role_by_id_when_id_not_found(self, mock):
        '''
          Test return of error message with status 404 when id not found
        '''
        response = self.client.get(f'/role/{invalid_role_id}')
        self.assertEqual(404, response.status_code)
        self.assertEqual({'detail': 'Role não encontrada.'}, response.json())
