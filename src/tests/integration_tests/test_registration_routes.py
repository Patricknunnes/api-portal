from json import JSONDecodeError
from unittest.mock import patch

from src.db.cruds.registration_crud import RegistrationCRUD
from src.db.models.models import RegistrationModel, UserModel, RoleModel
from src.tests.mocks.role_mocks import role_1

from src.tests.mocks.registration_mocks import (
    registrations,
    invalid_date_registration,
    valid_date_registration
)
from src.tests.settings import ApiWithAuthTestCase


user = UserModel(
    id='071aac88-f263-4c07-b215-7170d180da6a',
    name='user1',
    email='user1@email.com',
    document='12345678903',
    username='username1',
    phone=None,
    is_totvs=False,
    password='user_password',
    role=RoleModel(**role_1),
    image=None
)


class RegistrationRouteWithAuthTestClass(ApiWithAuthTestCase):
    def test_handle_list_registrations(self):
        '''
        Should return list with status 200
        '''
        response = self.client.get('/registration')
        self.assertEqual(200, response.status_code)
        self.assertEqual({'page': 1, 'total': 0, 'results': []}, response.json())

    def test_get_office365_registration_data_when_not_found(self):
        '''
        Should return error message and status 404 when registration not found
        '''
        response = self.client.get('/registration/office365/me')
        self.assertEqual(404, response.status_code)
        self.assertEqual({'detail': 'Cadastro não encontrado.'}, response.json())

    @patch.object(RegistrationCRUD, 'get', return_value=RegistrationModel(
        **registrations[0], user=user, id='de109b64-a829-4421-b254-bd504c99cd7c'))
    def test_get_office365_registration_data_when_found(self, _):
        '''
        Should return office registration data
        '''

        response = self.client.get('/registration/office365/me')
        self.assertEqual(200, response.status_code)
        self.assertEqual('de109b64-a829-4421-b254-bd504c99cd7c', response.json()['id'])

    def test_create_office365_registration_data_when_invalid_birthdate_format(self):
        '''
        Should return error message and status 400 when birthdate
        is in an invalid format
        '''
        response = self.client.post(
            '/registration/office365',
            json=invalid_date_registration)
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            {'detail': 'Data de expiração inválida. Siga o formato YYYY-MM-DD.'},
            response.json())

    @patch.object(RegistrationCRUD, 'get', return_value=registrations[0])
    def test_create_office365_registration_data_when_duplicated_registration(self, _):
        '''
        Should return error message and status 400 when user has already been registered
        '''
        response = self.client.post(
            '/registration/office365', json=valid_date_registration)
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            {'detail': 'O usuário já tem cadastro no serviço.'},
            response.json())

    @patch.object(RegistrationCRUD, 'create', return_value=RegistrationModel(
        **registrations[0], user=user, id='de109b64-a829-4421-b254-bd504c99cd7c'))
    def test_create_office365_registration_data(self, _):
        '''
        Should return status 201 when registration is successfully created
        '''
        response = self.client.post(
            '/registration/office365', json=valid_date_registration)
        self.assertEqual(201, response.status_code)
        self.assertEqual('de109b64-a829-4421-b254-bd504c99cd7c', response.json()['id'])

    def test_patch_registration_data_with_no_match(self):
        '''
        Should return error message and status 404 when registration is not found
        '''
        response = self.client.patch(
            '/registration/de109b64-a829-4421-b254-bd504c99cd7c',
            json={'status': 'APPROVED'})
        self.assertEqual(404, response.status_code)
        self.assertEqual({'detail': 'Cadastro não encontrado.'}, response.json())

    @patch.object(RegistrationCRUD, 'get', return_value=registrations[0])
    def test_patch_registration_data_with_match(self, _):
        '''
        Should return error message and status 404 when registration is found
        '''
        response = self.client.patch(
            '/registration/de109b64-a829-4421-b254-bd504c99cd7c',
            json={'status': 'APPROVED'})
        self.assertEqual(204, response.status_code)
        self.assertRaises(JSONDecodeError, response.json)
