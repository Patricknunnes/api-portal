from unittest.mock import patch

from src.db.cruds.user_crud import UserCRUD
from src.tests.settings import ApiWithAuthTestCase


class UtilsRouteWithAuthTestClass(ApiWithAuthTestCase):
    @patch.object(UserCRUD, 'patch', return_value=None)
    def test_handle_patch_image(self, _):
        '''
        Should return status 201 and None in body
        '''
        response = self.client.patch(
            '/utils/image',
            json={'image': 'profile_image'}
        )
        self.assertEqual(204, response.status_code)
