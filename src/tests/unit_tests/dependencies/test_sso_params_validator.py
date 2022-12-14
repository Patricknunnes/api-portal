from unittest.mock import patch

from src.db.cruds.client_crud import ClientCRUD
from src.dependencies.sso.validators import ParamsValidator
from src.tests.settings import BaseTestCase
from src.tests.mocks.client_mocks import client_with_secret


class ParamsValidatorTestClass(BaseTestCase):
    @patch.object(ClientCRUD, 'get', return_value=None)
    def test_check_invalid_client_id(self, _):
        result = ParamsValidator().check_client_id(
            db=self.session,
            client_id='invalid_client'
        )
        self.assertFalse(result)

    @patch.object(ClientCRUD, 'get', return_value=client_with_secret)
    def test_check_valid_client_id(self, _):
        result = ParamsValidator().check_client_id(
            db=self.session,
            client_id=client_with_secret['client_id']
        )
        self.assertTrue(result)

    def test_check_invalid_scope(self):
        result = ParamsValidator().check_scope(request_scope='invalid_scope')
        self.assertFalse(result)

    def test_check_valid_scope(self):
        result = ParamsValidator().check_scope(request_scope='openid another_scope')
        self.assertTrue(result)

    def test_check_invalid_response_type(self):
        result = ParamsValidator().check_response_type(type='invalid_type')
        self.assertFalse(result)

    def test_check_valid_response_type(self):
        result = ParamsValidator().check_response_type(type='code')
        self.assertTrue(result)
