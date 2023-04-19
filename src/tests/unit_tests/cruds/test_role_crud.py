from src.tests.mocks.access_mocks import access_1, access_2, access_3
from src.tests.mocks.role_mocks import role_1, role_2, invalid_role_id
from src.tests.settings import BaseTestCase

from src.db.cruds.role_crud import RoleCRUD
from src.db.models.models import RoleModel
from src.db.models.access_model import access_role


class RoleCrudTestClass(BaseTestCase):
    def setUp(self) -> None:
        '''
        Insert row with role_1 data before each test
        '''
        super().setUp()
        return RoleCRUD().create(db=self.session, data=role_1)

    def tearDown(self) -> None:
        '''
        Delete row with role_1 data before each test
        '''
        RoleCRUD().delete(db=self.session, object_id=role_1['id'])
        return super().tearDown()

    def test_list(self):
        '''
          Should return list
        '''
        result = RoleCRUD().list(db=self.session)
        self.assertEqual(type(result), list)

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
        result = RoleCRUD().get(db=self.session, id=role_1['id'])
        self.assertTrue(isinstance(result, RoleModel))

    def test_list_allowed_accesses_when_there_is_no_access_for_the_role(self):
        '''
          Should return an empty list of accesses when
          there is no access allowed to the role
        '''
        result = RoleCRUD().list_allowed_accesses(db=self.session, role_id=role_1['id'])
        self.assertEqual(result, [])

    def test_list_allowed_accesses(self):
        '''
        Should return a list of accesses allowed to the role_id
        '''
        self.session.add_all([access_1, access_2, access_3])
        self.session.commit()
        role = RoleModel(**role_2)
        role.accesses = [access_1, access_2]
        self.session.add(role)
        self.session.commit()

        result = RoleCRUD().list_allowed_accesses(db=self.session, role_id=role_2['id'])
        self.assertEqual(result, role.accesses)

        remove_access_role = access_role.delete() \
            .where(access_role.c.role_id == role_2['id'])
        self.session.execute(remove_access_role)
        RoleCRUD().delete(db=self.session, object_id=role.id)

    def test_list_allowed_accesses_when_role_is_invalid(self):
        '''
        Should return None when role_id is invalid
        '''
        result = RoleCRUD().list_allowed_accesses(
            db=self.session,
            role_id=invalid_role_id
        )
        self.assertIsNone(result)
