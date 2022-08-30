from uuid import uuid4
from sqlalchemy import Column, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func

from src.db.settings.config import Base, GUID


class PermissionModel(Base):
    __tablename__ = "permissions"

    id = Column(GUID(), primary_key=True, default=uuid4)
    role_id = Column(GUID(), ForeignKey("roles.id"))
    route_id = Column(GUID(), ForeignKey("routes.id"))
    created_at = Column(TIMESTAMP,
                        server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True, onupdate=func.current_timestamp())
