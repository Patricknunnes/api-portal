from unittest.mock import patch

from src.controllers.registration_controller import RegistrationController
from src.db.cruds.registration_crud import RegistrationCRUD
from src.exceptions.exceptions import BadRequestException, NotFoundException
from src.schemas.registration_schema import RegistrationCreateModel
from src.tests.settings import BaseTestCase


class RegistrationControllerTestClass(BaseTestCase):
    @patch.object(RegistrationCRUD, 'handle_list')
    def test_handle_list_call(self, list_mock):
        '''
          Should call CRUD handle_list method with expected params
        '''
        RegistrationController().handle_list(
            db=self.session,
            filter_attrs=['name'],
            filters='test',
            limit=15,
            page=2,
            sort='name:desc,status'
        )
        list_mock.assert_called_with(
            db=self.session,
            filter_attrs=['name'],
            filters='test',
            limit=15,
            page=2,
            sort=(('name', 'desc'), ('status', 'asc'))
        )

    def test_handle_create_with_invalid_birthdate(self):
        '''
          Should raise error when birthdate is in an invalid format
        '''
        with self.assertRaises(BadRequestException) as error:
            RegistrationController().handle_create(
                db=self.session,
                data=RegistrationCreateModel(
                    document='12345678901',
                    email='test@mail.com',
                    birthdate='01/01/2000',
                    service='service1'
                )
            )

        exception = error.exception
        self.assertEqual(
            'Data de expiração inválida. Siga o formato YYYY-MM-DD.',
            exception.detail
        )

    @patch.object(RegistrationCRUD, 'create')
    def test_handle_create(self, create_mock):
        '''
          Should call CRUD's create method with expected params
        '''
        registration = RegistrationCreateModel(
            document='12345678901',
            email='test@mail.com',
            birthdate='2000-01-01',
            service='service1'
        )
        RegistrationController().handle_create(
            db=self.session,
            data=registration
        )
        create_mock.assert_called_with(self.session, registration, True)

    def test_handle_get_by_data_with_no_match(self):
        '''
          Should raise error when there is no match
        '''
        with self.assertRaises(NotFoundException) as error:
            RegistrationController().handle_get_by_data(
                db=self.session,
                data={'email': 'no_match@email.com'},
                exception_message='Error'
            )

        exception = error.exception
        self.assertEqual('Error', exception.detail)

    @patch.object(RegistrationCRUD, 'get', return_value={})
    def test_handle_get_by_data_with_match(self, _):
        '''
          Should raise error when there is no match
        '''
        result = RegistrationController().handle_get_by_data(
            db=self.session,
            data={'email': 'match@email.com'},
            exception_message='Error'
        )

        self.assertEqual(result, {})
