from uuid import uuid4
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.db.settings.config import Base, GUID


class UserModel(Base):
    __tablename__ = "users"

    id = Column(GUID(), primary_key=True, default=uuid4)
    role_id = Column(GUID(), ForeignKey("roles.id"))
    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    document = Column(String(11), nullable=False)
    phone = Column(String(12), nullable=True)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP,
                        server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True, onupdate=func.current_timestamp())

    role = relationship("RoleModel")
