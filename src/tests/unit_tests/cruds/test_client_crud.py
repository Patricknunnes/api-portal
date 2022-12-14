from src.db.cruds.client_crud import ClientCRUD
from src.db.models.models import ClientModel
from src.tests.mocks.client_mocks import client_with_secret, client_without_secret
from src.tests.settings import BaseTestCase


class ClientCRUDTestClass(BaseTestCase):
    def test_create(self):
        '''Should return created client'''
        result = ClientCRUD().create(db=self.session, data=client_with_secret)
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, ClientModel))

    def test_get_client_with_match(self):
        '''Should return client found'''
        result = ClientCRUD().get(
            db=self.session,
            client_id=client_with_secret['client_id']
        )
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, ClientModel))

    def test_get_client_without_match(self):
        '''Should return None when client_id match no client'''
        result = ClientCRUD().get(
            db=self.session,
            client_id=client_without_secret['client_id']
        )
        self.assertIsNone(result)
