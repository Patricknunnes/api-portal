from src.db.cruds.role_crud import RoleCRUD
from src.tests.settings import BaseTestCase
from src.tests.mocks.role_mocks import roles, invalid_role_id, valid_role_id


class RoleCrudTestClass(BaseTestCase):
    def test_list(self):
        '''
          Should return list
        '''
        result = RoleCRUD().list(db=self.session)
        self.assertEqual(type(result), list)
        self.assertEqual([], result)

    def test_get_when_id_not_found(self):
        '''
          Should return None when id not found
        '''
        result = RoleCRUD().get(db=self.session, id=invalid_role_id)
        self.assertIsNone(result)

    def test_get_when_id_found(self):
        '''
          Should return role when id found
        '''
        RoleCRUD().create(db=self.session, data=roles[0])
        result = RoleCRUD().get(db=self.session, id=valid_role_id)
        self.assertIsNotNone(result)
