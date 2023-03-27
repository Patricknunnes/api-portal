from uuid import uuid4
from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.sql import func

from src.db.settings.config import Base, GUID


class InstitutionModel(Base):
    __tablename__ = "institutions"

    id = Column(GUID(), primary_key=True, default=uuid4)
    name = Column(String(50), nullable=False, unique=True)
    created_at = Column(TIMESTAMP,
                        server_default=func.now(),
                        onupdate=func.current_timestamp())
