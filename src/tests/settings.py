from fastapi.testclient import TestClient
from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.db.settings.config import Base, get_db

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

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
