from unittest.mock import patch

from src.tests.settings import BaseTestCase
from src.db.cruds.user_crud import UserCRUD
from src.dependencies.sso.controller import SSOController
from src.tests.mocks.user_mocks import totvs_user_db_response


class SSOControllerTestClass(BaseTestCase):
    code_mock = 'atetd_et_tat_idatiidstis_'

    @patch('src.dependencies.sso.controller.choices', return_value=code_mock)
    @patch.object(UserCRUD, 'patch')
    def test_create_session(self, user_patch_mock, _):
        '''
        Test code is created, inserted in user row and returned
        '''
        result = SSOController().create_session(
            user_id='valid_id',
            state='valid_state',
            db=self.session
        )
        user_patch_mock.assert_called_with(
            db=self.session,
            object_id='valid_id',
            data={'session_code': self.code_mock}
        )
        self.assertEqual(result, self.code_mock)

    @patch.object(UserCRUD, 'get', return_value=totvs_user_db_response)
    def test_validate_session_with_valid_code(self, _):
        '''
        Test user is returned
        '''
        result = SSOController().validate_session(
            session_code=totvs_user_db_response['session_code'],
            db=self.session
        )
        self.assertIsNotNone(result)

    @patch.object(UserCRUD, 'get', return_value=None)
    def test_validate_session_with_invalid_code(self, _):
        '''
        Test None is returned when code is invalid
        '''
        result = SSOController().validate_session(
            session_code='invalid_code',
            db=self.session
        )
        self.assertIsNone(result)
