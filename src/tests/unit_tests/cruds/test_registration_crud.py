from src.tests.settings import BaseTestCase

from src.db.cruds.registration_crud import RegistrationCRUD
from src.db.models.models import RegistrationModel, RoleModel, UserModel
from src.schemas.registration_schema import StatusEnum

from src.tests.mocks.role_mocks import role_1, role_2, role_3
from src.tests.mocks.registration_mocks import registrations

users = [
    {
        'id': '071aac88-f263-4c07-b215-7170d180da6a',
        'name': 'user1',
        'email': 'user1@email.com',
        'document': '12345678901',
        'username': 'username1',
        'phone': None,
        'is_totvs': False,
        'password': 'user_password',
        'role': RoleModel(**role_1),
        'image': None
    },
    {
        'id': '071aac88-f263-4c07-b215-7170d180da6b',
        'name': 'user2',
        'email': 'user2@email.com',
        'document': '12345678902',
        'username': 'username2',
        'phone': None,
        'is_totvs': False,
        'password': 'user_password',
        'role': RoleModel(**role_2),
        'image': None
    },
    {
        'id': '071aac88-f263-4c07-b215-7170d180da8b',
        'name': 'user3',
        'email': 'user3@email.com',
        'document': '12345678903',
        'username': 'username3',
        'phone': None,
        'is_totvs': False,
        'password': 'user_password',
        'role': RoleModel(**role_3),
        'image': None
    },
]


class RegistrationCrudTestClass(BaseTestCase):
    def test_handle_list_with_extra_parameters(self):
        '''
          Should return sorted and filtered lists
        '''
        self.session.add_all([UserModel(**user) for user in users])
        self.session.add_all(
            [RegistrationModel(**registration) for registration in registrations])
        self.session.commit()

        result = RegistrationCRUD().handle_list(
            db=self.session,
            filter_attrs=[],
            sort=(('status', 'desc'),)
        )
        self.assertEqual(result['total'], 3)
        self.assertEqual(result['results'][0].status, StatusEnum.REJECTED)
        self.assertEqual(result['results'][1].status, StatusEnum.APPROVED)
        self.assertEqual(result['results'][2].status, StatusEnum.ANALYSIS)

        result = RegistrationCRUD().handle_list(
            db=self.session,
            filter_attrs=['status'],
            filters='ap'
        )
        self.assertEqual(result['total'], 1)
        self.assertEqual(result['results'][0].status, StatusEnum.APPROVED)

        self.session.rollback()
