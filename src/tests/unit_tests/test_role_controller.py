from unittest.mock import patch
from unittest import TestCase
from fastapi import Depends
from sqlalchemy.orm import Session

from src.exceptions.excepetions import NotFoundException
from src.db.cruds.role_crud import RoleCRUD
from src.controllers.role_controller import RoleController
from src.db.settings.config import get_db
from src.tests.mocks.role_mocks import roles, invalid_role_id, valid_role_id


class RoleControllerTestClass(TestCase):
    @patch.object(RoleCRUD, 'list', return_value=roles)
    def test_handle_list(self, mock, session: Session = Depends(get_db)):
        '''
          Test return of all roles from controller
        '''
        result = RoleController().handle_list(db=session)
        self.assertEqual(roles, result)


    @patch.object(RoleCRUD, 'get', return_value=roles[0])
    def test_handle_get_when_id_found(self, mock, session: Session = Depends(get_db)):
        '''
          Test return of single role when id found
        '''
        result = RoleController().handle_get(db=session, exception_message='', object_id=valid_role_id)
        self.assertEqual(roles[0], result)


    @patch.object(RoleCRUD, 'get', return_value=None)
    def test_handle_get_when_id_not_found(self, mock, session: Session = Depends(get_db)):
        '''
          Test raise exception when role id not found
        '''
        with self.assertRaises(NotFoundException) as error:
            RoleController().handle_get(db=session, exception_message='Error', object_id=invalid_role_id)
        exception = error.exception
        self.assertEqual('Error', exception.detail)


    @patch.object(RoleCRUD, 'create', return_value=roles[0])
    def test_handle_create(self, mock, session: Session = Depends(get_db)):
        '''
          Test return of created role
        '''
        result = RoleController().handle_create(db=session, data=roles[0]['name'])
        self.assertEqual(roles[0], result)
