from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4
from src.schemas.registration_schema import StatusEnum

from src.db.settings.config import Base, GUID


class RegistrationModel(Base):
    __tablename__ = 'registrations'

    id = Column(GUID(), unique=True, index=True, default=uuid4)
    document = Column(String(11), ForeignKey('users.document'), primary_key=True)
    email = Column(String(150), nullable=False)
    birthdate = Column(TIMESTAMP, nullable=False)
    status = Column(Enum(StatusEnum), nullable=False)
    service = Column(String(50), nullable=False, primary_key=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship('UserModel')
