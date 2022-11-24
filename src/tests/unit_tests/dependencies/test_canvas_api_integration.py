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
