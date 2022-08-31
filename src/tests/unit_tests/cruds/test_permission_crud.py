from src.schemas.auth_schema import PermissionParams
from src.tests.settings import BaseTestCase

from src.db.cruds.route_crud import RouteCRUD
from src.db.cruds.permission_crud import PermissionCRUD

from src.tests.mocks.route_mocks import ROUTES, VALID_ROUTE_ID
from src.tests.mocks.permission_mocks import GET_PERMISSION, GET_PERMISSION_ERROR
from src.tests.mocks.role_mocks import valid_role_id


class PermissionCrudTestClass(BaseTestCase):

    def test_get_when_permission_not_found(self):
        '''
          Should return None when params not found
        '''
        result = PermissionCRUD().get_permission(
            db=self.session,
            datas=PermissionParams(**GET_PERMISSION_ERROR)
        )

        self.assertIsNone(result)

    def test_get_when_permission_found(self):
        '''
          Should return a permission id
        '''

        RouteCRUD().create(db=self.session, data=ROUTES[0])

        new_permission = {
            'id': 'ddeb34a8-d9bf-416e-8a5d-96e1cef213ed',
            'role_id': valid_role_id,
            'route_id': VALID_ROUTE_ID
        }

        PermissionCRUD().create(db=self.session, data=new_permission)

        result = PermissionCRUD().get_permission(
            db=self.session,
            datas=PermissionParams(**GET_PERMISSION)
        )

        self.assertEqual(str(result[0]), new_permission.get('id'))
