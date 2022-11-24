from unittest import TestCase
from unittest.mock import patch, MagicMock

from src.dependencies.canvas.api_integration import CanvasApiIntegration


class CanvasIntegrationTestClass(TestCase):
    canvas = CanvasApiIntegration()

    @patch('requests.get', return_value=MagicMock(ok=False))
    def test_request_login_id_when_fail(self, _):
        '''Failed login_id request should return None'''
        result = self.canvas._CanvasApiIntegration__request_login_id(9999)
        self.assertIsNone(result)

    @patch('requests.get', return_value=MagicMock(ok=True, json= lambda : [{'id': 20}]))
    def test_request_login_id_when_succeed(self, _):
        '''Succeeded login_id request should return login_id'''
        result = self.canvas._CanvasApiIntegration__request_login_id(1)
        self.assertEqual(result, 20)

    @patch('requests.put', return_value=MagicMock(ok=False))
    def test_update_login_data_when_fail(self, _):
        '''Failed update login data request should return False'''
        result = self.canvas._CanvasApiIntegration__update_login_data(1, {})
        self.assertFalse(result)

    @patch('requests.put', return_value=MagicMock(ok=True))
    def test_update_login_data_when_succeed(self, _):
        '''Succeeded update login data request should return True'''
        result = self.canvas._CanvasApiIntegration__update_login_data(1, {})
        self.assertTrue(result)

    @patch.object(
        CanvasApiIntegration,
        '_CanvasApiIntegration__request_login_id',
        return_value=None
    )
    def test_sync_password_with_no_login_id(self, request_mock):
        '''
        Should return False when __request_login_id return None
        '''
        result = self.canvas.sync_password(1, 'password')
        request_mock.assert_called_with(1)
        self.assertFalse(result)

    @patch.object(
        CanvasApiIntegration,
        '_CanvasApiIntegration__update_login_data',
        return_value=False
    )
    @patch.object(
        CanvasApiIntegration,
        '_CanvasApiIntegration__request_login_id',
        return_value=2
    )
    def test_sync_password_with_update_fail(self, request_mock, update_mock):
        '''
        Should return False when __request_login_id return id
        but __update_login fail
        '''
        result = self.canvas.sync_password(1, 'password')
        request_mock.assert_called_with(1)
        update_mock.assert_called_with(2, {'login[password]': 'password'})
        self.assertFalse(result)

    @patch.object(
        CanvasApiIntegration,
        '_CanvasApiIntegration__update_login_data',
        return_value=True
    )
    @patch.object(
        CanvasApiIntegration,
        '_CanvasApiIntegration__request_login_id',
        return_value=2
    )
    def test_sync_password_with_update_success(self, request_mock, update_mock):
        '''
        Should return True when __request_login_id return id
        and __update_login succeed
        '''
        result = self.canvas.sync_password(1, 'password')
        request_mock.assert_called_with(1)
        update_mock.assert_called_with(2, {'login[password]': 'password'})
        self.assertTrue(result)
