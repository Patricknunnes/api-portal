from fastapi.testclient import TestClient
from unittest import TestCase

from src.main import app

class ApiBaseTestCase(TestCase):
    client: TestClient

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)        
