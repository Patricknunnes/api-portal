from uuid import uuid4
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.db.settings.config import Base, GUID


class UserModel(Base):
    __tablename__ = "users"

    id = Column(GUID(), primary_key=True, default=uuid4)
    role_id = Column(GUID(), ForeignKey("roles.id"))
    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    document = Column(String(11), nullable=False, unique=True)
    phone = Column(String(12), nullable=True)
    username = Column(String(50), nullable=True, unique=True)
    password = Column(String(255), nullable=False)
    is_totvs = Column(Boolean, nullable=False, default=False)
    last_sync = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP,
                        server_default=func.now())

    role = relationship("RoleModel")
