from uuid import uuid4
from sqlalchemy import Column, String

from src.db.settings.config import Base, GUID


class ClientModel(Base):
    __tablename__ = "clients"

    id = Column(GUID(), primary_key=True, default=uuid4)
    client_id = Column(String(50), nullable=False, unique=True)
    client_secret = Column(String(255), nullable=True)
    redirect_uri = Column(String(255), nullable=False)
