from unittest.mock import patch

from src.db.cruds.client_crud import ClientCRUD
from src.db.models.models import ClientModel
from src.dependencies.sso.sso_utils import AuthRequestParameters
from src.dependencies.sso.validators import ParamsValidator
from src.tests.settings import BaseTestCase

from src.tests.mocks.client_mocks import (
    client_with_secret,
    client_without_secret,
    valid_auth_request_params
)


class ParamsValidatorTestClass(BaseTestCase):
    def setUp(self) -> None:
        self.auth_params = AuthRequestParameters(**valid_auth_request_params)
        return super().setUp()

    def tearDown(self) -> None:
        self.auth_params = AuthRequestParameters(**valid_auth_request_params)
        return super().tearDown()

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

    @patch.object(ClientCRUD, 'get', return_value=ClientModel(**client_with_secret))
    def test_check_invalid_client_secret_receiving_string(self, _):
        result = ParamsValidator().check_client_secret(
            db=self.session,
            client_id=client_with_secret['client_id'],
            client_secret='invalid_secret'
        )
        self.assertFalse(result)

    @patch.object(ClientCRUD, 'get', return_value=ClientModel(**client_with_secret))
    def test_check_invalid_client_secret_receiving_none(self, _):
        result = ParamsValidator().check_client_secret(
            db=self.session,
            client_id=client_with_secret['client_id'],
            client_secret=None
        )
        self.assertFalse(result)

    @patch.object(ClientCRUD, 'get', return_value=ClientModel(**client_with_secret))
    def test_check_valid_client_secret(self, _):
        result = ParamsValidator().check_client_secret(
            db=self.session,
            client_id=client_with_secret['client_id'],
            client_secret='client1_secret'
        )
        self.assertTrue(result)

    @patch.object(ClientCRUD, 'get', return_value=ClientModel(**client_without_secret))
    def test_check_client_secret_unneeded_receiving_none(self, _):
        result = ParamsValidator().check_client_secret(
            db=self.session,
            client_id=client_without_secret['client_id'],
            client_secret=None
        )
        self.assertTrue(result)

    @patch.object(ClientCRUD, 'get', return_value=ClientModel(**client_without_secret))
    def test_check_client_secret_unneeded_receiving_str(self, _):
        result = ParamsValidator().check_client_secret(
            db=self.session,
            client_id=client_without_secret['client_id'],
            client_secret='any_string'
        )
        self.assertTrue(result)

    @patch.object(ClientCRUD, 'get', return_value=ClientModel(**client_without_secret))
    def test_check_invalid_redirect_uri(self, _):
        result = ParamsValidator().check_redirect_uri(
            db=self.session,
            client_id=client_without_secret['client_id'],
            uri='invalid_uri'
        )
        self.assertFalse(result)

    @patch.object(ClientCRUD, 'get', return_value=ClientModel(**client_without_secret))
    def test_check_valid_redirect_uri(self, _):
        result = ParamsValidator().check_redirect_uri(
            db=self.session,
            client_id=client_without_secret['client_id'],
            uri=client_without_secret['redirect_uri']
        )
        self.assertTrue(result)

    @patch.object(ClientCRUD, 'get', return_value=ClientModel(**client_with_secret))
    def test_validate_valid_authorize_params(self, _):
        result = ParamsValidator().validate_authorize_params(
            db=self.session,
            params=self.auth_params
        )
        self.assertTrue(result)

    @patch.object(ClientCRUD, 'get', return_value=None)
    def test_validate_authorize_params_invalid_client_id(self, _):
        self.auth_params.client_id = 'invalid'
        result = ParamsValidator().validate_authorize_params(
            db=self.session,
            params=self.auth_params
        )
        self.assertFalse(result)

    @patch.object(ClientCRUD, 'get', return_value=ClientModel(**client_with_secret))
    def test_validate_authorize_params_invalid_redirect_uri(self, _):
        self.auth_params.redirect_uri = 'invalid'
        result = ParamsValidator().validate_authorize_params(
            db=self.session,
            params=self.auth_params
        )
        self.assertFalse(result)

    @patch.object(ClientCRUD, 'get', return_value=ClientModel(**client_with_secret))
    def test_validate_authorize_params_invalid_response_type(self, _):
        self.auth_params.response_type = 'invalid'
        result = ParamsValidator().validate_authorize_params(
            db=self.session,
            params=self.auth_params
        )
        self.assertFalse(result)

    @patch.object(ClientCRUD, 'get', return_value=ClientModel(**client_with_secret))
    def test_validate_authorize_params_invalid_scope(self, _):
        self.auth_params.scope = 'invalid'
        result = ParamsValidator().validate_authorize_params(
            db=self.session,
            params=self.auth_params
        )
        self.assertFalse(result)
