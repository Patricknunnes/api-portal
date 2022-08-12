from unittest import TestCase
from unittest.mock import patch
from fastapi import Depends
from sqlalchemy.orm import Session

from src.db.cruds.role_crud import RoleCRUD
from src.tests.settings import BaseTestCase
from src.tests.mocks.role_mocks import roles, invalid_role_id, valid_role_id


class RoleCrudTestClass(BaseTestCase):
    def test_list(self):
        '''
          Test return of list from crud
        '''
        result = RoleCRUD().list(db=self.session)
        self.assertEqual(type(result), list)
        self.assertEqual([], result)

    
    def test_get_when_id_not_found(self):
        '''
          Test return of None from crud when id not found
        '''
        result = RoleCRUD().get(db=self.session, id=invalid_role_id)
        self.assertIsNone(result)


    def test_get_when_id_found(self):
        '''
          Test return of role from crud when id found
        '''
        RoleCRUD().create(db=self.session, data=roles[0])
        result = RoleCRUD().get(db=self.session, id=valid_role_id)
        self.assertIsNotNone(result)