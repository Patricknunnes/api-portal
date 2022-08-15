from fastapi.testclient import TestClient
from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.db.settings.config import Base, get_db
from src.shared.auth.auth_utils import current_user
from src.tests.mocks.user_mocks import user_db_response

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    connection = engine.connect()

    connection.begin()

    db = TestingSessionLocal(bind=connection)

    yield db

    db.rollback()
    connection.close()


app.dependency_overrides[get_db] = override_get_db


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.session = next(override_get_db())


class ApiBaseTestCase(TestCase):
    client: TestClient
    invalid_token_msg = {'detail': 'Token invalido.'}

    def setUp(self) -> None:
        app.dependency_overrides[get_db] = override_get_db

    def tearDown(self) -> None:
        app.dependency_overrides = {}

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)


def override_current_user():
        return user_db_response


class ApiWithAuthTestCase(ApiBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        app.dependency_overrides[current_user] = override_current_user
