from uuid import uuid4
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.db.settings.config import Base, GUID


class TokenModel(Base):
    __tablename__ = 'tokens'

    id = Column(GUID(), primary_key=True, default=uuid4)
    user_id = Column(String(50), ForeignKey('users.id'), nullable=False)
    token_hash = Column(String(150), nullable=False, unique=True)
    expiration_date = Column(TIMESTAMP, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship('UserModel')
