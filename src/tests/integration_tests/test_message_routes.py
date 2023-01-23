from unittest.mock import patch, MagicMock
from datetime import datetime
from json import JSONDecodeError

from src.tests.mocks.message_mocks import (
    message_created_with_all_fields,
    message_with_all_fields,
    message_with_expiration_date,
    message_with_invalid_format_date,
    message_with_invalid_string_as_date,
    message_with_max_length_title,
    message_with_role_permission,
    message_with_too_long_title,
    message_with_user_permission,
    message,
    uuid_test
)
from src.tests.mocks.role_mocks import roles
from src.tests.mocks.user_mocks import user_db_response
from src.tests.settings import ApiWithAuthTestCase, ApiBaseTestCase
from src.db.cruds.message_crud import MessageCRUD
from src.db.cruds.role_crud import RoleCRUD
from src.db.cruds.user_crud import UserCRUD


class MessageRouteWithoutAuthTestClass(ApiBaseTestCase):
    def setUp(self) -> None:
        self.headers = {'Authorization': 'Bearer invalid_token'}
        return super().setUp()

    def test_list_messages_without_auth(self):
        '''
        A request from a user without permission should return status 401
        '''
        response = self.client.get('/message', headers=self.headers)

        self.assertEqual(401, response.status_code)
        self.assertEqual(
            self.invalid_token_msg,
            response.json()
        )

    def test_delete_message_without_auth(self):
        '''
        A request from a user without permission should return status 401
        '''
        response = self.client.delete(
            f'/message/{uuid_test}',
            headers=self.headers
        )

        self.assertEqual(401, response.status_code)
        self.assertEqual(
            self.invalid_token_msg,
            response.json()
        )

    def test_create_message_without_auth(self):
        '''
        A request from a user without permission should return status 401
        '''
        response = self.client.post(
            '/message',
            headers=self.headers,
            data=message
        )

        self.assertEqual(401, response.status_code)
        self.assertEqual(
            self.invalid_token_msg,
            response.json()
        )

    def test_patch_message_without_auth(self):
        '''
        A request from a user without permission should return status 401
        '''
        response = self.client.patch(
            f'/message/{uuid_test}',
            headers=self.headers,
            data=message
        )

        self.assertEqual(401, response.status_code)
        self.assertEqual(
            self.invalid_token_msg,
            response.json()
        )


class MessageRouteTestClass(ApiWithAuthTestCase):
    def setUp(self) -> None:
        self.headers = {'Authorization': 'Bearer valid_token'}
        return super().setUp()

    def test_list_messages(self):
        '''
        A request from a user with valid_token should return status 200 and message list
        '''
        response = self.client.get('/message', headers=self.headers)

        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {'page': 1, 'results': [], 'total': 0},
            response.json()
        )

    def test_delete_message_without_id_match(self):
        '''
        Should return status 404 when id not found
        '''
        response = self.client.delete(
            f'/message/{uuid_test}',
            headers=self.headers
        )

        self.assertEqual(404, response.status_code)
        self.assertEqual(
            {'detail': 'Mensagem não encontrada'},
            response.json()
        )

    @patch.multiple(
        MessageCRUD,
        delete=MagicMock(return_value=None),
        get=MagicMock(return_value=message)
    )
    def test_delete_message_with_id_match(self):
        '''
        Should return status 204 when delete successfully
        '''
        response = self.client.delete(
            f'/message/{uuid_test}',
            headers=self.headers
        )

        self.assertEqual(204, response.status_code)
        self.assertRaises(JSONDecodeError, response.json)

    def test_create_with_invalid_string_as_expiration_date(self):
        '''
        Should return status 400 when invalid string as date
        '''
        response = self.client.post(
            '/message',
            headers=self.headers,
            json=message_with_invalid_string_as_date
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            response.json(),
            {'detail': 'Data de expiração inválida. Siga o formato YYYY-MM-DD.'}
        )

    def test_create_with_invalid_date_format(self):
        '''
        Should return status 400 when date is in an invalid format
        '''
        response = self.client.post(
            '/message',
            headers=self.headers,
            json=message_with_invalid_format_date
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            response.json(),
            {'detail': 'Data de expiração inválida. Siga o formato YYYY-MM-DD.'}
        )

    @patch('src.controllers.message_controller.datetime', wraps=datetime)
    def test_create_with_day_past(self, datetime_mock):
        '''
        Should return status 400 when setting a expiration date past
        '''
        datetime_mock.now.return_value = datetime.strptime('2100-01-01', '%Y-%m-%d')
        response = self.client.post(
            '/message',
            headers=self.headers,
            json=message_with_expiration_date
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            response.json(),
            {'detail': 'A data de expiração deve ser uma data futura.'}
        )

    def test_create_with_not_found_role(self):
        '''
        Should return status 404 when role id not found
        '''
        response = self.client.post(
            '/message',
            headers=self.headers,
            json=message_with_role_permission
        )

        self.assertEqual(404, response.status_code)
        self.assertEqual(response.json(), {'detail': 'Cargo não encontrado.'})

    def test_create_with_not_found_user(self):
        '''
        Should return status 404 when user id not found
        '''
        response = self.client.post(
            '/message',
            headers=self.headers,
            json=message_with_user_permission
        )

        self.assertEqual(404, response.status_code)
        self.assertEqual(response.json(), {'detail': 'Usuário não encontrado.'})

    def test_create_with_too_long_title(self):
        '''
        Should return status 400 when title has more than
        50 characters
        '''
        response = self.client.post(
            '/message',
            headers=self.headers,
            json={'title': message_with_too_long_title['title'], 'text': 'any text'}
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            response.json(),
            {'detail': 'O título pode ter no máximo 50 caracteres.'}
        )

    @patch.object(RoleCRUD, 'get', return_value=roles[0])
    @patch.object(UserCRUD, 'get', return_value=user_db_response)
    @patch.object(MessageCRUD, 'create', return_value=message_created_with_all_fields)
    @patch('src.controllers.message_controller.datetime', wraps=datetime)
    def test_create_with_all_fields(self, datetime_mock, *_):
        '''
        Should return status 201 when message is created successfully
        '''
        datetime_mock.now.return_value = datetime.strptime('2000-01-01', '%Y-%m-%d')
        response = self.client.post(
            '/message',
            headers=self.headers,
            json=message_with_all_fields
        )

        self.assertEqual(201, response.status_code)
        self.assertEqual(
            response.json(),
            {
                'expiration_date': '2023-12-31T00:00:00',
                'id': '5545ccbe-9e27-4d3f-b26d-5aa5466906c6',
                'role': None,
                'text': 'message text',
                'title': 'message title',
                'user': None,
                'created_at': '2000-01-01T00:00:00',
                'updated_at': None,
                'is_important': True
            }
        )

    @patch.object(
        MessageCRUD,
        'create',
        return_value=dict(**message_with_max_length_title, id=uuid_test)
    )
    def test_create_with_max_length_title(self, create_mock):
        '''
        Should create a message with 50-characters-long title
        '''
        response = self.client.post(
            '/message',
            headers=self.headers,
            json={'title': message_with_max_length_title['title'], 'text': 'any text'}
        )

        self.assertEqual(201, response.status_code)
        create_mock.assert_called()

    def test_patch_with_invalid_string_as_expiration_date(self):
        '''
        Should return status 400 when invalid string as date
        '''
        response = self.client.patch(
            f'/message/{uuid_test}',
            headers=self.headers,
            json=message_with_invalid_string_as_date
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            response.json(),
            {'detail': 'Data de expiração inválida. Siga o formato YYYY-MM-DD.'}
        )

    def test_patch_with_invalid_date_format(self):
        '''
        Should return status 400 when date is in an invalid format
        '''
        response = self.client.patch(
            f'/message/{uuid_test}',
            headers=self.headers,
            json=message_with_invalid_format_date
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            response.json(),
            {'detail': 'Data de expiração inválida. Siga o formato YYYY-MM-DD.'}
        )

    @patch('src.controllers.message_controller.datetime', wraps=datetime)
    def test_patch_with_day_past(self, datetime_mock):
        '''
        Should return status 400 when setting a expiration date past
        '''
        datetime_mock.now.return_value = datetime.strptime('2100-01-01', '%Y-%m-%d')
        response = self.client.patch(
            f'/message/{uuid_test}',
            headers=self.headers,
            json=message_with_expiration_date
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            response.json(),
            {'detail': 'A data de expiração deve ser uma data futura.'}
        )

    def test_patch_with_not_uuid_role(self):
        '''
        Should return status 400 when role_permission is not an uuid
        '''
        response = self.client.patch(
            f'/message/{uuid_test}',
            headers=self.headers,
            json={'role_permission': 'not uuid'}
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual(response.json(), {'detail': 'role_permission deve ser um UUID.'})

    def test_patch_with_not_found_role(self):
        '''
        Should return status 404 when role id not found
        '''
        response = self.client.patch(
            f'/message/{uuid_test}',
            headers=self.headers,
            json=message_with_role_permission
        )

        self.assertEqual(404, response.status_code)
        self.assertEqual(response.json(), {'detail': 'Cargo não encontrado.'})

    def test_patch_with_not_uuid_user(self):
        '''
        Should return status 400 when user_permission is not an uuid
        '''
        response = self.client.patch(
            f'/message/{uuid_test}',
            headers=self.headers,
            json={'user_permission': 'not uuid'}
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual(response.json(), {'detail': 'user_permission deve ser um UUID.'})

    def test_patch_with_not_found_user(self):
        '''
        Should return status 404 when user id not found
        '''
        response = self.client.patch(
            f'/message/{uuid_test}',
            headers=self.headers,
            json=message_with_user_permission
        )

        self.assertEqual(404, response.status_code)
        self.assertEqual(response.json(), {'detail': 'Usuário não encontrado.'})

    @patch.object(RoleCRUD, 'get', return_value=roles[0])
    @patch.object(UserCRUD, 'get', return_value=user_db_response)
    @patch.object(MessageCRUD, 'get', return_value=message)
    @patch.object(MessageCRUD, 'patch', return_value=None)
    @patch('src.controllers.message_controller.datetime', wraps=datetime)
    def test_patch_with_all_fields(self, datetime_mock, *_):
        '''
        Should return status 204 when message is patched successfully
        '''
        datetime_mock.now.return_value = datetime.strptime('2000-01-01', '%Y-%m-%d')
        response = self.client.patch(
            f'/message/{uuid_test}',
            headers=self.headers,
            json=message_with_all_fields
        )

        self.assertEqual(204, response.status_code)
        self.assertRaises(JSONDecodeError, response.json)

    @patch.object(RoleCRUD, 'get', return_value=roles[0])
    @patch.object(UserCRUD, 'get', return_value=user_db_response)
    @patch('src.controllers.message_controller.datetime', wraps=datetime)
    def test_patch_with_all_fields_when_message_id_not_found(self, datetime_mock, *_):
        '''
        Should return status 404 when message id not found
        '''
        datetime_mock.now.return_value = datetime.strptime('2000-01-01', '%Y-%m-%d')
        response = self.client.patch(
            f'/message/{uuid_test}',
            headers=self.headers,
            json=message_with_all_fields
        )

        self.assertEqual(404, response.status_code)
        self.assertEqual({'detail': 'Mensagem não encontrada'}, response.json())

    def test_list_messages_per_permission(self):
        '''
        Should return status 200 and messages list
        '''
        response = self.client.get('/message/me', headers=self.headers)

        self.assertEqual(200, response.status_code)
        self.assertEqual({'page': 1, 'results': [], 'total': 0}, response.json())
