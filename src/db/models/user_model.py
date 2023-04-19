from uuid import uuid4
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Boolean, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.db.settings.config import Base, GUID


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(GUID(), primary_key=True, default=uuid4)
    role_id = Column(GUID(), ForeignKey('roles.id'))
    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    document = Column(String(11), nullable=False)
    phone = Column(String(12), nullable=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    image = Column(String, nullable=True)
    is_totvs = Column(Boolean, nullable=False, default=False)
    canvas_id = Column(Integer, nullable=True, unique=True)
    last_sync = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    session_code = Column(String(25), nullable=True, unique=True)
    institution_id = Column(
        GUID(),
        ForeignKey('institutions.id'),
        default='dcef34bf-2cc6-4d67-b6af-803e7e33d0f3'
    )

    role = relationship('RoleModel')
    institution = relationship('InstitutionModel')
