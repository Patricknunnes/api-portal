from json import JSONDecodeError
from unittest.mock import MagicMock, patch

from src.tests.settings import ApiWithAuthTestCase, ApiBaseTestCase
from src.tests.mocks.user_mocks import (
    invalid_user_id,
    user_create_data,
    user_db_response,
    valid_user_id,
    user_update_data
)
from src.tests.mocks.role_mocks import roles, invalid_role_id
from src.db.cruds.role_crud import RoleCRUD
from src.db.cruds.user_crud import UserCRUD


class UserRouteNoAuthTestClass(ApiBaseTestCase):
    def test_get_users_with_invalid_token(self):
        '''
        Should return error message and status 401
        when requesting GET /user with invalid token
        '''
        response = self.client.get(
            '/user',
            headers={'Authorization': 'Bearer invalid_token'}
        )
        self.assertEqual(401, response.status_code)
        self.assertEqual(self.invalid_token_msg, response.json())

    def test_get_user_by_id_with_invalid_token(self):
        '''
        Should return error message and status 401
        when requesting GET /user/role_id with invalid token
        '''
        response = self.client.get(
            f'/user/{invalid_user_id}',
            headers={'Authorization': 'Bearer invalid_token'}
        )
        self.assertEqual(401, response.status_code)
        self.assertEqual(self.invalid_token_msg, response.json())

    def test_create_user_with_invalid_token(self):
        '''
        Should return error message and status 401
        when requesting POST /user with invalid token
        '''
        response = self.client.post('/user',
                                    json={**user_create_data, 'role_id': invalid_role_id},
                                    headers={'Authorization': 'Bearer invalid_token'})
        self.assertEqual(401, response.status_code)
        self.assertEqual(self.invalid_token_msg, response.json())

    def test_patch_user_with_invalid_token(self):
        '''
        Should return error message and status 401
        when requesting PATCH /user/user_id with invalid token
        '''
        response = self.client.patch(
            f'/user/{valid_user_id}',
            json={'name': 'changed_name'},
            headers={'Authorization': 'Bearer invalid_token'})
        self.assertEqual(401, response.status_code)
        self.assertEqual(self.invalid_token_msg, response.json())


class UserRouteWithAuthTestClass(ApiWithAuthTestCase):
    def test_get_users(self):
        '''
        Should return list with status 200
        '''
        response = self.client.get('/user')
        self.assertEqual(200, response.status_code)
        self.assertEqual({'page': 1, 'total': 0, 'user_response': []}, response.json())

    def test_get_user_by_id_when_id_not_found(self):
        '''
        Should return error message and status 404 when id not found
        '''
        response = self.client.get(f'/user/{invalid_user_id}')
        self.assertEqual(404, response.status_code)
        self.assertEqual({'detail': 'Usuário não encontrado'}, response.json())

    @patch.object(UserCRUD, 'get', return_value=user_db_response)
    def test_get_user_by_id_when_id_found(self, mock):
        '''
        Should return user data and status 200 when id found
        '''
        response = self.client.get(f'/user/{valid_user_id}')
        self.assertEqual(200, response.status_code)

        body = response.json()

        for key, value in user_db_response.items():
            if key != 'password':
                self.assertEqual(value, body[key])
            else:
                self.assertTrue(key not in body)

    def test_create_user_with_invalid_role_id(self):
        '''
        Should return error message and status 404 when role_id not found
        '''
        response = self.client.post('/user',
                                    json={**user_create_data, 'role_id': invalid_role_id})
        self.assertEqual(404, response.status_code)
        self.assertEqual({'detail': 'Role não encontrada.'}, response.json())

    @patch.object(RoleCRUD, 'get', return_value=roles[0])
    def test_create_user_with_invalid_document(self, mock):
        '''
        Should return error message and status 400 when document is invalid
        '''
        response = self.client.post('/user',
                                    json={**user_create_data, 'document': '1111111'})
        self.assertEqual(400, response.status_code)
        self.assertEqual({'detail': 'Documento invalido.'}, response.json())

    @patch.object(UserCRUD, 'get_user_document_or_email', return_value=True)
    @patch.object(RoleCRUD, 'get', return_value=roles[0])
    def test_create_user_with_document_or_email_in_use(self, RoleCRUDMock, UserCRUDMock):
        '''
        Should return error message and status 400 when document or email already in use
        '''
        response = self.client.post('/user',
                                    json=user_create_data)
        self.assertEqual(400, response.status_code)
        self.assertEqual({'detail': 'Documento ou Email já cadastrado.'}, response.json())

    @patch.object(RoleCRUD, 'get', return_value=roles[0])
    def test_create_user_with_invalid_fields(self, mock):
        '''
        Should return error message and status 400
        when required fields have invalid value
        '''
        response = self.client.post('/user',
                                    json={**user_create_data, 'name': 'string'})
        self.assertEqual(400, response.status_code)
        self.assertEqual({'detail': 'Campos obrigatorios: (name) .'}, response.json())

    @patch.object(UserCRUD, 'create', return_value=user_db_response)
    @patch.object(RoleCRUD, 'get', return_value=roles[0])
    def test_create_user(self, RoleCRUDMock, UserCRUDMock):
        '''
        Should return created user and status 201
        '''
        response = self.client.post('/user',
                                    json=user_create_data)
        self.assertEqual(201, response.status_code)

        body = response.json()

        for key, value in user_create_data.items():
            if key != 'password' and key != 'role_id':
                self.assertEqual(value, body[key])
            else:
                self.assertTrue(key not in body)

        self.assertEqual(user_create_data['role_id'], body['role']['id'])

    @patch.multiple(
        UserCRUD,
        get=MagicMock(return_value=user_db_response),
        patch=MagicMock(return_value=None)
    )
    @patch.object(RoleCRUD, 'get', return_value=roles[0])
    def test_patch_user(self, RoleCRUDMock, **UserCRUDMock):
        '''
        Should return status 204 and no body
        '''
        response = self.client.patch(
            f'/user/{valid_user_id}',
            json=user_update_data
        )
        self.assertEqual(204, response.status_code)
        self.assertRaises(JSONDecodeError, response.json)
