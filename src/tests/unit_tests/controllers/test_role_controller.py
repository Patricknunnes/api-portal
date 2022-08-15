from unittest.mock import patch

from src.exceptions.exceptions import NotFoundException
from src.db.cruds.role_crud import RoleCRUD
from src.controllers.role_controller import RoleController
from src.tests.settings import BaseTestCase
from src.tests.mocks.role_mocks import roles, invalid_role_id, valid_role_id


class RoleControllerTestClass(BaseTestCase):
    @patch.object(RoleCRUD, 'list', return_value=roles)
    def test_handle_list(self, mock):
        '''
          Should return list with all roles
        '''
        result = RoleController().handle_list(db=self.session)
        self.assertEqual(roles, result)

    @patch.object(RoleCRUD, 'get', return_value=roles[0])
    def test_handle_get_when_id_found(self, mock):
        '''
          Should return single role when id found
        '''
        result = RoleController().handle_get(
            db=self.session,
            exception_message='',
            object_id=valid_role_id
        )
        self.assertEqual(roles[0], result)

    @patch.object(RoleCRUD, 'get', return_value=None)
    def test_handle_get_when_id_not_found(self, mock):
        '''
          Should raise exception when role id not found
        '''
        with self.assertRaises(NotFoundException) as error:
            RoleController().handle_get(db=self.session,
                                        exception_message='Error',
                                        object_id=invalid_role_id)
        exception = error.exception
        self.assertEqual('Error', exception.detail)
