from src.tests.integration_tests.settings import ApiBaseTestCase


class RootRouteTestClass(ApiBaseTestCase):
    def test_root(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)
        self.assertEqual({'message': 'Hello World'}, response.json())
