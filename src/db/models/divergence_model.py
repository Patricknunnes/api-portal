from uuid import uuid4
from sqlalchemy import Column, String

from src.db.settings.config import Base, GUID


class DivergenceModel(Base):
    __tablename__ = "divergences"

    id = Column(GUID(), primary_key=True, default=uuid4)
    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=True)
    document = Column(String(11), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    error = Column(String, nullable=False)
