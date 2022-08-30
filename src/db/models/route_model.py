from uuid import uuid4
from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.sql import func

from src.db.settings.config import Base, GUID


class RouteModel(Base):
    __tablename__ = "routes"

    id = Column(GUID(), unique=True, index=True, default=uuid4)
    method = Column(String(30), primary_key=True, nullable=False)
    path = Column(String(100), primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP,
                        server_default=func.now(),
                        onupdate=func.current_timestamp())
