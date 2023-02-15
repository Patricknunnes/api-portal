from unittest.mock import patch

from src.exceptions.exceptions import NotFoundException
from src.db.cruds.role_crud import RoleCRUD
from src.controllers.role_controller import RoleController
from src.tests.settings import BaseTestCase
from src.tests.mocks.role_mocks import roles, invalid_role_id, valid_role_id


class RoleControllerTestClass(BaseTestCase):
    @patch.object(RoleCRUD, 'list', return_value=roles)
    def test_handle_list(self, _):
        '''
          Should return list with all roles
        '''
        result = RoleController().handle_list(db=self.session)
        self.assertEqual(roles, result)

    @patch.object(RoleCRUD, 'get', return_value=roles[0])
    def test_handle_get_when_id_found(self, _):
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
    def test_handle_get_when_id_not_found(self, _):
        '''
          Should raise exception when role id not found
        '''
        with self.assertRaises(NotFoundException) as error:
            RoleController().handle_get(db=self.session,
                                        exception_message='Error',
                                        object_id=invalid_role_id)
        exception = error.exception
        self.assertEqual('Error', exception.detail)

    @patch.object(RoleCRUD, 'list_allowed_accesses', return_value=None)
    def test_handle_list_allowed_accesses_when_crud_return_none(self, _):
        '''
          Should raise exception when
          crud_class' list_allowed_accesses method returns None
        '''
        with self.assertRaises(NotFoundException) as error:
            RoleController().handle_list_allowed_accesses(
                db=self.session,
                exception_message='Error',
                role_id=invalid_role_id
            )
        exception = error.exception
        self.assertEqual('Error', exception.detail)

    @patch.object(RoleCRUD, 'list_allowed_accesses', return_value=[])
    def test_handle_list_allowed_accesses(self, _):
        '''
          Should return the result of crud_class'
          list_allowed_accesses method when it is not None
        '''
        result = RoleController().handle_list_allowed_accesses(
            db=self.session,
            exception_message='Error',
            role_id=invalid_role_id
        )
        self.assertEqual(result, [])
