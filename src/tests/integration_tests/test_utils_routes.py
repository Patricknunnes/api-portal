from unittest.mock import patch

from src.db.cruds.user_crud import UserCRUD
from src.tests.settings import ApiWithAuthTestCase


class UtilsRouteWithAuthTestClass(ApiWithAuthTestCase):
    @patch.object(UserCRUD, 'patch', return_value=None)
    def test_handle_insert_image(self, _):
        '''
        Should return status 201 and None in body
        '''
        response = self.client.post(
            '/utils/image',
            json={'image': 'profile_image'}
        )
        self.assertEqual(201, response.status_code)
        self.assertEqual(None, response.json())
