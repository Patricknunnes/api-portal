from unittest.mock import patch

from src.tests.settings import ApiWithAuthTestCase, ApiBaseTestCase
from src.db.cruds.role_crud import RoleCRUD
from src.tests.mocks.role_mocks import roles, invalid_role_id, valid_role_id


class RoleRouteNoAuthTestClass(ApiBaseTestCase):
    def test_get_roles_with_invalid_token(self):
        '''
        Should return error message and status 401
        when requesting GET /role with invalid token
        '''

        response = self.client.get(
            '/role',
            headers={'Authorization': 'Bearer invalid_token'}
        )
        self.assertEqual(401, response.status_code)
        self.assertEqual(self.invalid_token_msg, response.json())

    def test_get_role_by_id_with_invalid_token(self):
        '''
        Should return error message and status 401
        when requesting GET /role/role_id with invalid token
        '''
        response = self.client.get(
            f'/role/{valid_role_id}',
            headers={'Authorization': 'Bearer valid_token'}
        )
        self.assertEqual(401, response.status_code)
        self.assertEqual(self.invalid_token_msg, response.json())


class RoleRouteWithAuthTestClass(ApiWithAuthTestCase):
    def test_get_roles(self):
        '''
          Should return list with status 200
        '''
        response = self.client.get('/role')
        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json())

    @patch.object(RoleCRUD, 'get', return_value=roles[0])
    def test_get_role_by_id_when_id_found(self, _):
        '''
          Should return single role and status 200 when id found
        '''
        response = self.client.get(f'/role/{valid_role_id}')
        self.assertEqual(200, response.status_code)
        self.assertEqual(roles[0], response.json())

    def test_get_role_by_id_when_id_not_found(self):
        '''
          Should return error message and status 404 when id not found
        '''
        response = self.client.get(f'/role/{invalid_role_id}')
        self.assertEqual(404, response.status_code)
        self.assertEqual({'detail': 'Role não encontrada.'}, response.json())
